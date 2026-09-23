/**
 * Bounded, Platform-Aware Python Candidate Discovery.
 *
 * Implements deterministic candidate discovery across Windows, Linux, and macOS.
 * Strictly adheres to precedence:
 *   1. Explicit configuration (offcode.pythonPath / chup.pythonPath)
 *   2. VS Code selected interpreter (if available)
 *   3. Active virtual environment (VIRTUAL_ENV / CONDA_PREFIX)
 *   4. Workspace virtual environment (.venv / venv)
 *   5. Platform-native launcher (Windows py launcher)
 *   6. PATH-discovered executables (python3 / python / python.exe)
 *   7. Conservative known installation locations
 *
 * PROHIBITION: Never performs recursive filesystem crawling or broad disk searches.
 */

import * as path from "path";
import { PythonCandidate, PythonRuntimeSource } from "./types";
import { IFileSystem, NodeFileSystem } from "./fileSystem";
import { detectProjectRoot } from "./projectRoot";

export interface DiscoveryOptions {
  configuredPath?: string;
  projectRoot?: string;
  platform?: NodeJS.Platform;
  env?: NodeJS.ProcessEnv;
  fs?: IFileSystem;
  vscodePythonInterpreter?: string;
}

export class PythonDiscoveryService {
  private fs: IFileSystem;
  private platform: NodeJS.Platform;
  private env: NodeJS.ProcessEnv;
  private projectRoot: string;
  private configuredPath?: string;
  private vscodePythonInterpreter?: string;

  constructor(options?: DiscoveryOptions) {
    this.fs = options?.fs || new NodeFileSystem();
    this.platform = options?.platform || process.platform;
    this.env = options?.env || process.env;
    this.projectRoot = detectProjectRoot(options?.projectRoot, this.fs);
    this.configuredPath = options?.configuredPath;
    this.vscodePythonInterpreter = options?.vscodePythonInterpreter;
  }

  public discoverCandidates(): PythonCandidate[] {
    const candidates: PythonCandidate[] = [];

    // 1. Explicit configuration
    if (this.configuredPath && this.configuredPath.trim().length > 0) {
      candidates.push({
        executable: this.normalizePath(this.configuredPath.trim()),
        args: [],
        source: "configured",
        description: "Explicitly configured offcode.pythonPath / chup.pythonPath"
      });
    }

    // 2. VS Code selected interpreter
    if (this.vscodePythonInterpreter && this.vscodePythonInterpreter.trim().length > 0) {
      candidates.push({
        executable: this.normalizePath(this.vscodePythonInterpreter.trim()),
        args: [],
        source: "vscode",
        description: "VS Code Python extension selected interpreter"
      });
    }

    // 3. Active virtual environment (VIRTUAL_ENV, CONDA_PREFIX)
    this.discoverActiveEnvironment(candidates);

    // 4. Workspace virtual environments (.venv, venv)
    this.discoverWorkspaceVenv(candidates);

    // 5. Platform-native launchers (e.g. Windows py)
    this.discoverPlatformLaunchers(candidates);

    // 6. PATH executables
    this.discoverPathExecutables(candidates);

    // 7. Conservative known locations
    this.discoverKnownLocations(candidates);

    return this.deduplicateCandidates(candidates);
  }

  /**
   * Narrow, bounded candidates for synchronous fallback.
   * PROHIBITION:
   * - Does NOT perform broad filesystem searches
   * - Does NOT perform where/which crawling
   * - Does NOT perform C++ probing
   * - Does NOT perform VS Code extension API calls
   * - Does NOT crawl multiple known directories across disks
   *
   * Only checks immediate high-probability locations:
   * 1. Explicitly configured path (offcode.pythonPath / chup.pythonPath)
   * 2. Active virtual environment (VIRTUAL_ENV / CONDA_PREFIX)
   * 3. Workspace .venv / venv immediate paths
   * 4. Platform default executable (py -3 on Windows, python3 on POSIX)
   */
  public discoverImmediateCandidates(): PythonCandidate[] {
    const candidates: PythonCandidate[] = [];

    // 1. Explicit configuration
    if (this.configuredPath && this.configuredPath.trim().length > 0) {
      candidates.push({
        executable: this.normalizePath(this.configuredPath.trim()),
        args: [],
        source: "configured",
        description: "Explicitly configured offcode.pythonPath / chup.pythonPath"
      });
    }

    // 2. Active virtual environment (VIRTUAL_ENV, CONDA_PREFIX)
    this.discoverActiveEnvironment(candidates);

    // 3. Workspace virtual environments (.venv, venv)
    this.discoverWorkspaceVenv(candidates);

    // 4. Single immediate platform default
    if (this.platform === "win32") {
      candidates.push({
        executable: "py",
        args: ["-3"],
        source: "windows-launcher",
        description: "Immediate Windows Launcher (py -3)"
      });
    } else {
      candidates.push({
        executable: "python3",
        args: [],
        source: "path",
        description: "Immediate PATH executable (python3)"
      });
    }

    return this.deduplicateCandidates(candidates);
  }

