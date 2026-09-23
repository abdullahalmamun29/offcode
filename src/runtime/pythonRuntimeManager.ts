/**
 * Authoritative Python Runtime Manager for CHUP.
 *
 * Coordinates candidate discovery, validation, in-memory caching, and structured diagnostics.
 * Adheres to strict architectural contracts:
 * - Direct process execution with argument arrays.
 * - Non-blocking asynchronous resolution as the primary operational path.
 * - Cache-first synchronous resolution for compatibility with synchronous CP solvers.
 * - Fail-fast on invalid configured paths (never hides configuration errors).
 * - Cache invalidation on configuration changes or executable disappearance.
 */

import * as fs from "fs";
import {
  PythonRuntime,
  PythonDiagnostic,
  RuntimeStatus,
  CandidateValidationResult,
  PythonCandidate
} from "./types";
import { PythonDiscoveryService, DiscoveryOptions } from "./discovery";
import { PythonValidator, ValidatorOptions } from "./validator";
import { SUPPORTED_RANGE_DESCRIPTION } from "./versionPolicy";
import { IFileSystem, NodeFileSystem } from "./fileSystem";
import { IProcessExecutor, NodeProcessExecutor } from "./processExecutor";
import { detectProjectRoot } from "./projectRoot";

export class PythonRuntimeError extends Error {
  public diagnostic: PythonDiagnostic;

  constructor(message: string, diagnostic: PythonDiagnostic) {
    super(message);
    this.name = "PythonRuntimeError";
    this.diagnostic = diagnostic;
  }
}

export class RuntimeNotPrimedError extends Error {
  constructor(message = "Offcode Python runtime is not yet primed. The runtime is asynchronously initialized upon extension activation.") {
    super(message);
    this.name = "RuntimeNotPrimedError";
  }
}

export interface PythonRuntimeManagerOptions {
  discoveryOptions?: DiscoveryOptions;
  validatorOptions?: ValidatorOptions;
  fs?: IFileSystem;
  executor?: IProcessExecutor;
  projectRoot?: string;
  configuredPath?: string;
  vscodePythonInterpreter?: string;
  platform?: NodeJS.Platform;
  env?: NodeJS.ProcessEnv;
}

export class PythonRuntimeManager {
  private static instance: PythonRuntimeManager | null = null;

  private fs: IFileSystem;
  private executor: IProcessExecutor;
  private discoveryService: PythonDiscoveryService;
  private validator: PythonValidator;
  private cachedRuntime: PythonRuntime | null = null;
  private resolutionPromise: Promise<PythonRuntime> | null = null;
  private lastDiagnostic: PythonDiagnostic | null = null;
  private options: PythonRuntimeManagerOptions;
  private projectRoot: string;

  constructor(options?: PythonRuntimeManagerOptions) {
    this.options = options || {};
    this.fs = this.options.fs || new NodeFileSystem();
    this.executor = this.options.executor || new NodeProcessExecutor();

    this.projectRoot = detectProjectRoot(this.options.projectRoot, this.fs);
    const platform = this.options.platform || process.platform;
    const env = this.options.env || process.env;

    this.discoveryService = new PythonDiscoveryService({
      configuredPath: this.options.configuredPath,
      projectRoot: this.projectRoot,
      platform,
      env,
      fs: this.fs,
      vscodePythonInterpreter: this.options.vscodePythonInterpreter,
      ...this.options.discoveryOptions
    });

    this.validator = new PythonValidator({
      executor: this.executor,
      projectRoot: this.projectRoot,
      platform,
      timeoutMs: 5000,
      ...this.options.validatorOptions
    });
  }

  public static getInstance(options?: PythonRuntimeManagerOptions): PythonRuntimeManager {
    if (!PythonRuntimeManager.instance) {
      PythonRuntimeManager.instance = new PythonRuntimeManager(options);
    }
    return PythonRuntimeManager.instance;
  }

  public static resetInstance(): void {
    PythonRuntimeManager.instance = null;
  }

  public getRuntime(): PythonRuntime | null {
    if (this.cachedRuntime && this.isCachedRuntimeHealthy(this.cachedRuntime)) {
      return this.cachedRuntime;
    }
    return null;
  }

  public clearCache(): void {
    this.cachedRuntime = null;
    this.resolutionPromise = null;
    this.lastDiagnostic = null;
  }

