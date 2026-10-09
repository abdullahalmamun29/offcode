/**
 * Decoupled C++ Toolchain Manager for CHUP.
 *
 * Requirements:
 * - Completely separate from Python runtime management so C++ errors never masquerade as Python errors.
 * - Discovers g++ / clang++.
 * - Performs a genuine C++17 compilation probe to prove C++17 capabilities.
 * - Cleans up probe files safely in os.tmpdir().
 */

import * as os from "os";
import * as path from "path";
import * as fs from "fs";
import { CxxDiagnostic } from "./types";
import { IProcessExecutor, NodeProcessExecutor } from "./processExecutor";

const CXX17_PROBE_SOURCE = `
#include <iostream>
#include <string_view>
#include <optional>

int main() {
    std::string_view sv = "cxx17_ready";
    std::optional<int> opt = 42;
    if (opt.has_value() && !sv.empty()) {
        std::cout << sv << std::endl;
        return 0;
    }
    return 1;
}
`.trim();

const STANDARD_WINDOWS_COMPILER_PATHS: string[] = [
  // Code::Blocks MinGW (standard university lab installs)
  "C:\\Program Files\\CodeBlocks\\MinGW\\bin\\g++.exe",
  "C:\\Program Files (x86)\\CodeBlocks\\MinGW\\bin\\g++.exe",
  "D:\\Program Files\\CodeBlocks\\MinGW\\bin\\g++.exe",
  "D:\\Program Files (x86)\\CodeBlocks\\MinGW\\bin\\g++.exe",
  // Dev-C++ / Embarcadero Dev-C++
  "C:\\Program Files (x86)\\Dev-Cpp\\MinGW64\\bin\\g++.exe",
  "C:\\Dev-Cpp\\MinGW64\\bin\\g++.exe",
  "C:\\Dev-Cpp\\bin\\g++.exe",
  "D:\\Dev-Cpp\\MinGW64\\bin\\g++.exe",
  // Standalone MinGW / MinGW-w64
  "C:\\MinGW\\bin\\g++.exe",
  "C:\\MinGW\\bin\\c++.exe",
  "C:\\MinGW64\\bin\\g++.exe",
  "D:\\MinGW\\bin\\g++.exe",
  // MSYS2 environments
  "C:\\msys64\\ucrt64\\bin\\g++.exe",
  "C:\\msys64\\mingw64\\bin\\g++.exe",
  "C:\\msys64\\usr\\bin\\g++.exe",
  "D:\\msys64\\ucrt64\\bin\\g++.exe",
  "D:\\msys64\\mingw64\\bin\\g++.exe",
  // TDM-GCC
  "C:\\TDM-GCC-64\\bin\\g++.exe",
  "C:\\TDM-GCC-32\\bin\\g++.exe",
  "D:\\TDM-GCC-64\\bin\\g++.exe",
  // LLVM / Clang on Windows
  "C:\\Program Files\\LLVM\\bin\\clang++.exe",
  "C:\\Program Files (x86)\\LLVM\\bin\\clang++.exe",
  // w64devkit
  "C:\\w64devkit\\bin\\g++.exe",
  "D:\\w64devkit\\bin\\g++.exe"
];

export interface CxxToolchainManagerOptions {
  executor?: IProcessExecutor;
  compilers?: string[];
  tmpDir?: string;
  configuredCompiler?: string;
}

export class CxxToolchainManager {
  private executor: IProcessExecutor;
  private candidateCompilers: string[];
  private tmpDir: string;
  private cachedDiagnostic: CxxDiagnostic | null = null;

  constructor(options?: CxxToolchainManagerOptions) {
    this.executor = options?.executor || new NodeProcessExecutor();
    this.tmpDir = options?.tmpDir || os.tmpdir();

    if (options?.compilers) {
      this.candidateCompilers = [...options.compilers];
    } else {
      const candidates: string[] = [];
      if (options?.configuredCompiler && options.configuredCompiler.trim()) {
        candidates.push(options.configuredCompiler.trim());
      }
      candidates.push("g++", "clang++", "c++");

      if (process.platform === "win32") {
        for (const winPath of STANDARD_WINDOWS_COMPILER_PATHS) {
          try {
            if (fs.existsSync(winPath) && !candidates.includes(winPath)) {
              candidates.push(winPath);
            }
          } catch {
            // ignore filesystem access errors
          }
        }
      }

      this.candidateCompilers = candidates;
    }
  }

