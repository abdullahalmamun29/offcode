/**
 * Deterministic Python Candidate Validator.
 *
 * Validates a Python candidate through direct process execution:
 * 1. Checks basic interpreter health (sys, json).
 * 2. Extracts exact version (sys.version_info) and enforces the supported version policy.
 * 3. Identifies the concrete interpreter executable (sys.executable) for launchers such as 'py -3'.
 * 4. Performs CHUP bootstrap verification (imports python_parser, pointer_algorithms, architecture_v2).
 * 5. Isolates environment: passes projectRoot in PYTHONPATH without modifying the host process.env.
 */

import * as path from "path";
import {
  PythonCandidate,
  PythonRuntime,
  CandidateValidationResult,
  RuntimeStatus
} from "./types";
import {
  parsePythonVersion,
  isVersionSupported,
  formatVersionRejectionMessage,
  SUPPORTED_RANGE_DESCRIPTION
} from "./versionPolicy";
import {
  IProcessExecutor,
  NodeProcessExecutor,
  ProcessExecutionOptions
} from "./processExecutor";
import { detectProjectRoot } from "./projectRoot";

export const PYTHON_VALIDATION_SCRIPT = `
import sys
import os
import json

result = {
    "sanity": True,
    "major": sys.version_info.major,
    "minor": sys.version_info.minor,
    "micro": sys.version_info.micro,
    "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
    "concrete_executable": sys.executable,
    "bootstrap_ok": True,
    "bootstrap_error": None
}

# If a project root was passed as argv[1], verify that it exists and CHUP modules import
if len(sys.argv) > 1 and sys.argv[1]:
    root = sys.argv[1]
    if root not in sys.path:
        sys.path.insert(0, root)

    try:
        import python_parser
        import pointer_algorithms
        import architecture_v2
    except Exception as e:
        result["bootstrap_ok"] = False
        result["bootstrap_error"] = f"{type(e).__name__}: {str(e)}"

print(json.dumps(result))
`.trim();

export interface ValidatorOptions {
  executor?: IProcessExecutor;
  projectRoot?: string;
  platform?: NodeJS.Platform;
  timeoutMs?: number;
}

export class PythonValidator {
  private executor: IProcessExecutor;
  private projectRoot: string;
  private platform: NodeJS.Platform;
  private timeoutMs: number;

  constructor(options?: ValidatorOptions) {
    this.executor = options?.executor || new NodeProcessExecutor();
    this.projectRoot = detectProjectRoot(options?.projectRoot);
    this.platform = options?.platform || process.platform;
    this.timeoutMs = options?.timeoutMs || 5000;
  }

  private buildExecutionOptions(): ProcessExecutionOptions {
    const existingPythonPath = process.env["PYTHONPATH"];
    const delimiter = this.platform === "win32" ? ";" : ":";
    const combinedPythonPath =
      existingPythonPath && existingPythonPath.trim().length > 0
        ? `${this.projectRoot}${delimiter}${existingPythonPath.trim()}`
        : this.projectRoot;

    return {
      cwd: this.projectRoot,
      env: {
        ...process.env,
        PYTHONPATH: combinedPythonPath,
        PYTHONDONTWRITEBYTECODE: "1"
      },
      timeout: this.timeoutMs
    };
  }

  public async validateCandidate(
    candidate: PythonCandidate
  ): Promise<CandidateValidationResult> {
    const execOptions = this.buildExecutionOptions();
    const args = [
      ...candidate.args,
      "-c",
      PYTHON_VALIDATION_SCRIPT,
      this.projectRoot
    ];

    const result = await this.executor.execFile(
      candidate.executable,
      args,
      execOptions
    );

    return this.parseValidationOutput(candidate, result);
  }

  public validateCandidateSync(
    candidate: PythonCandidate
  ): CandidateValidationResult {
    const execOptions = this.buildExecutionOptions();
    const args = [
      ...candidate.args,
      "-c",
      PYTHON_VALIDATION_SCRIPT,
      this.projectRoot
    ];

    const result = this.executor.execFileSync(
      candidate.executable,
      args,
      execOptions
    );

    return this.parseValidationOutput(candidate, result);
  }

  private parseValidationOutput(
    candidate: PythonCandidate,
    result: { stdout: string; stderr: string; exitCode: number; timedOut: boolean; error?: Error }
  ): CandidateValidationResult {
    const invocationLabel =
      candidate.args.length > 0
        ? `${candidate.executable} ${candidate.args.join(" ")}`
        : candidate.executable;

    if (result.timedOut) {
      return {
        valid: false,
        status: "PYTHON_INVALID",
        error: `Python candidate timed out after ${this.timeoutMs}ms: ${invocationLabel}`
      };
    }

    if (result.exitCode !== 0 && !result.stdout.trim()) {
      return {
        valid: false,
        status: "PYTHON_INVALID",
        error: `Failed to execute ${invocationLabel} (exit code ${result.exitCode}): ${result.stderr.trim() || "No error details available."}`
      };
    }

    let payload: any;
    try {
      const trimmed = result.stdout.trim();
      const lastLine = trimmed.split("\n").filter((l) => l.trim().length > 0).pop() || "";
      payload = JSON.parse(lastLine);
    } catch (parseErr) {
      return {
        valid: false,
        status: "PYTHON_INVALID",
        error: `Malformed JSON response from ${invocationLabel}: ${result.stdout.trim() || result.stderr.trim()}`,
        rawOutput: result.stdout
      };
    }

    const major = payload.major;
    const minor = payload.minor;
    const patch = payload.micro ?? 0;
    const versionStr = payload.version || `${major}.${minor}.${patch}`;
    const concreteExecutable = payload.concrete_executable || candidate.executable;

    // 1. Version enforcement
    if (!isVersionSupported(major, minor)) {
      return {
        valid: false,
        status: "PYTHON_VERSION_UNSUPPORTED",
        error: formatVersionRejectionMessage(versionStr, invocationLabel)
      };
    }

    // 2. Bootstrap check
    if (payload.bootstrap_ok === false) {
      return {
        valid: false,
        status: "PYTHON_BOOTSTRAP_FAILED",
        error: `CHUP Python component bootstrap failed on ${invocationLabel}: ${payload.bootstrap_error || "Unknown import error"}`,
        bootstrapOk: false,
        bootstrapError: payload.bootstrap_error
      };
    }

    const runtime: PythonRuntime = {
      executable: candidate.executable,
      args: [...candidate.args],
      concreteExecutable,
      version: versionStr,
      major,
      minor,
      patch,
      platform: this.platform,
      source: candidate.source
    };

    return {
      valid: true,
      runtime,
      status: "READY",
      bootstrapOk: true
    };
  }
}
