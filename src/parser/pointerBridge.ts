/**
 * Pointer Bridge for CHUP.
 *
 * Spawns the authoritative Python Pointer-Based Algorithms reasoning engine
 * (pointer_algorithms/bridge.py) and communicates via JSON over stdin/stdout.
 */

import { spawn } from "child_process";
import * as path from "path";
import * as fs from "fs";
import { PointerReasoningResult } from "../models/problemSpec";
import { ExplanationDocument } from "../models/explanationModel";
import { PythonRuntimeManager } from "../runtime/pythonRuntimeManager";
import { PythonRuntime } from "../runtime/types";

export interface PointerBridgeOptions {
  pythonPath?: string;
  runtimeManager?: PythonRuntimeManager;
  bridgeScriptPath?: string;
  timeoutMs?: number;
}

export class PointerBridge {
  private explicitPythonPath?: string;
  private runtimeManager?: PythonRuntimeManager;
  private bridgeScriptPath: string;
  private timeoutMs: number;

  constructor(options?: PointerBridgeOptions) {
    this.explicitPythonPath = options?.pythonPath;
    this.runtimeManager = options?.runtimeManager;
    this.bridgeScriptPath = options?.bridgeScriptPath || this.detectBridgeScriptPath();
    this.timeoutMs = options?.timeoutMs || 10000;
  }

  private detectProjectRoot(): string {
    const cwd = process.cwd();
    const candidateDirs = [
      cwd,
      path.join(__dirname, "..", ".."),
      path.join(__dirname, "..")
    ];
    for (const d of candidateDirs) {
      if (fs.existsSync(path.join(d, "pointer_algorithms", "bridge.py"))) {
        return d;
      }
    }
    return cwd;
  }

