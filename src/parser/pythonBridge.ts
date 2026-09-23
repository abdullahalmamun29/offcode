/**
 * Python Bridge for CodeForge V1.
 * Spawns the local Python NLP parser and communicates via JSON over stdin/stdout.
 * Constructs ProblemSpecV1 from the flat Python parser output.
 */

import { spawn } from "child_process";
import * as path from "path";
import * as fs from "fs";
import { ProblemSpecV1, ConfidenceBasis } from "../models/problemSpec";
import { PythonRuntimeManager } from "../runtime/pythonRuntimeManager";
import { PythonRuntime } from "../runtime/types";

export interface PythonBridgeOptions {
  pythonPath?: string;
  runtimeManager?: PythonRuntimeManager;
  parserScriptPath?: string;
  timeoutMs?: number;
}

export class PythonBridge {
  private explicitPythonPath?: string;
  private runtimeManager?: PythonRuntimeManager;
  private parserScriptPath: string;
  private timeoutMs: number;

  constructor(options?: PythonBridgeOptions) {
    this.explicitPythonPath = options?.pythonPath;
    this.runtimeManager = options?.runtimeManager;
    this.parserScriptPath = options?.parserScriptPath || this.detectParserScriptPath();
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
      if (fs.existsSync(path.join(d, "python_parser", "parser.py"))) {
        return d;
      }
    }
    return cwd;
  }

  private detectParserScriptPath(): string {
    const cwd = process.cwd();
    const candidatePaths = [
      path.join(cwd, "python_parser", "parser.py"),
      path.join(__dirname, "..", "..", "python_parser", "parser.py"),
      path.join(__dirname, "..", "python_parser", "parser.py"),
      path.join(__dirname, "python_parser", "parser.py")
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) { return p; }
    }
    return path.join(__dirname, "..", "..", "python_parser", "parser.py");
  }

  public async parseQuery(query: string): Promise<ProblemSpecV1> {
    const flat = await this.rawParse(query);
    return this.constructProblemSpecV1(flat, query);
  }

  private async rawParse(query: string, isRetry = false): Promise<any> {
    return new Promise(async (resolve) => {
      let executable: string;
      let args: string[];
      let runtimeObj: any = null;
      const manager = this.runtimeManager || PythonRuntimeManager.getInstance();

      if (this.explicitPythonPath) {
        executable = this.explicitPythonPath;
        args = [this.parserScriptPath];
      } else {
        try {
          const runtime = await manager.resolveRuntime();
          runtimeObj = runtime;
          // Invariant: downstream child-process execution consumes concreteExecutable
          executable = runtime.concreteExecutable || runtime.executable;
          args = runtime.concreteExecutable
            ? [this.parserScriptPath]
            : [...runtime.args, this.parserScriptPath];
        } catch (runtimeErr: any) {
          return resolve({
            status: "ambiguous",
            language: "cpp",
            domain: "data_structure",
            intent: "ambiguous",
            confidence: 0,
            confidence_basis: "ambiguous",
            error_code: "PYTHON_RUNTIME_UNAVAILABLE",
            message: `Python runtime unavailable: ${runtimeErr.message}`,
            raw_query: query,
            normalized_query: ""
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
            const retryResult = await this.rawParse(query, true);
            return resolve(retryResult);
          } catch (_) {
            // fall through to error resolution
          }
        }
        return resolve({
          status: "ambiguous",
          language: "cpp",
          domain: "data_structure",
          intent: "ambiguous",
          confidence: 0,
          confidence_basis: "ambiguous",
          error_code: "PROCESS_SPAWN_ERROR",
          message: `Failed to spawn Python process: ${err.message}`,
          raw_query: query,
          normalized_query: ""
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
      let timer: NodeJS.Timeout | null = null;
      let finished = false;

      const cleanup = () => {
        if (timer) { clearTimeout(timer); timer = null; }
      };

      timer = setTimeout(() => {
        if (!finished) {
          finished = true;
          child.kill();
          resolve({
            status: "ambiguous",
            language: "cpp",
            domain: "data_structure",
            intent: "ambiguous",
            confidence: 0,
            confidence_basis: "ambiguous",
            error_code: "PARSER_TIMEOUT",
            message: `Python parser timed out after ${this.timeoutMs}ms.`,
            raw_query: query,
            normalized_query: ""
          });
        }
      }, this.timeoutMs);

      child.stdout.on("data", (chunk: any) => { stdoutData += chunk.toString(); });
      child.stderr.on("data", (chunk: any) => { stderrData += chunk.toString(); });

      child.on("error", (err: any) => {
        if (finished) return;
        finished = true;
        cleanup();
        handleSpawnFailure(err);
      });

      child.on("close", (code: number) => {
        if (finished) return;
        finished = true; cleanup();
        if (code !== 0 && !stdoutData.trim()) {
          resolve({
            status: "ambiguous", language: "cpp", domain: "data_structure",
            intent: "ambiguous", confidence: 0, confidence_basis: "ambiguous",
            error_code: "PROCESS_EXIT_ERROR",
            message: `Python parser exited with code ${code}. ${stderrData.trim()}`,
            raw_query: query, normalized_query: ""
          });
          return;
        }
        try {
          resolve(JSON.parse(stdoutData.trim()));
        } catch (parseError) {
          resolve({
            status: "ambiguous", language: "cpp", domain: "data_structure",
            intent: "ambiguous", confidence: 0, confidence_basis: "ambiguous",
            error_code: "JSON_PARSE_ERROR",
            message: `Failed to parse Python output: ${(parseError as Error).message}`,
            raw_query: query, normalized_query: ""
          });
        }
      });

      try {
        child.stdin.write(JSON.stringify({ query }) + "\n");
        child.stdin.end();
      } catch (err) {
        if (!finished) {
          finished = true; cleanup();
          resolve({
            status: "ambiguous", language: "cpp", domain: "data_structure",
            intent: "ambiguous", confidence: 0, confidence_basis: "ambiguous",
            error_code: "STDIN_WRITE_ERROR",
            message: `Error writing to stdin: ${(err as Error).message}`,
            raw_query: query, normalized_query: ""
          });
        }
      }
    });
  }

  private constructProblemSpecV1(flat: any, query: string): ProblemSpecV1 {
    return {
      status: flat.status || "ambiguous",
      language: flat.language || "cpp",
      domain: flat.domain || "data_structure",
      intent: flat.intent || "ambiguous",
      structure: {
        type: flat.structure || null,
        confidence_basis: (flat.confidence_basis as ConfidenceBasis) || "ambiguous",
      },
      operation: {
        action: flat.operation_action || null,
        position: flat.operation_position || null,
        combined: flat.operation || null,
        target_value: flat.target_value ?? null,
        target_index: flat.target_index ?? null,
        negated: flat.operation_negated || false,
      },
      compound: {
        is_compound: flat.is_compound || false,
        detected_actions: flat.detected_actions || [],
        sequencing_marker: flat.sequencing_marker || null,
      },
      numerical: {
        method: flat.numerical_method || null,
        category: flat.numerical_category || null,
      },
      confidence: flat.confidence || 0,
      confidence_basis: (flat.confidence_basis as ConfidenceBasis) || "ambiguous",
      error_code: flat.error_code || null,
      message: flat.message || "",
      raw_query: flat.raw_query || query,
      normalized_query: flat.normalized_query || "",
      generation_mode: flat.generation_mode || "single",
      menu_operations: flat.menu_operations || undefined,
    };
  }
}