  public async validateToolchain(forceRefresh = false): Promise<CxxDiagnostic> {
    if (!forceRefresh && this.cachedDiagnostic && this.cachedDiagnostic.status === "READY") {
      return this.cachedDiagnostic;
    }

    let compilerMissing = true;
    let lastError = "";

    for (const compiler of this.candidateCompilers) {
      // 1. Check if compiler binary can be executed
      const verResult = await this.executor.execFile(compiler, ["--version"], { timeout: 3000 });
      if (verResult.exitCode !== 0 && !verResult.stdout.trim()) {
        continue;
      }

      compilerMissing = false;
      const firstLine = verResult.stdout.trim().split("\n")[0] || compiler;

      // 2. Perform actual C++17 compile probe
      const probeId = `chup_cxx_probe_${Date.now()}_${Math.floor(Math.random() * 1000000)}`;
      const sourceFile = path.join(this.tmpDir, `${probeId}.cpp`);
      const binaryFile = path.join(this.tmpDir, probeId);

      try {
        fs.writeFileSync(sourceFile, CXX17_PROBE_SOURCE, "utf8");

        const compileResult = await this.executor.execFile(
          compiler,
          ["-std=c++17", "-Wall", "-Wextra", sourceFile, "-o", binaryFile],
          { timeout: 5000 }
        );

        if (compileResult.exitCode === 0) {
          const diag: CxxDiagnostic = {
            status: "READY",
            compilerPath: compiler,
            compilerVersion: firstLine
          };
          this.cachedDiagnostic = diag;
          this.cleanupFile(sourceFile);
          this.cleanupFile(binaryFile);
          return diag;
        } else {
          lastError = `C++17 probe compilation failed with ${compiler}: ${compileResult.stderr.trim()}`;
        }
      } catch (err: any) {
        lastError = `C++17 probe error with ${compiler}: ${err.message}`;
      } finally {
        this.cleanupFile(sourceFile);
        this.cleanupFile(binaryFile);
      }
    }

    const diag: CxxDiagnostic = compilerMissing
      ? {
          status: "CXX_COMPILER_MISSING",
          errorMessage: "No C++ compiler (g++ or clang++) could be found on PATH."
        }
      : {
          status: "CXX_PROBE_FAILED",
          errorMessage: lastError || "C++ compiler failed C++17 compilation probe."
        };

    this.cachedDiagnostic = diag;
    return diag;
  }

  public validateToolchainSync(): CxxDiagnostic {
    if (this.cachedDiagnostic && this.cachedDiagnostic.status === "READY") {
      return this.cachedDiagnostic;
    }

    let compilerMissing = true;
    let lastError = "";

    for (const compiler of this.candidateCompilers) {
      const verResult = this.executor.execFileSync(compiler, ["--version"], { timeout: 3000 });
      if (verResult.exitCode !== 0 && !verResult.stdout.trim()) {
        continue;
      }

      compilerMissing = false;
      const firstLine = verResult.stdout.trim().split("\n")[0] || compiler;

      const probeId = `chup_cxx_probe_${Date.now()}_${Math.floor(Math.random() * 1000000)}`;
      const sourceFile = path.join(this.tmpDir, `${probeId}.cpp`);
      const binaryFile = path.join(this.tmpDir, probeId);

      try {
        fs.writeFileSync(sourceFile, CXX17_PROBE_SOURCE, "utf8");

        const compileResult = this.executor.execFileSync(
          compiler,
          ["-std=c++17", "-Wall", "-Wextra", sourceFile, "-o", binaryFile],
          { timeout: 5000 }
        );

        if (compileResult.exitCode === 0) {
          const diag: CxxDiagnostic = {
            status: "READY",
            compilerPath: compiler,
            compilerVersion: firstLine
          };
          this.cachedDiagnostic = diag;
          this.cleanupFile(sourceFile);
          this.cleanupFile(binaryFile);
          return diag;
        } else {
          lastError = `C++17 probe compilation failed with ${compiler}: ${compileResult.stderr.trim()}`;
        }
      } catch (err: any) {
        lastError = `C++17 probe error with ${compiler}: ${err.message}`;
      } finally {
        this.cleanupFile(sourceFile);
        this.cleanupFile(binaryFile);
      }
    }

    const diag: CxxDiagnostic = compilerMissing
      ? {
          status: "CXX_COMPILER_MISSING",
          errorMessage: "No C++ compiler (g++ or clang++) could be found on PATH."
        }
      : {
          status: "CXX_PROBE_FAILED",
          errorMessage: lastError || "C++ compiler failed C++17 compilation probe."
        };

    this.cachedDiagnostic = diag;
    return diag;
  }

  private cleanupFile(fp: string): void {
    try {
      if (fs.existsSync(fp)) {
        fs.unlinkSync(fp);
      }
      if (fs.existsSync(`${fp}.exe`)) {
        fs.unlinkSync(`${fp}.exe`);
      }
    } catch (_) {
      // ignore
    }
  }
}