  private detectBridgeScriptPath(): string {
    const cwd = process.cwd();
    const candidatePaths = [
      path.join(cwd, "pointer_algorithms", "bridge.py"),
      path.join(__dirname, "..", "..", "pointer_algorithms", "bridge.py"),
      path.join(__dirname, "..", "pointer_algorithms", "bridge.py")
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) return p;
    }
    return path.join(__dirname, "..", "..", "pointer_algorithms", "bridge.py");
  }

  public async evaluateProblem(problemText: string, isRetry = false): Promise<any> {
    return new Promise(async (resolve) => {
      let executable: string;
      let args: string[];
      let runtimeObj: any = null;
      const manager = this.runtimeManager || PythonRuntimeManager.getInstance();

      if (this.explicitPythonPath) {
        executable = this.explicitPythonPath;
        args = [this.bridgeScriptPath];
      } else {
        try {
          const runtime = await manager.resolveRuntime();
          runtimeObj = runtime;
          // Invariant: downstream child-process execution consumes concreteExecutable
          executable = runtime.concreteExecutable || runtime.executable;
          args = runtime.concreteExecutable
            ? [this.bridgeScriptPath]
            : [...runtime.args, this.bridgeScriptPath];
        } catch (runtimeErr: any) {
          return resolve({
            status: "error",
            domain: "pointer_algorithms",
            selectedPattern: null,
            family: null,
            reasoning: `Python pointer bridge runtime unavailable: ${runtimeErr.message}`
          });
        }
      }

      const projectRoot = this.detectProjectRoot();
      const delimiter = process.platform === "win32" ? ";" : ":";
      const existingPythonPath = process.env.PYTHONPATH;
      const combinedPythonPath =
        existingPythonPath && existingPythonPath.trim().length > 0
          ? `${projectRoot}${delimiter}${existingPythonPath.trim()}`
          : projectRoot;

      const handleSpawnFailure = async (err: any) => {
        if (!isRetry && runtimeObj && err?.code === "ENOENT") {
          manager.invalidateRuntime(runtimeObj);
          try {
            const retryResult = await this.evaluateProblem(problemText, true);
            return resolve(retryResult);
          } catch (_) {}
        }
        return resolve({
          status: "error",
          domain: "pointer_algorithms",
          selectedPattern: null,
          family: null,
          reasoning: `Python pointer bridge spawn error: ${err.message}`
        });
      };

      let child: any;
      try {
        child = spawn(executable, args, {
          cwd: projectRoot,
          env: {
            ...process.env,
            PYTHONPATH: combinedPythonPath,
            PYTHONDONTWRITEBYTECODE: "1"
          },
          shell: false,
          stdio: ["pipe", "pipe", "pipe"]
        });
      } catch (spawnErr: any) {
        return handleSpawnFailure(spawnErr);
      }

      let stdoutData = "";
      let stderrData = "";
      let finished = false;

      const timer = setTimeout(() => {
        if (!finished) {
          finished = true;
          child.kill();
          resolve({
            status: "error",
            domain: "pointer_algorithms",
            selectedPattern: null,
            family: null,
            reasoning: `Python pointer bridge timed out after ${this.timeoutMs}ms.`
          });
        }
      }, this.timeoutMs);

      child.stdout.on("data", (chunk: any) => { stdoutData += chunk.toString(); });
      child.stderr.on("data", (chunk: any) => { stderrData += chunk.toString(); });

      child.on("error", (err: any) => {
        if (finished) return;
        finished = true;
        clearTimeout(timer);
        resolve({
          status: "error",
          domain: "pointer_algorithms",
          selectedPattern: null,
          family: null,
          reasoning: `Python pointer bridge spawn error: ${err.message}`
        });
      });

      child.on("close", (code: number) => {
        if (finished) return;
        finished = true;
        clearTimeout(timer);

        try {
          const result = JSON.parse(stdoutData);
          resolve(result);
        } catch (e) {
          resolve({
            status: "error",
            domain: "pointer_algorithms",
            selectedPattern: null,
            family: null,
            reasoning: `Failed to parse Python pointer bridge output: ${stdoutData || stderrData}`
          });
        }
      });

      // Send payload
      try {
        child.stdin.write(JSON.stringify({ action: "solve", problemText }));
        child.stdin.end();
      } catch (err: any) {
        if (!finished) {
          finished = true;
          clearTimeout(timer);
          resolve({
            status: "error",
            domain: "pointer_algorithms",
            selectedPattern: null,
            family: null,
            reasoning: `Python pointer bridge stdin error: ${err.message}`
          });
        }
      }
    });
  }

  public evaluateProblemSync(problemText: string, isRetry = false): PointerReasoningResult {
    const { execFileSync } = require("child_process");
    let executable: string;
    let args: string[];
    let runtimeObj: any = null;
    const manager = this.runtimeManager || PythonRuntimeManager.getInstance();

    if (this.explicitPythonPath) {
      executable = this.explicitPythonPath;
      args = [this.bridgeScriptPath];
    } else {
      try {
        const runtime = manager.resolveRuntimeSync();
        runtimeObj = runtime;
        // Invariant: downstream child-process execution consumes concreteExecutable
        executable = runtime.concreteExecutable || runtime.executable;
        args = runtime.concreteExecutable
          ? [this.bridgeScriptPath]
          : [...runtime.args, this.bridgeScriptPath];
      } catch (runtimeErr: any) {
        return {
          status: "error",
          domain: "pointer_algorithms",
          selectedPattern: null,
          family: null,
          reasoning: `Python pointer bridge runtime unavailable: ${runtimeErr.message}`
        };
      }
    }

    const projectRoot = this.detectProjectRoot();
    const delimiter = process.platform === "win32" ? ";" : ":";
    const existingPythonPath = process.env.PYTHONPATH;
    const combinedPythonPath =
      existingPythonPath && existingPythonPath.trim().length > 0
        ? `${projectRoot}${delimiter}${existingPythonPath.trim()}`
        : projectRoot;

    try {
      const stdout = execFileSync(executable, args, {
        cwd: projectRoot,
        env: {
          ...process.env,
          PYTHONPATH: combinedPythonPath,
          PYTHONDONTWRITEBYTECODE: "1"
        },
        input: JSON.stringify({ action: "solve", problemText }),
        encoding: "utf-8",
        timeout: this.timeoutMs,
        shell: false,
        stdio: ["pipe", "pipe", "pipe"]
      });
      return JSON.parse(stdout);
    } catch (e: any) {
      if (!isRetry && runtimeObj && e?.code === "ENOENT") {
        manager.invalidateRuntime(runtimeObj);
        try {
          return this.evaluateProblemSync(problemText, true);
        } catch (_) {}
      }
      return {
        status: "error",
        domain: "pointer_algorithms",
        selectedPattern: null,
        family: null,
        reasoning: `Sync execution error: ${e.message}`
      };
    }
  }

  public explainProblemSync(problemText: string, level = "DETAILED"): { status: string; explanation?: ExplanationDocument; markdown?: string; error?: string } {
    const { execFileSync } = require("child_process");
    let executable: string;
    let args: string[];
    const manager = this.runtimeManager || PythonRuntimeManager.getInstance();

    if (this.explicitPythonPath) {
      executable = this.explicitPythonPath;
      args = [this.bridgeScriptPath];
    } else {
      try {
        const runtime = manager.resolveRuntimeSync();
        executable = runtime.concreteExecutable || runtime.executable;
        args = runtime.concreteExecutable
          ? [this.bridgeScriptPath]
          : [...runtime.args, this.bridgeScriptPath];
      } catch (runtimeErr: any) {
        return {
          status: "error",
          error: `Python pointer bridge runtime unavailable: ${runtimeErr.message}`
        };
      }
    }

    const projectRoot = this.detectProjectRoot();
    const delimiter = process.platform === "win32" ? ";" : ":";
    const existingPythonPath = process.env.PYTHONPATH;
    const combinedPythonPath =
      existingPythonPath && existingPythonPath.trim().length > 0
        ? `${projectRoot}${delimiter}${existingPythonPath.trim()}`
        : projectRoot;

    try {
      const stdout = execFileSync(executable, args, {
        cwd: projectRoot,
        env: {
          ...process.env,
          PYTHONPATH: combinedPythonPath,
          PYTHONDONTWRITEBYTECODE: "1"
        },
        input: JSON.stringify({ action: "explain", problemText, level }),
        encoding: "utf-8",
        timeout: this.timeoutMs,
        shell: false,
        stdio: ["pipe", "pipe", "pipe"]
      });
      return JSON.parse(stdout);
    } catch (e: any) {
      return {
        status: "error",
        error: `Sync explanation error: ${e.message}`
      };
    }
  }

  public async explainProblem(problemText: string, level = "DETAILED"): Promise<{ status: string; explanation?: ExplanationDocument; markdown?: string; error?: string }> {
    return new Promise(async (resolve) => {
      let executable: string;
      let args: string[];
      const manager = this.runtimeManager || PythonRuntimeManager.getInstance();

      if (this.explicitPythonPath) {
        executable = this.explicitPythonPath;
        args = [this.bridgeScriptPath];
      } else {
        try {
          const runtime = await manager.resolveRuntime();
          executable = runtime.concreteExecutable || runtime.executable;
          args = runtime.concreteExecutable
            ? [this.bridgeScriptPath]
            : [...runtime.args, this.bridgeScriptPath];
        } catch (runtimeErr: any) {
          return resolve({
            status: "error",
            error: `Python pointer bridge runtime unavailable: ${runtimeErr.message}`
          });
        }
      }

      const projectRoot = this.detectProjectRoot();
      const delimiter = process.platform === "win32" ? ";" : ":";
      const existingPythonPath = process.env.PYTHONPATH;
      const combinedPythonPath =
        existingPythonPath && existingPythonPath.trim().length > 0
          ? `${projectRoot}${delimiter}${existingPythonPath.trim()}`
          : projectRoot;

      const child = spawn(executable, args, {
        cwd: projectRoot,
        env: {
          ...process.env,
          PYTHONPATH: combinedPythonPath,
          PYTHONDONTWRITEBYTECODE: "1"
        },
        stdio: ["pipe", "pipe", "pipe"]
      });

      let stdoutData = "";
      let stderrData = "";
      let finished = false;

      const timer = setTimeout(() => {
        if (!finished) {
          finished = true;
          child.kill();
          resolve({
            status: "error",
            error: `Explanation timed out after ${this.timeoutMs}ms.`
          });
        }
      }, this.timeoutMs);

      child.stdout.on("data", (chunk: any) => { stdoutData += chunk.toString(); });
      child.stderr.on("data", (chunk: any) => { stderrData += chunk.toString(); });

      child.on("error", (err: any) => {
        if (finished) return;
        finished = true;
        clearTimeout(timer);
        resolve({
          status: "error",
          error: `Failed to spawn process: ${err.message}`
        });
      });

      child.on("close", (code: number) => {
        if (finished) return;
        finished = true;
        clearTimeout(timer);
        if (code !== 0 && !stdoutData.trim()) {
          resolve({
            status: "error",
            error: `Process exited with code ${code}. ${stderrData.trim()}`
          });
          return;
        }
        try {
          resolve(JSON.parse(stdoutData.trim()));
        } catch (e: any) {
          resolve({
            status: "error",
            error: `Failed to parse explanation output: ${stdoutData || stderrData}`
          });
        }
      });

      try {
        child.stdin.write(JSON.stringify({ action: "explain", problemText, level }));
        child.stdin.end();
      } catch (err: any) {
        if (!finished) {
          finished = true;
          clearTimeout(timer);
          resolve({
            status: "error",
            error: `Failed to write to stdin: ${err.message}`
          });
        }
      }
    });
  }
}