  private normalizePath(p: string): string {
    return path.normalize(p);
  }

  private fileExists(filePath: string): boolean {
    try {
      return this.fs.existsSync(filePath);
    } catch {
      return false;
    }
  }

  private discoverActiveEnvironment(candidates: PythonCandidate[]): void {
    const isWindows = this.platform === "win32";

    // VIRTUAL_ENV
    const venv = this.env["VIRTUAL_ENV"];
    if (venv && venv.trim().length > 0) {
      const venvCandidates = isWindows
        ? [
            path.join(venv, "Scripts", "python.exe"),
            path.join(venv, "python.exe")
          ]
        : [
            path.join(venv, "bin", "python3"),
            path.join(venv, "bin", "python")
          ];

      for (const p of venvCandidates) {
        if (this.fileExists(p)) {
          candidates.push({
            executable: this.normalizePath(p),
            args: [],
            source: "virtual-environment",
            description: "Active VIRTUAL_ENV"
          });
          break;
        }
      }
    }

    // CONDA_PREFIX
    const conda = this.env["CONDA_PREFIX"];
    if (conda && conda.trim().length > 0) {
      const condaCandidates = isWindows
        ? [path.join(conda, "python.exe")]
        : [
            path.join(conda, "bin", "python"),
            path.join(conda, "bin", "python3")
          ];

      for (const p of condaCandidates) {
        if (this.fileExists(p)) {
          candidates.push({
            executable: this.normalizePath(p),
            args: [],
            source: "conda",
            description: "Active CONDA_PREFIX"
          });
          break;
        }
      }
    }
  }

  private discoverWorkspaceVenv(candidates: PythonCandidate[]): void {
    const isWindows = this.platform === "win32";
    const venvDirs = [".venv", "venv"];

    const searchRoots: string[] = [];
    if (this.projectRoot) {
      searchRoots.push(this.projectRoot);
    }
    const cwd = process.cwd();
    if (cwd && !searchRoots.includes(cwd)) {
      searchRoots.push(cwd);
    }

    try {
      // eslint-disable-next-line @typescript-eslint/no-var-requires
      const vscode = require("vscode");
      if (vscode && vscode.workspace && Array.isArray(vscode.workspace.workspaceFolders)) {
        for (const wf of vscode.workspace.workspaceFolders) {
          const p = wf.uri?.fsPath;
          if (p && !searchRoots.includes(p)) {
            searchRoots.push(p);
          }
        }
      }
    } catch (_) {}

    for (const root of searchRoots) {
      for (const venvName of venvDirs) {
        const dir = path.join(root, venvName);
        const possible = isWindows
          ? [
              path.join(dir, "Scripts", "python.exe"),
              path.join(dir, "python.exe")
            ]
          : [
              path.join(dir, "bin", "python3"),
              path.join(dir, "bin", "python")
            ];

        for (const p of possible) {
          if (this.fileExists(p)) {
            candidates.push({
              executable: this.normalizePath(p),
              args: [],
              source: "virtual-environment",
              description: `Workspace virtual environment (${venvName})`
            });
            break;
          }
        }
      }
    }
  }

  private discoverPlatformLaunchers(candidates: PythonCandidate[]): void {
    if (this.platform === "win32") {
      // Windows Python Launcher 'py'
      candidates.push({
        executable: "py",
        args: ["-3"],
        source: "windows-launcher",
        description: "Windows Python Launcher (py -3)"
      });
      candidates.push({
        executable: "py",
        args: [],
        source: "windows-launcher",
        description: "Windows Python Launcher (py)"
      });
    }
  }

  private discoverPathExecutables(candidates: PythonCandidate[]): void {
    if (this.platform === "win32") {
      candidates.push({
        executable: "python.exe",
        args: [],
        source: "path",
        description: "PATH executable (python.exe)"
      });
      candidates.push({
        executable: "python3.exe",
        args: [],
        source: "path",
        description: "PATH executable (python3.exe)"
      });
      candidates.push({
        executable: "python",
        args: [],
        source: "path",
        description: "PATH executable (python)"
      });
    } else {
      candidates.push({
        executable: "python3",
        args: [],
        source: "path",
        description: "PATH executable (python3)"
      });
      candidates.push({
        executable: "python",
        args: [],
        source: "path",
        description: "PATH executable (python)"
      });
    }
  }

