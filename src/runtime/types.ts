/**
 * Authoritative Type Definitions for CHUP Python Runtime Resolution & Environment Management.
 */

export type PythonRuntimeSource =
  | "configured"
  | "vscode"
  | "environment"
  | "windows-launcher"
  | "path"
  | "known-location"
  | "virtual-environment"
  | "conda"
  | "other";

export interface PythonCandidate {
  executable: string;
  args: string[];
  source: PythonRuntimeSource;
  description?: string;
}

export interface PythonRuntime {
  executable: string;
  args: string[];
  concreteExecutable: string;
  version: string;
  major: number;
  minor: number;
  patch: number;
  platform: NodeJS.Platform;
  source: PythonRuntimeSource;
}

export type PythonRuntimeStatus =
  | "READY"
  | "PYTHON_NOT_FOUND"
  | "PYTHON_INVALID"
  | "PYTHON_VERSION_UNSUPPORTED"
  | "PYTHON_BOOTSTRAP_FAILED";

export type CxxToolchainStatus =
  | "READY"
  | "CXX_COMPILER_MISSING"
  | "CXX_PROBE_FAILED";

export type EnvironmentStatus =
  | "READY"
  | "DEGRADED"
  | "BLOCKED";

// Backward-compatible alias for Python runtime status
export type RuntimeStatus = PythonRuntimeStatus;

export interface CandidateValidationResult {
  valid: boolean;
  runtime?: PythonRuntime;
  error?: string;
  status: PythonRuntimeStatus;
  rawOutput?: string;
  bootstrapOk?: boolean;
  bootstrapError?: string;
}

export interface PythonDiagnostic {
  status: PythonRuntimeStatus;
  executable?: string;
  args?: string[];
  concreteExecutable?: string;
  version?: string;
  source?: PythonRuntimeSource;
  testedCandidates: Array<{
    executable: string;
    args: string[];
    source: PythonRuntimeSource;
    error?: string;
  }>;
  errorMessage?: string;
  supportedRange: string;
}

export interface CxxDiagnostic {
  status: CxxToolchainStatus;
  compilerPath?: string;
  compilerVersion?: string;
  errorMessage?: string;
}

export interface EnvironmentReport {
  overallStatus: EnvironmentStatus;
  os: string;
  arch: string;
  python: PythonDiagnostic;
  cxx: CxxDiagnostic;
  vscodeVersion?: string;
  offcodeVersion?: string;
  chupVersion?: string;
}
