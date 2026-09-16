/**
 * Python Bridge for CodeForge.
 * Spawns the local Python NLP parser process and communicates via JSON over stdin/stdout.
 */

import { spawn } from "child_process";
import * as path from "path";
import * as fs from "fs";
import { ProblemSpec } from "../models/problemSpec";

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
    this.timeoutMs = options?.timeoutMs || 5000;
  }

  /**
   * Detects the Python interpreter path, prioritizing workspace virtualenv.
   */
  private detectPythonPath(): string {
    const cwd = process.cwd();
    const candidatePaths = [
      path.join(cwd, ".venv", "bin", "python3"),
      path.join(cwd, ".venv", "bin", "python"),
      path.join(__dirname, "..", "..", ".venv", "bin", "python3"),
      path.join(__dirname, "..", "..", ".venv", "bin", "python")
    ];

    for (const p of candidatePaths) {
      if (fs.existsSync(p)) {
        return p;
      }
    }

    return "python3";
  }

  /**
   * Detects the path to python_parser/parser.py.
   */
  private detectParserScriptPath(): string {
    const cwd = process.cwd();
    const candidatePaths = [
      path.join(cwd, "python_parser", "parser.py"),
      path.join(__dirname, "..", "..", "python_parser", "parser.py")
    ];

    for (const p of candidatePaths) {
      if (fs.existsSync(p)) {
        return p;
      }
    }

    // Default fallback
    return path.join(cwd, "python_parser", "parser.py");
  }

  /**
   * Sends a natural-language query to the Python parser over stdin/stdout.
   */
  public async parseQuery(query: string): Promise<ProblemSpec> {
    return new Promise((resolve) => {
      const child = spawn(this.pythonPath, [this.parserScriptPath], {
        stdio: ["pipe", "pipe", "pipe"]
      });

      let stdoutData = "";
      let stderrData = "";
      let timer: NodeJS.Timeout | null = null;
      let finished = false;

      const cleanup = () => {
        if (timer) {
          clearTimeout(timer);
          timer = null;
        }
      };

      timer = setTimeout(() => {
        if (!finished) {
          finished = true;
          child.kill();
          resolve({
            status: "ambiguous",
            language: "cpp",
            confidence: 0.0,
            confidence_basis: "ambiguous",
            error_code: "PARSER_TIMEOUT",
            message: `Python parser process timed out after ${this.timeoutMs}ms.`,
            raw_query: query
          });
        }
      }, this.timeoutMs);

      child.stdout.on("data", (chunk) => {
        stdoutData += chunk.toString();
      });

      child.stderr.on("data", (chunk) => {
        stderrData += chunk.toString();
      });

      child.on("error", (err) => {
        if (finished) return;
        finished = true;
        cleanup();
        resolve({
          status: "ambiguous",
          language: "cpp",
          confidence: 0.0,
          confidence_basis: "ambiguous",
          error_code: "PROCESS_SPAWN_ERROR",
          message: `Failed to spawn Python process (${this.pythonPath}): ${err.message}`,
          raw_query: query
        });
      });

      child.on("close", (code) => {
        if (finished) return;
        finished = true;
        cleanup();

        if (code !== 0 && !stdoutData.trim()) {
          resolve({
            status: "ambiguous",
            language: "cpp",
            confidence: 0.0,
            confidence_basis: "ambiguous",
            error_code: "PROCESS_EXIT_ERROR",
            message: `Python parser exited with code ${code}. Stderr: ${stderrData.trim()}`,
            raw_query: query
          });
          return;
        }

        try {
          const parsed = JSON.parse(stdoutData.trim()) as ProblemSpec;
          resolve(parsed);
        } catch (parseError) {
          resolve({
            status: "ambiguous",
            language: "cpp",
            confidence: 0.0,
            confidence_basis: "ambiguous",
            error_code: "JSON_PARSE_ERROR",
            message: `Failed to parse JSON output from Python parser: ${(parseError as Error).message}. Raw output: ${stdoutData}`,
            raw_query: query
          });
        }
      });

      // Send payload via stdin
      try {
        child.stdin.write(JSON.stringify({ query }) + "\n");
        child.stdin.end();
      } catch (err) {
        if (!finished) {
          finished = true;
          cleanup();
          resolve({
            status: "ambiguous",
            language: "cpp",
            confidence: 0.0,
            confidence_basis: "ambiguous",
            error_code: "STDIN_WRITE_ERROR",
            message: `Error writing to Python process stdin: ${(err as Error).message}`,
            raw_query: query
          });
        }
      }
    });
  }
}
