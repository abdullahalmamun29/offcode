/**
 * Environment Health Manager for CHUP.
 *
 * Aggregates runtime telemetry across the Python Runtime Manager and C++ Toolchain Manager.
 * Computes overall system status (READY / DEGRADED / BLOCKED) without collapsing distinct errors.
 */

import * as os from "os";
import { EnvironmentReport, EnvironmentStatus, PythonDiagnostic, CxxDiagnostic } from "./types";
import { PythonRuntimeManager } from "./pythonRuntimeManager";
import { CxxToolchainManager } from "./cxxToolchainManager";

export interface EnvironmentManagerOptions {
  pythonManager?: PythonRuntimeManager;
  cxxManager?: CxxToolchainManager;
  vscodeVersion?: string;
  offcodeVersion?: string;
  chupVersion?: string;
}

export class EnvironmentManager {
  private pythonManager: PythonRuntimeManager;
  private cxxManager: CxxToolchainManager;
  private vscodeVersion?: string;
  private offcodeVersion?: string;
  private chupVersion?: string;

  constructor(options?: EnvironmentManagerOptions) {
    this.pythonManager = options?.pythonManager || PythonRuntimeManager.getInstance();
    this.cxxManager = options?.cxxManager || new CxxToolchainManager();
    this.vscodeVersion = options?.vscodeVersion;
    this.offcodeVersion = options?.offcodeVersion || options?.chupVersion || "2.2.0";
    this.chupVersion = this.offcodeVersion;
  }

  public async diagnose(): Promise<EnvironmentReport> {
    let pythonDiag: PythonDiagnostic;
    try {
      await this.pythonManager.resolveRuntime();
      pythonDiag = this.pythonManager.getDiagnostic();
    } catch {
      pythonDiag = this.pythonManager.getDiagnostic();
    }

    const cxxDiag = await this.cxxManager.validateToolchain();

    let overallStatus: EnvironmentStatus = "READY";

    if (pythonDiag.status !== "READY") {
      overallStatus = "BLOCKED";
    } else if (cxxDiag.status !== "READY") {
      overallStatus = "DEGRADED";
    }

    return {
      overallStatus,
      os: `${os.type()} ${os.release()}`,
      arch: os.arch(),
      python: pythonDiag,
      cxx: cxxDiag,
      vscodeVersion: this.vscodeVersion,
      offcodeVersion: this.offcodeVersion,
      chupVersion: this.chupVersion
    };
  }

  public formatReport(report: EnvironmentReport): string {
    const lines: string[] = [];
    lines.push("=================================================");
    lines.push("          Offcode Environment Diagnostics        ");
    lines.push("=================================================");
    lines.push(`Overall Status : ${report.overallStatus}`);
    lines.push(`Operating System : ${report.os} (${report.arch})`);
    if (report.vscodeVersion) lines.push(`VS Code Version : ${report.vscodeVersion}`);
    const ver = report.offcodeVersion || report.chupVersion;
    if (ver) lines.push(`Offcode Version : ${ver}`);
    lines.push("");

    lines.push("--- Python Subsystem ---");
    lines.push(`Status             : ${report.python.status}`);
    if (report.python.status === "READY") {
      const inv = report.python.args && report.python.args.length > 0
        ? `${report.python.executable} ${report.python.args.join(" ")}`
        : report.python.executable || "unknown";
      lines.push(`Executable         : ${inv}`);
      if (report.python.concreteExecutable && report.python.concreteExecutable !== report.python.executable) {
        lines.push(`Concrete Binary    : ${report.python.concreteExecutable}`);
      }
      lines.push(`Version            : ${report.python.version}`);
      lines.push(`Discovery Source   : ${report.python.source}`);
      lines.push(`Offcode Bootstrap  : READY`);
    } else {
      lines.push(`Required Version   : ${report.python.supportedRange}`);
      if (report.python.errorMessage) {
        lines.push(`Error Details      : ${report.python.errorMessage}`);
      }
      lines.push("Remediation        : Set 'offcode.pythonPath' in VS Code settings to an absolute Python path.");
    }
    lines.push("");

    lines.push("--- C++ Verification Subsystem ---");
    lines.push(`Status             : ${report.cxx.status}`);
    if (report.cxx.status === "READY") {
      lines.push(`Compiler           : ${report.cxx.compilerPath}`);
      lines.push(`Version            : ${report.cxx.compilerVersion}`);
      lines.push(`C++17 Probe        : PASSED`);
    } else {
      lines.push(`Error Details      : ${report.cxx.errorMessage}`);
      lines.push("Note               : Python reasoning will work, but C++ solution compilation & verification will be disabled.");
    }

    lines.push("=================================================");
    return lines.join("\n");
  }
}
