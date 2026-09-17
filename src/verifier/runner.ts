import { spawnSync } from 'child_process';

export interface ExecutionResult {
  success: boolean;
  exitCode: number;
  stdout: string;
  stderr: string;
  timedOut: boolean;
}

export function executeProgram(binaryPath: string, stdin: string, timeoutMs: number = 5000): ExecutionResult {
  const result = spawnSync(binaryPath, [], {
    input: stdin,
    timeout: timeoutMs,
    encoding: 'utf-8'
  });

  const timedOut = result.error && (result.error as any).code === 'ETIMEDOUT';
  
  return {
    success: result.status === 0,
    exitCode: result.status ?? 1,
    stdout: result.stdout || '',
    stderr: result.stderr || '',
    timedOut: !!timedOut
  };
}
