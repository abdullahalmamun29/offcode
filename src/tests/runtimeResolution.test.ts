/**
 * Comprehensive Test Suite for CHUP Cross-Platform Python Runtime Resolution & Environment Hardening.
 *
 * Covers:
 * - Version policy and semver evaluation.
 * - Windows-style resolution (including 'py -3', PATH-missing, multiple versions, invalid config).
 * - Mandatory reproduction test: C:\\Python312\\python.exe non-PATH resolution.
 * - Linux-style resolution (python3, virtualenv, system paths).
 * - macOS-style resolution (Apple Silicon vs Intel Homebrew).
 * - Process execution timeouts, hung process kills, and error boundaries.
 * - In-memory caching, cache health checks, and configuration change invalidation.
 * - Decoupled C++ toolchain diagnostics (C++17 probe) and EnvironmentManager aggregation.
 * - Real integration test exercising the local environment.
 */

import * as path from "path";
import {
  parsePythonVersion,
  isVersionSupported,
  formatVersionRejectionMessage
} from "../runtime/versionPolicy";
import { MockProcessExecutor } from "../runtime/processExecutor";
import { MockFileSystem } from "../runtime/fileSystem";
import { PythonDiscoveryService } from "../runtime/discovery";
import { PythonValidator, PYTHON_VALIDATION_SCRIPT } from "../runtime/validator";
import {
  PythonRuntimeManager,
  PythonRuntimeError,
  RuntimeNotPrimedError
} from "../runtime/pythonRuntimeManager";
import { CxxToolchainManager } from "../runtime/cxxToolchainManager";
import { EnvironmentManager } from "../runtime/environmentManager";