  /**
   * Defines precise invalidation semantics:
   * Invalidates only if the supplied runtime is still the currently cached runtime
   * (or unconditionally if omitted).
   * This prevents an older bridge operation from accidentally clearing a newer runtime
   * discovered by another concurrent operation.
   */
  public invalidateRuntime(runtime?: PythonRuntime): void {
    if (!runtime) {
      this.clearCache();
      return;
    }
    if (this.cachedRuntime?.concreteExecutable === runtime.concreteExecutable) {
      this.cachedRuntime = null;
      this.resolutionPromise = null;
    }
  }

  public onConfigurationChanged(newConfiguredPath?: string): void {
    this.clearCache();
    const effectivePath = newConfiguredPath?.trim() || undefined;
    this.options.configuredPath = effectivePath;
    const platform = this.options.platform || process.platform;
    const env = this.options.env || process.env;

    this.discoveryService = new PythonDiscoveryService({
      configuredPath: effectivePath,
      projectRoot: this.projectRoot,
      platform,
      env,
      fs: this.fs,
      vscodePythonInterpreter: this.options.vscodePythonInterpreter,
      ...this.options.discoveryOptions
    });
  }

  private isCachedRuntimeHealthy(runtime: PythonRuntime): boolean {
    // If it's a direct filesystem path, verify it still exists
    if (runtime.executable.includes("/") || runtime.executable.includes("\\")) {
      return this.fs.existsSync(runtime.executable);
    }
    return true;
  }

  /**
   * Primary asynchronous resolution method.
   * Concurrency-safe: shares an in-flight Promise among parallel callers during startup.
   * Discovers candidates, validates in precedence order, caches the result.
   */
  public async resolveRuntime(forceRefresh = false): Promise<PythonRuntime> {
    if (!forceRefresh && this.cachedRuntime && this.isCachedRuntimeHealthy(this.cachedRuntime)) {
      return this.cachedRuntime;
    }

    if (!forceRefresh && this.resolutionPromise) {
      return this.resolutionPromise;
    }

    const promise = this.doResolveRuntime();
    this.resolutionPromise = promise.finally(() => {
      if (this.resolutionPromise === promise) {
        this.resolutionPromise = null;
      }
    });

    return this.resolutionPromise;
  }

  private async doResolveRuntime(): Promise<PythonRuntime> {
    const candidates = this.discoveryService.discoverCandidates();
    const testedCandidates: Array<{
      executable: string;
      args: string[];
      source: any;
      error?: string;
    }> = [];

    let hasExplicitConfig = false;
    let explicitConfigFailed = false;
    let explicitConfigError = "";

    for (const candidate of candidates) {
      if (candidate.source === "configured") {
        hasExplicitConfig = true;
      }

      const valResult: CandidateValidationResult = await this.validator.validateCandidate(
        candidate
      );

      testedCandidates.push({
        executable: candidate.executable,
        args: candidate.args,
        source: candidate.source,
        error: valResult.error
      });

      if (valResult.valid && valResult.runtime) {
        this.cachedRuntime = valResult.runtime;
        this.lastDiagnostic = {
          status: "READY",
          executable: valResult.runtime.executable,
          args: valResult.runtime.args,
          concreteExecutable: valResult.runtime.concreteExecutable,
          version: valResult.runtime.version,
          source: valResult.runtime.source,
          testedCandidates,
          supportedRange: SUPPORTED_RANGE_DESCRIPTION
        };
        return valResult.runtime;
      }

      if (candidate.source === "configured") {
        explicitConfigFailed = true;
        explicitConfigError = valResult.error || "Explicitly configured interpreter is invalid.";
        break; // Do not silently fall back if user explicitly configured an invalid pythonPath!
      }
    }

    // Build failure diagnostic
    const status: RuntimeStatus = explicitConfigFailed
      ? "PYTHON_INVALID"
      : testedCandidates.length === 0
      ? "PYTHON_NOT_FOUND"
      : testedCandidates.some((c) => c.error?.includes("outside CHUP's supported range"))
      ? "PYTHON_VERSION_UNSUPPORTED"
      : testedCandidates.some((c) => c.error?.includes("bootstrap failed"))
      ? "PYTHON_BOOTSTRAP_FAILED"
      : "PYTHON_NOT_FOUND";

    const errorMessage = explicitConfigFailed
      ? `Explicitly configured Python interpreter failed validation:\n${explicitConfigError}`
      : this.formatFailureSummary(testedCandidates, status);

    const diagnostic: PythonDiagnostic = {
      status,
      testedCandidates,
      errorMessage,
      supportedRange: SUPPORTED_RANGE_DESCRIPTION
    };

    this.lastDiagnostic = diagnostic;
    throw new PythonRuntimeError(errorMessage, diagnostic);
  }

