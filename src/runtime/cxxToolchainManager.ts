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

export interface CxxToolchainManagerOptions {
  executor?: IProcessExecutor;
  compilers?: string[];
  tmpDir?: string;
}

export class CxxToolchainManager {
  private executor: IProcessExecutor;
  private candidateCompilers: string[];
  private tmpDir: string;
  private cachedDiagnostic: CxxDiagnostic | null = null;

  constructor(options?: CxxToolchainManagerOptions) {
    this.executor = options?.executor || new NodeProcessExecutor();
    this.candidateCompilers = options?.compilers || ["g++", "clang++", "c++"];
    this.tmpDir = options?.tmpDir || os.tmpdir();
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
    } catch (_) {
      // ignore
    }
  }
}
