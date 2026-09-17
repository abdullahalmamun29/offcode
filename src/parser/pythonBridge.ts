/**
 * Python Bridge for CodeForge V1.
 * Spawns the local Python NLP parser and communicates via JSON over stdin/stdout.
 * Constructs ProblemSpecV1 from the flat Python parser output.
 */

import { spawn } from "child_process";
import * as path from "path";
import * as fs from "fs";
import { ProblemSpecV1, ConfidenceBasis } from "../models/problemSpec";

export interface PythonBridgeOptions {
  pythonPath?: string;
  parserScriptPath?: string;
  timeoutMs?: number;
}

export class PythonBridge {
  private pythonPath: string;
  private parserScriptPath: string;
  private timeoutMs: number;

  constructor(options?: PythonBridgeOptions) {
    this.pythonPath = options?.pythonPath || this.detectPythonPath();
    this.parserScriptPath = options?.parserScriptPath || this.detectParserScriptPath();
    this.timeoutMs = options?.timeoutMs || 10000;
  }

  private detectPythonPath(): string {
    const cwd = process.cwd();
    const candidatePaths = [
      path.join(cwd, ".venv", "bin", "python3"),
      path.join(cwd, ".venv", "bin", "python"),
      path.join(__dirname, "..", "..", ".venv", "bin", "python3"),
      path.join(__dirname, "..", "..", ".venv", "bin", "python")
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) { return p; }
    }
    return "python3";
  }

  private detectParserScriptPath(): string {
    const cwd = process.cwd();
    const candidatePaths = [
      path.join(cwd, "python_parser", "parser.py"),
      path.join(__dirname, "..", "..", "python_parser", "parser.py")
    ];
    for (const p of candidatePaths) {
      if (fs.existsSync(p)) { return p; }
    }
    return path.join(cwd, "python_parser", "parser.py");
  }

  public async parseQuery(query: string): Promise<ProblemSpecV1> {
    const flat = await this.rawParse(query);
    return this.constructProblemSpecV1(flat, query);
  }

  private async rawParse(query: string): Promise<any> {
    return new Promise((resolve) => {
      const child = spawn(this.pythonPath, [this.parserScriptPath], {
        stdio: ["pipe", "pipe", "pipe"]
      });

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
            status: "ambiguous", language: "cpp", domain: "data_structure",
            intent: "ambiguous", confidence: 0, confidence_basis: "ambiguous",
            error_code: "PARSER_TIMEOUT",
            message: `Python parser timed out after ${this.timeoutMs}ms.`,
            raw_query: query, normalized_query: ""
          });
        }
      }, this.timeoutMs);

      child.stdout.on("data", (chunk) => { stdoutData += chunk.toString(); });
      child.stderr.on("data", (chunk) => { stderrData += chunk.toString(); });

      child.on("error", (err) => {
        if (finished) return;
        finished = true; cleanup();
        resolve({
          status: "ambiguous", language: "cpp", domain: "data_structure",
          intent: "ambiguous", confidence: 0, confidence_basis: "ambiguous",
          error_code: "PROCESS_SPAWN_ERROR",
          message: `Failed to spawn Python process: ${err.message}`,
          raw_query: query, normalized_query: ""
        });
      });

      child.on("close", (code) => {
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
