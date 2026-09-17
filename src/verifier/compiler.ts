import { execSync } from 'child_process';

export interface CompilationResult {
  success: boolean;
  exitCode: number;
  warnings: string[];
  errors: string[];
  outputPath: string;
}

export function compileCpp(sourcePath: string, outputPath: string): CompilationResult {
  try {
    execSync(`g++ -std=c++17 -Wall -Wextra -pedantic "${sourcePath}" -o "${outputPath}"`, { stdio: 'pipe' });
    return {
      success: true,
      exitCode: 0,
      warnings: [],
      errors: [],
      outputPath
    };
  } catch (error: any) {
    const stderr = error.stderr ? error.stderr.toString() : '';
    return {
      success: false,
      exitCode: error.status || 1,
      warnings: [],
      errors: stderr.split('\n').filter((l: string) => l.trim().length > 0),
      outputPath
    };
  }
}