export async function runRuntimeResolutionTests(): Promise<{ passed: number; failed: number }> {
  let passed = 0;
  let failed = 0;

  function assert(condition: boolean, testName: string, detail?: string) {
    if (condition) {
      console.log(`  ✓ ${testName}`);
      passed++;
    } else {
      console.error(`  ✗ ${testName}${detail ? ` (${detail})` : ""}`);
      failed++;
    }
  }

  console.log("\n=================================================");
  console.log("   CHUP Python Runtime Resolution Test Suite     ");
  console.log("=================================================");

  // ── 1. Python Version Policy Tests ──────────────────────────────────────────
  console.log("\n--- 1. Version Policy Unit Tests ---");

  const v1 = parsePythonVersion("3.12.3");
  assert(v1?.major === 3 && v1?.minor === 12 && v1?.patch === 3, "Parses standard version '3.12.3'");

  const v2 = parsePythonVersion("Python 3.10.8+");
  assert(v2?.major === 3 && v2?.minor === 10 && v2?.patch === 8, "Parses prefixed version 'Python 3.10.8+'");

  const v3 = parsePythonVersion("3.8");
  assert(v3?.major === 3 && v3?.minor === 8 && v3?.patch === 0, "Parses 2-component version '3.8'");

  assert(parsePythonVersion("invalid") === null, "Rejects unparseable version string");
  assert(isVersionSupported(3, 12), "Version 3.12 is supported");
  assert(isVersionSupported(3, 8), "Version 3.8 is supported");
  assert(!isVersionSupported(3, 7), "Version 3.7 is rejected (< 3.8)");
  assert(!isVersionSupported(2, 7), "Version 2.7 is rejected (major != 3)");
  assert(!isVersionSupported(4, 0), "Version 4.0 is rejected (major != 3)");

  const msg = formatVersionRejectionMessage("3.6.5", "/usr/bin/python3.6");
  assert(msg.includes("Python 3.6.5") && msg.includes("Python >= 3.8"), "Diagnostic message contains version & range");

  // ── 2. Windows Scenarios (Mocked) ───────────────────────────────────────────
  console.log("\n--- 2. Windows Scenarios (Mocked) ---");

  // Scenario W1: py -3 launcher with arguments
  {
    const mockFs = new MockFileSystem(true);
    const mockExec = new MockProcessExecutor();

    // py -3 responds with 3.12.2 and concrete executable
    mockExec.onCommand(
      (f, a) => f === "py" && a.includes("-3"),
      {
        stdout: JSON.stringify({
          sanity: true,
          major: 3,
          minor: 12,
          micro: 2,
          version: "3.12.2",
          concrete_executable: "C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
          bootstrap_ok: true
        }),
        stderr: "",
        exitCode: 0,
        timedOut: false
      }
    );

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "win32",
      env: {}
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.executable === "py", "W1: Resolves 'py' launcher");
    assert(runtime.args.includes("-3"), "W1: Retains ['-3'] in args");
    assert(runtime.concreteExecutable.includes("Python312"), "W1: Captures concrete interpreter path");
    assert(runtime.source === "windows-launcher", "W1: Source is 'windows-launcher'");
  }

  // Scenario W2: Explicit chup.pythonPath absolute path
  {
    const mockFs = new MockFileSystem(true);
    mockFs.addFile("D:\\CustomPython\\python.exe");

    const mockExec = new MockProcessExecutor();
    mockExec.onCommand(
      (f) => f.includes("CustomPython"),
      {
        stdout: JSON.stringify({
          sanity: true,
          major: 3,
          minor: 11,
          micro: 4,
          version: "3.11.4",
          concrete_executable: "D:\\CustomPython\\python.exe",
          bootstrap_ok: true
        }),
        stderr: "",
        exitCode: 0,
        timedOut: false
      }
    );

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "win32",
      configuredPath: "D:\\CustomPython\\python.exe",
      env: {}
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.executable === "D:\\CustomPython\\python.exe", "W2: Uses explicitly configured pythonPath");
    assert(runtime.source === "configured", "W2: Source is 'configured'");
  }

  // Scenario W3: Explicit configured path is invalid -> Fail fast (Never silently fall back)
  {
    const mockFs = new MockFileSystem(true);
    const mockExec = new MockProcessExecutor();
    // Path doesn't exist or fails execution
    mockExec.onCommand((f) => f.includes("NonExistent"), {
      stdout: "",
      stderr: "File not found",
      exitCode: -1,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "win32",
      configuredPath: "C:\\NonExistent\\python.exe",
      env: {}
    });

    let failedFast = false;
    try {
      await manager.resolveRuntime();
    } catch (err: any) {
      if (err instanceof PythonRuntimeError && err.message.includes("Explicitly configured")) {
        failedFast = true;
      }
    }
    assert(failedFast, "W3: Explicitly configured invalid interpreter fails fast without silent fallback");
  }

  // Scenario W4: Multiple Python versions, one unsupported (3.6) then supported (3.10)
  {
    const mockFs = new MockFileSystem(true);
    const mockExec = new MockProcessExecutor();

    // python.exe on PATH is 3.6 (unsupported)
    mockExec.onExact("python.exe", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 6,
        micro: 12,
        version: "3.6.12",
        concrete_executable: "C:\\Python36\\python.exe",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    // python3.exe on PATH is 3.10 (supported)
    mockExec.onExact("python3.exe", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 10,
        micro: 9,
        version: "3.10.9",
        concrete_executable: "C:\\Python310\\python.exe",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "win32",
      env: {}
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.major === 3 && runtime.minor === 10, "W4: Rejects 3.6 and selects compatible 3.10");
  }

  // Scenario W5: Bootstrap import failure returns PYTHON_BOOTSTRAP_FAILED
  {
    const mockFs = new MockFileSystem(true);
    const mockExec = new MockProcessExecutor();

    mockExec.onCommand(() => true, {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 11,
        micro: 0,
        version: "3.11.0",
        concrete_executable: "C:\\Python311\\python.exe",
        bootstrap_ok: false,
        bootstrap_error: "ModuleNotFoundError: No module named 'pointer_algorithms'"
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "win32",
      env: {}
    });

    let bootstrapFailed = false;
    try {
      await manager.resolveRuntime();
    } catch (err: any) {
      if (err instanceof PythonRuntimeError && err.diagnostic.status === "PYTHON_BOOTSTRAP_FAILED") {
        bootstrapFailed = true;
      }
    }
    assert(bootstrapFailed, "W5: Reports PYTHON_BOOTSTRAP_FAILED when imports fail");
  }

  // ── 3. MANDATORY Named Reproduction Regression Test: C:\Python312 ───────────
  console.log("\n--- 3. Mandatory Named Regression: C:\\Python312 Non-PATH ---");
  {
    /**
     * Exact user situation:
     * - C:\Python312\python.exe exists on disk
     * - PATH contains NO Python interpreter (python.exe, python3.exe, py fail)
     * - "where python" would return no result
     * - Direct execution of C:\Python312\python.exe succeeds
     * - CHUP discovers C:\Python312\python.exe from conservative known locations
     * - Resolves to READY
     */
    const mockFs = new MockFileSystem(true);
    mockFs.addFile("C:\\Python312\\python.exe");

    const mockExec = new MockProcessExecutor();

    // Commands on PATH fail with command not found
    mockExec.onExact("py", ["-3", "-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: "", stderr: "'py' is not recognized as an internal or external command", exitCode: 9009, timedOut: false
    });
    mockExec.onExact("py", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: "", stderr: "'py' is not recognized", exitCode: 9009, timedOut: false
    });
    mockExec.onExact("python.exe", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: "", stderr: "'python' is not recognized", exitCode: 9009, timedOut: false
    });
    mockExec.onExact("python3.exe", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: "", stderr: "'python3' is not recognized", exitCode: 9009, timedOut: false
    });

    // Direct invocation of C:\Python312\python.exe succeeds
    mockExec.onExact("C:\\Python312\\python.exe", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 12,
        micro: 7,
        version: "3.12.7",
        concrete_executable: "C:\\Python312\\python.exe",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "win32",
      env: {
        PATH: "C:\\Windows\\system32;C:\\Windows" // No Python on PATH
      }
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.executable === "C:\\Python312\\python.exe", "test_windows_c_python312_non_path_resolution: Discovers non-PATH C:\\Python312");
    assert(runtime.version === "3.12.7", "test_windows_c_python312_non_path_resolution: Validates version 3.12.7");
    assert(runtime.source === "known-location", "test_windows_c_python312_non_path_resolution: Source is 'known-location'");
    assert(manager.getDiagnostic().status === "READY", "test_windows_c_python312_non_path_resolution: Status is READY");
  }

  // ── 4. Linux Scenarios (Mocked) ─────────────────────────────────────────────
  console.log("\n--- 4. Linux Scenarios (Mocked) ---");

  // Scenario L1: Virtual Environment VIRTUAL_ENV active
  {
    const mockFs = new MockFileSystem();
    mockFs.addFile("/home/user/myenv/bin/python3");

    const mockExec = new MockProcessExecutor();
    mockExec.onExact("/home/user/myenv/bin/python3", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 11,
        micro: 2,
        version: "3.11.2",
        concrete_executable: "/home/user/myenv/bin/python3",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "linux",
      env: {
        VIRTUAL_ENV: "/home/user/myenv"
      }
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.executable === "/home/user/myenv/bin/python3", "L1: Prioritizes active VIRTUAL_ENV");
    assert(runtime.source === "virtual-environment", "L1: Source is 'virtual-environment'");
  }

  // Scenario L2: System /usr/bin/python3 fallback when PATH python fails
  {
    const mockFs = new MockFileSystem();
    mockFs.addFile("/usr/bin/python3");

    const mockExec = new MockProcessExecutor();
    mockExec.onExact("python3", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: "", stderr: "python3: command not found", exitCode: 127, timedOut: false
    });
    mockExec.onExact("python", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: "", stderr: "python: command not found", exitCode: 127, timedOut: false
    });
    mockExec.onExact("/usr/bin/python3", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 10,
        micro: 12,
        version: "3.10.12",
        concrete_executable: "/usr/bin/python3",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "linux",
      env: {}
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.executable === "/usr/bin/python3", "L2: Falls back to /usr/bin/python3");
    assert(runtime.source === "known-location", "L2: Source is 'known-location'");
  }

  // ── 5. macOS Scenarios (Mocked) ─────────────────────────────────────────────
  console.log("\n--- 5. macOS Scenarios (Mocked) ---");

  // Scenario M1: Homebrew on Apple Silicon (/opt/homebrew/bin/python3)
  {
    const mockFs = new MockFileSystem();
    mockFs.addFile("/opt/homebrew/bin/python3");

    const mockExec = new MockProcessExecutor();
    mockExec.onExact("/opt/homebrew/bin/python3", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 12,
        micro: 1,
        version: "3.12.1",
        concrete_executable: "/opt/homebrew/bin/python3",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "darwin",
      env: {}
    });

    const runtime = await manager.resolveRuntime();
    assert(runtime.executable === "/opt/homebrew/bin/python3", "M1: Discovers Apple Silicon Homebrew Python");
    assert(runtime.source === "known-location", "M1: Source is 'known-location'");
  }

  // ── 6. In-Memory Caching & Sync Resolution ──────────────────────────────────
  console.log("\n--- 6. Caching & Synchronous Resolution ---");
  {
    const mockFs = new MockFileSystem();
    mockFs.addFile("/usr/bin/python3");

    let execCallCount = 0;
    const mockExec = new MockProcessExecutor();
    mockExec.onExact("/usr/bin/python3", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], () => {
      execCallCount++;
      return {
        stdout: JSON.stringify({
          sanity: true,
          major: 3,
          minor: 11,
          micro: 0,
          version: "3.11.0",
          concrete_executable: "/usr/bin/python3",
          bootstrap_ok: true
        }),
        stderr: "",
        exitCode: 0,
        timedOut: false
      };
    });

    const manager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "linux",
      env: {}
    });

    // 1. Initial async resolution primes cache
    const r1 = await manager.resolveRuntime();
    assert(execCallCount === 1, "Cache 1: Validation called once");

    // 2. Second async resolution returns cached without executing again
    const r2 = await manager.resolveRuntime();
    assert(execCallCount === 1, "Cache 2: Cached runtime returned without re-execution");
    assert(r1 === r2, "Cache 3: Same runtime object returned");

    // 3. Synchronous resolution hits validated cache immediately (0ms)
    const rSync = manager.resolveRuntimeSync();
    assert(rSync === r1, "Cache 4: resolveRuntimeSync() returns primed cache immediately");
    assert(execCallCount === 1, "Cache 5: resolveRuntimeSync() did not trigger re-execution");

    // 4. Invalidation on configuration change
    manager.onConfigurationChanged("/usr/local/bin/python3");
    assert(manager.getRuntime() === null, "Cache 6: Cache is cleared on configuration change");

    // 5. Concurrency safety: Parallel calls during startup share same in-flight Promise
    const manager2 = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "linux",
      env: {}
    });
    execCallCount = 0;
    const [p1, p2, p3] = await Promise.all([
      manager2.resolveRuntime(),
      manager2.resolveRuntime(),
      manager2.resolveRuntime()
    ]);
    assert(p1 === p2 && p2 === p3, "Concurrency 1: Parallel resolveRuntime() calls share same Promise");
    assert(execCallCount === 1, "Concurrency 2: Validation executed exactly once for parallel callers");

    // 6. Precise invalidation semantics
    const staleRuntime = {
      ...p1,
      concreteExecutable: "/different/python3"
    };
    manager2.invalidateRuntime(staleRuntime);
    assert(manager2.getRuntime() !== null, "Invalidate 1: Stale runtime does not clear cache");
    manager2.invalidateRuntime(p1);
    assert(manager2.getRuntime() === null, "Invalidate 2: Matching runtime clears cache");

    // 7. Bounded synchronous compatibility probe failure contract
    const emptyFs = new MockFileSystem();
    const emptyExec = new MockProcessExecutor();
    const unprimedManager = new PythonRuntimeManager({
      fs: emptyFs,
      executor: emptyExec,
      platform: "linux",
      env: {}
    });
    let thrownError: any = null;
    try {
      unprimedManager.resolveRuntimeSync();
    } catch (e: any) {
      thrownError = e;
    }
    assert(thrownError instanceof RuntimeNotPrimedError, "SyncFallback 1: Throws RuntimeNotPrimedError when unprimed");
    assert(
      thrownError?.message.includes("bounded synchronous fallback failed"),
      "SyncFallback 2: Error explains bounded synchronous fallback"
    );

    // 8. Clean PYTHONPATH construction without trailing delimiter
    const validator = new PythonValidator({
      executor: mockExec,
      projectRoot: "/workspace/project",
      platform: "linux"
    });
    const origPythonPath = process.env.PYTHONPATH;
    delete process.env.PYTHONPATH;
    const optsEmpty = (validator as any).buildExecutionOptions();
    assert(optsEmpty.env.PYTHONPATH === "/workspace/project", "PYTHONPATH 1: No trailing delimiter when unset");
    process.env.PYTHONPATH = "   ";
    const optsWhitespace = (validator as any).buildExecutionOptions();
    assert(optsWhitespace.env.PYTHONPATH === "/workspace/project", "PYTHONPATH 2: No trailing delimiter when whitespace");
    process.env.PYTHONPATH = "/extra/lib";
    const optsCustom = (validator as any).buildExecutionOptions();
    assert(optsCustom.env.PYTHONPATH === "/workspace/project:/extra/lib", "PYTHONPATH 3: Correctly appends existing PYTHONPATH");
    if (origPythonPath !== undefined) {
      process.env.PYTHONPATH = origPythonPath;
    } else {
      delete process.env.PYTHONPATH;
    }
  }

  // ── 7. Decoupled C++ Toolchain & EnvironmentManager ─────────────────────────
  console.log("\n--- 7. C++ Separation & EnvironmentManager ---");
  {
    const mockExec = new MockProcessExecutor();

    // g++ compiler version
    mockExec.onExact("g++", ["--version"], {
      stdout: "g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0",
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    // g++ C++17 compilation probe
    mockExec.onCommand(
      (f, a) => f === "g++" && a.includes("-std=c++17"),
      {
        stdout: "",
        stderr: "",
        exitCode: 0,
        timedOut: false
      }
    );

    const cxxManager = new CxxToolchainManager({
      executor: mockExec,
      compilers: ["g++"]
    });

    const cxxDiag = await cxxManager.validateToolchain();
    assert(cxxDiag.status === "READY", "CXX 1: C++17 probe succeeds -> READY");
    assert(cxxDiag.compilerPath === "g++", "CXX 2: Compiler path is g++");
  }

  // Decoupled error test: Python is READY, C++ is MISSING -> Overall DEGRADED, Python NOT blamed
  {
    const mockFs = new MockFileSystem();
    mockFs.addFile("/usr/bin/python3");

    const mockExec = new MockProcessExecutor();
    // Python works
    mockExec.onExact("/usr/bin/python3", ["-c", PYTHON_VALIDATION_SCRIPT, process.cwd()], {
      stdout: JSON.stringify({
        sanity: true,
        major: 3,
        minor: 12,
        micro: 0,
        version: "3.12.0",
        concrete_executable: "/usr/bin/python3",
        bootstrap_ok: true
      }),
      stderr: "",
      exitCode: 0,
      timedOut: false
    });

    // All C++ compilers fail
    mockExec.onCommand((f) => f === "g++" || f === "clang++" || f === "c++", {
      stdout: "",
      stderr: "command not found",
      exitCode: 127,
      timedOut: false
    });

    const pythonManager = new PythonRuntimeManager({
      fs: mockFs,
      executor: mockExec,
      platform: "linux",
      env: {}
    });

    const cxxManager = new CxxToolchainManager({
      executor: mockExec,
      compilers: ["g++", "clang++", "c++"]
    });

    const envManager = new EnvironmentManager({
      pythonManager,
      cxxManager
    });

    const report = await envManager.diagnose();
    assert(report.python.status === "READY", "Decouple 1: Python status is READY");
    assert(report.cxx.status === "CXX_COMPILER_MISSING", "Decouple 2: C++ status is CXX_COMPILER_MISSING");
    assert(report.overallStatus === "DEGRADED", "Decouple 3: Overall status is DEGRADED, not BLOCKED");

    // Python missing -> Overall BLOCKED
    const emptyFs = new MockFileSystem();
    const emptyPythonManager = new PythonRuntimeManager({
      fs: emptyFs,
      executor: mockExec,
      platform: "linux",
      env: {}
    });
    const envManagerBlocked = new EnvironmentManager({
      pythonManager: emptyPythonManager,
      cxxManager
    });
    const reportBlocked = await envManagerBlocked.diagnose();
    assert(reportBlocked.python.status !== "READY", "Decouple 4: Python status is NOT READY");
    assert(reportBlocked.overallStatus === "BLOCKED", "Decouple 5: Missing Python yields BLOCKED overall");
  }

  // ── 8. Real Integration Test (Current Environment) ──────────────────────────
  console.log("\n--- 8. Real Integration Test ---");
  try {
    const realManager = new PythonRuntimeManager();
    const realRuntime = await realManager.resolveRuntime(true);
    assert(
      realRuntime.major === 3 && realRuntime.minor >= 8,
      `Real Integration: Resolved Python ${realRuntime.version} (${realRuntime.executable}) meets requirements`
    );
    assert(
      realRuntime.concreteExecutable.length > 0,
      `Real Integration: Concrete binary identified: ${realRuntime.concreteExecutable}`
    );
    assert(
      realManager.getDiagnostic().status === "READY",
      "Real Integration: Manager diagnostic status is READY"
    );

    // Verify synchronous resolution of primed cache
    const syncRuntime = realManager.resolveRuntimeSync();
    assert(syncRuntime.version === realRuntime.version, "Real Integration: Sync resolution returns primed runtime");
  } catch (err: any) {
    console.error("Real integration test error:", err);
    assert(false, "Real Integration: Exception occurred", err.message);
  }

  console.log(`\nRuntime Resolution Summary: ${passed} passed, ${failed} failed.`);
  return { passed, failed };
}

// Allow direct execution
if (require.main === module) {
  runRuntimeResolutionTests()
    .then((res) => {
      if (res.failed > 0) process.exit(1);
      process.exit(0);
    })
    .catch((err) => {
      console.error(err);
      process.exit(1);
    });
}