  /**
   * Bounded synchronous compatibility probe.
   * 1. Returns existing validated cache immediately (zero I/O).
   * 2. If unprimed, evaluates only narrow immediate candidates synchronously.
   * 3. Throws RuntimeNotPrimedError if unresolvable.
   */
  public resolveRuntimeSync(): PythonRuntime {
    if (this.cachedRuntime && this.isCachedRuntimeHealthy(this.cachedRuntime)) {
      return this.cachedRuntime;
    }

    // Attempt bounded immediate candidates synchronously (narrow fallback)
    const candidates = this.discoveryService.discoverImmediateCandidates();
    const testedCandidates: Array<{
      executable: string;
      args: string[];
      source: any;
      error?: string;
    }> = [];

    for (const candidate of candidates) {
      try {
        const valResult = this.validator.validateCandidateSync(candidate);
        testedCandidates.push({
          executable: candidate.executable,
          args: candidate.args,
          source: candidate.source,
          error: valResult.error
        });

        if (valResult.valid && valResult.runtime) {
          this.cachedRuntime = valResult.runtime;
          this.lastDiagnostic = {
            status: "READY",
            executable: valResult.runtime.executable,
            args: valResult.runtime.args,
            concreteExecutable: valResult.runtime.concreteExecutable,
            version: valResult.runtime.version,
            source: valResult.runtime.source,
            testedCandidates,
            supportedRange: SUPPORTED_RANGE_DESCRIPTION
          };
          return valResult.runtime;
        }

        if (candidate.source === "configured") {
          throw new PythonRuntimeError(
            `Explicitly configured Python interpreter failed validation:\n${valResult.error}`,
            {
              status: "PYTHON_INVALID",
              testedCandidates,
              errorMessage: valResult.error,
              supportedRange: SUPPORTED_RANGE_DESCRIPTION
            }
          );
        }
      } catch (err: any) {
        if (err instanceof PythonRuntimeError) throw err;
        testedCandidates.push({
          executable: candidate.executable,
          args: candidate.args,
          source: candidate.source,
          error: err.message
        });
      }
    }

    throw new RuntimeNotPrimedError(
      `Offcode Python runtime could not be resolved synchronously.\n` +
      `Validated cache was absent and bounded synchronous fallback failed (checked ${candidates.length} immediate candidates).\n` +
      `Please ensure Python >= 3.8 is installed or configure "offcode.pythonPath".`
    );
  }

  public getDiagnostic(): PythonDiagnostic {
    if (this.lastDiagnostic) {
      return this.lastDiagnostic;
    }

    if (this.cachedRuntime) {
      return {
        status: "READY",
        executable: this.cachedRuntime.executable,
        args: this.cachedRuntime.args,
        concreteExecutable: this.cachedRuntime.concreteExecutable,
        version: this.cachedRuntime.version,
        source: this.cachedRuntime.source,
        testedCandidates: [],
        supportedRange: SUPPORTED_RANGE_DESCRIPTION
      };
    }

    return {
      status: "PYTHON_NOT_FOUND",
      testedCandidates: [],
      errorMessage: "No Python runtime has been resolved yet.",
      supportedRange: SUPPORTED_RANGE_DESCRIPTION
    };
  }

  private formatFailureSummary(
    tested: Array<{ executable: string; args: string[]; source: any; error?: string }>,
    status: RuntimeStatus
  ): string {
    const lines: string[] = [
      "Offcode Python Runtime Unavailable",
      "",
      "No compatible Python interpreter could be found.",
      "",
      `Status: ${status}`,
      `Required: ${SUPPORTED_RANGE_DESCRIPTION}`,
      "",
      `Tested Candidates (${tested.length}):`
    ];

    for (const t of tested) {
      const inv = t.args.length > 0 ? `${t.executable} ${t.args.join(" ")}` : t.executable;
      lines.push(`- [${t.source}] ${inv}`);
      if (t.error) {
        lines.push(`  Reason: ${t.error}`);
      }
    }

    lines.push("");
    lines.push("Configure an explicit Python interpreter via the VS Code setting: 'offcode.pythonPath'.");
    return lines.join("\n");
  }
}
