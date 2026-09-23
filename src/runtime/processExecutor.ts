/**
 * Safe, Direct Process Execution Layer for CHUP.
 *
 * Requirements:
 * - Uses direct process APIs (execFile, execFileSync) with argument arrays.
 * - Prohibits shell concatenation or shell execution (shell: false).
 * - Enforces timeouts and kills hung processes.
 * - Captures stdout, stderr, exitCode cleanly without unhandled crashes.
 * - Provides mockable interface for deterministic unit testing.
 */

import * as cp from "child_process";

export interface ProcessExecutionOptions {
  cwd?: string;
  env?: NodeJS.ProcessEnv;
  timeout?: number;
  input?: string;
}

export interface ProcessExecutionResult {
  stdout: string;
  stderr: string;
  exitCode: number;
  timedOut: boolean;
  error?: Error;
}

export interface IProcessExecutor {
  execFile(
    file: string,
    args: string[],
    options?: ProcessExecutionOptions
  ): Promise<ProcessExecutionResult>;

  execFileSync(
    file: string,
    args: string[],
    options?: ProcessExecutionOptions
  ): ProcessExecutionResult;
}

export class NodeProcessExecutor implements IProcessExecutor {
  public async execFile(
    file: string,
    args: string[],
    options?: ProcessExecutionOptions
  ): Promise<ProcessExecutionResult> {
    const timeout = options?.timeout ?? 10000;

    return new Promise((resolve) => {
      let child: cp.ChildProcess;
      let timedOut = false;
      let stdout = "";
      let stderr = "";
      let timer: NodeJS.Timeout | null = null;
      let finished = false;

      const cleanup = () => {
        if (timer) {
          clearTimeout(timer);
          timer = null;
        }
      };

      try {
        child = cp.spawn(file, args, {
          cwd: options?.cwd,
          env: options?.env ?? process.env,
          shell: false,
          stdio: ["pipe", "pipe", "pipe"]
        });
      } catch (err: any) {
        return resolve({
          stdout: "",
          stderr: err.message || String(err),
          exitCode: -1,
          timedOut: false,
          error: err
        });
      }

      timer = setTimeout(() => {
        if (!finished) {
          timedOut = true;
          finished = true;
          try {
            child.kill("SIGKILL");
          } catch (_) {
            // ignore
          }
          resolve({
            stdout,
            stderr: stderr + `\nProcess timed out after ${timeout}ms.`,
            exitCode: -1,
            timedOut: true
          });
        }
      }, timeout);

      if (child.stdout) {
        child.stdout.on("data", (data) => {
          stdout += data.toString();
        });
      }

      if (child.stderr) {
        child.stderr.on("data", (data) => {
          stderr += data.toString();
        });
      }

      child.on("error", (err) => {
        if (finished) return;
        finished = true;
        cleanup();
        resolve({
          stdout,
          stderr: stderr ? `${stderr}\n${err.message}` : err.message,
          exitCode: -1,
          timedOut: false,
          error: err
        });
      });

      child.on("close", (code) => {
        if (finished) return;
        finished = true;
        cleanup();
        resolve({
          stdout,
          stderr,
          exitCode: code ?? 0,
          timedOut: false
        });
      });

      if (options?.input && child.stdin) {
        try {
          child.stdin.write(options.input);
          child.stdin.end();
        } catch (_) {
          // ignore stream error
        }
      } else if (child.stdin) {
        child.stdin.end();
      }
    });
  }

  public execFileSync(
    file: string,
    args: string[],
    options?: ProcessExecutionOptions
  ): ProcessExecutionResult {
    const timeout = options?.timeout ?? 5000;
    try {
      const stdout = cp.execFileSync(file, args, {
        cwd: options?.cwd,
        env: options?.env ?? process.env,
        shell: false,
        timeout,
        input: options?.input,
        encoding: "utf-8",
        stdio: ["pipe", "pipe", "pipe"]
      });

      return {
        stdout: stdout || "",
        stderr: "",
        exitCode: 0,
        timedOut: false
      };
    } catch (err: any) {
      const isTimeout = err.code === "ETIMEDOUT" || err.signal === "SIGTERM";
      return {
        stdout: err.stdout ? err.stdout.toString() : "",
        stderr: err.stderr ? err.stderr.toString() : err.message || "",
        exitCode: err.status !== undefined && err.status !== null ? err.status : -1,
        timedOut: isTimeout,
        error: err
      };
    }
  }
}

/**
 * Mock executor for deterministic tests across platforms.
 */
export type MockExecutionHandler = (
  file: string,
  args: string[],
  options?: ProcessExecutionOptions
) => ProcessExecutionResult | Promise<ProcessExecutionResult>;

export class MockProcessExecutor implements IProcessExecutor {
  private handlers: Array<{
    matcher: (file: string, args: string[]) => boolean;
    handler: MockExecutionHandler;
  }> = [];

  private defaultHandler: MockExecutionHandler = (file) => ({
    stdout: "",
    stderr: `Command not found: ${file}`,
    exitCode: 127,
    timedOut: false
  });

  public onCommand(
    matcher: (file: string, args: string[]) => boolean,
    handler: MockExecutionHandler | ProcessExecutionResult
  ): this {
    const fn: MockExecutionHandler =
      typeof handler === "function" ? handler : () => handler;
    this.handlers.unshift({ matcher, handler: fn });
    return this;
  }

  public onExact(
    file: string,
    args: string[],
    result: ProcessExecutionResult | MockExecutionHandler
  ): this {
    return this.onCommand(
      (f, a) => f === file && JSON.stringify(a) === JSON.stringify(args),
      result
    );
  }

  public setDefault(handler: MockExecutionHandler): this {
    this.defaultHandler = handler;
    return this;
  }

  public async execFile(
    file: string,
    args: string[],
    options?: ProcessExecutionOptions
  ): Promise<ProcessExecutionResult> {
    for (const h of this.handlers) {
      if (h.matcher(file, args)) {
        return await h.handler(file, args, options);
      }
    }
    return await this.defaultHandler(file, args, options);
  }

  public execFileSync(
    file: string,
    args: string[],
    options?: ProcessExecutionOptions
  ): ProcessExecutionResult {
    for (const h of this.handlers) {
      if (h.matcher(file, args)) {
        const res = h.handler(file, args, options);
        if (res instanceof Promise) {
          throw new Error("Cannot execute async mock handler in execFileSync");
        }
        return res;
      }
    }
    const res = this.defaultHandler(file, args, options);
    if (res instanceof Promise) {
      throw new Error("Cannot execute async mock handler in execFileSync");
    }
    return res;
  }
}