  private discoverKnownLocations(candidates: PythonCandidate[]): void {
    const isWindows = this.platform === "win32";
    const isMac = this.platform === "darwin";

    if (isWindows) {
      const knownWindows: string[] = [];
      const versions = ["313", "312", "311", "310", "39", "38"];

      // Root drive installations (e.g. C:\Python312\python.exe)
      for (const v of versions) {
        knownWindows.push(`C:\\Python${v}\\python.exe`);
      }

      // Local AppData installations
      const localAppData = this.env["LOCALAPPDATA"];
      if (localAppData) {
        for (const v of versions) {
          knownWindows.push(
            path.join(localAppData, "Programs", "Python", `Python${v}`, "python.exe")
          );
        }
      }

      // Program Files installations
      const progFiles = this.env["ProgramFiles"];
      if (progFiles) {
        for (const v of versions) {
          knownWindows.push(
            path.join(progFiles, `Python${v}`, "python.exe")
          );
          knownWindows.push(
            path.join(progFiles, "Python", `Python${v}`, "python.exe")
          );
        }
      }

      // UserProfile Anaconda / Miniconda
      const userProfile = this.env["USERPROFILE"];
      if (userProfile) {
        knownWindows.push(path.join(userProfile, "anaconda3", "python.exe"));
        knownWindows.push(path.join(userProfile, "miniconda3", "python.exe"));
      }

      for (const p of knownWindows) {
        if (this.fileExists(p)) {
          candidates.push({
            executable: this.normalizePath(p),
            args: [],
            source: "known-location",
            description: `Standard Windows location: ${p}`
          });
        }
      }
    } else if (isMac) {
      const knownMac = [
        "/opt/homebrew/bin/python3",
        "/opt/homebrew/bin/python",
        "/usr/local/bin/python3",
        "/usr/local/bin/python",
        "/usr/bin/python3"
      ];

      const home = this.env["HOME"];
      if (home) {
        knownMac.push(path.join(home, ".pyenv", "shims", "python3"));
        knownMac.push(path.join(home, "miniconda3", "bin", "python3"));
        knownMac.push(path.join(home, "anaconda3", "bin", "python3"));
      }

      for (const p of knownMac) {
        if (this.fileExists(p)) {
          candidates.push({
            executable: this.normalizePath(p),
            args: [],
            source: "known-location",
            description: `Standard macOS location: ${p}`
          });
        }
      }
    } else {
      // Linux
      const knownLinux = [
        "/usr/bin/python3",
        "/usr/local/bin/python3",
        "/opt/python3/bin/python3",
        "/usr/bin/python"
      ];

      const home = this.env["HOME"];
      if (home) {
        knownLinux.push(path.join(home, ".pyenv", "shims", "python3"));
        knownLinux.push(path.join(home, "miniconda3", "bin", "python3"));
        knownLinux.push(path.join(home, "anaconda3", "bin", "python3"));
      }

      for (const p of knownLinux) {
        if (this.fileExists(p)) {
          candidates.push({
            executable: this.normalizePath(p),
            args: [],
            source: "known-location",
            description: `Standard Linux location: ${p}`
          });
        }
      }
    }
  }

  private deduplicateCandidates(candidates: PythonCandidate[]): PythonCandidate[] {
    const seen = new Set<string>();
    const result: PythonCandidate[] = [];

    for (const c of candidates) {
      // Key is executable + args
      const key = `${c.executable.toLowerCase()}::${c.args.join(" ")}`;
      if (!seen.has(key)) {
        seen.add(key);
        result.push(c);
      }
    }

    return result;
  }
}

/**
 * Concrete contract for resolving VS Code Python interpreter.
 * Inspects python.defaultInterpreterPath configuration and ms-python.python extension API.
 * CHUP does NOT declare a hard dependency on ms-python.python; if absent or unavailable,
 * returns undefined and discovery falls through to standard precedence tiers.
 */
export function resolveVsCodePythonInterpreter(): string | undefined {
  try {
    // Dynamically require vscode to remain decoupled in non-extension environments (e.g. tests)
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const vscode = require("vscode");
    if (vscode && vscode.workspace) {
      // 1. Inspect python.defaultInterpreterPath
      const pythonConfig = vscode.workspace.getConfiguration("python");
      const rawDefault = pythonConfig?.get ? (pythonConfig.get("defaultInterpreterPath") as string | undefined) : undefined;
      const defaultInterpreter = typeof rawDefault === "string" ? rawDefault.trim() : undefined;
      if (defaultInterpreter && defaultInterpreter !== "python" && defaultInterpreter.length > 0) {
        return defaultInterpreter;
      }

      // 2. Query documented ms-python.python environments API if available
      const pythonExt = vscode.extensions?.getExtension("ms-python.python");
      if (pythonExt && pythonExt.exports?.environments) {
        const activeEnv = pythonExt.exports.environments.getActiveEnvironmentPath?.();
        if (activeEnv?.path && typeof activeEnv.path === "string" && activeEnv.path.trim().length > 0) {
          return activeEnv.path.trim();
        }
      }
    }
  } catch (_) {
    // Non-fatal: extension host not running or vscode API unavailable
  }
  return undefined;
}
