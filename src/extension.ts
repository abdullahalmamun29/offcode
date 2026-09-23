import * as vscode from "vscode";
import { PythonBridge } from "./parser/pythonBridge";
import { UniversalInputPanel } from "./ui/universalInputPanel";
import { normalizeInput } from "./pipeline/inputNormalizer";
import { parseProblem } from "./pipeline/problemParser";
import { UNIVERSAL_ROUTER } from "./pipeline/universalRouter";
import { typeCodeCharacterByCharacter, typeSolutionIntoEditor } from "./utils/editorTyping";
import { PythonRuntimeManager, EnvironmentManager, resolveVsCodePythonInterpreter } from "./runtime";
import * as path from 'path';
import * as os from 'os';
import * as fs from 'fs';

function getOffcodeConfig<T>(key: string, defaultValue: T): T {
  const offcodeConfig = vscode.workspace.getConfiguration("offcode");
  const val = offcodeConfig.get<T>(key);
  if (val !== undefined && val !== "" && (typeof val !== "number" || !isNaN(val))) {
    return val;
  }
  return vscode.workspace.getConfiguration("chup").get<T>(key, defaultValue);
}

export function activate(context: vscode.ExtensionContext) {
  // Query optional VS Code Python extension / defaultInterpreterPath configuration
  const vscodePythonInterpreter = resolveVsCodePythonInterpreter();

  const configuredPythonPath =
    vscode.workspace.getConfiguration("offcode").get<string>("pythonPath", "").trim() ||
    vscode.workspace.getConfiguration("chup").get<string>("pythonPath", "").trim() ||
    undefined;

  const runtimeManager = PythonRuntimeManager.getInstance({
    projectRoot: context.extensionPath,
    configuredPath: configuredPythonPath,
    vscodePythonInterpreter
  });

  // Asynchronously prime the cache without blocking extension activation
  runtimeManager.resolveRuntime().catch((err) => {
    console.warn("[Offcode] Background Python runtime priming warning:", err.message);
  });

  // Invalidate and re-prime cache when pythonPath changes
  context.subscriptions.push(
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("offcode.pythonPath") || e.affectsConfiguration("chup.pythonPath")) {
        const newPath =
          vscode.workspace.getConfiguration("offcode").get<string>("pythonPath", "").trim() ||
          vscode.workspace.getConfiguration("chup").get<string>("pythonPath", "").trim() ||
          undefined;
        runtimeManager.onConfigurationChanged(newPath);
        runtimeManager.resolveRuntime(true).catch((err) => {
          vscode.window.showWarningMessage(`Offcode: Python runtime validation failed for configured path: ${err.message}`);
        });
      }
    })
  );

  const pythonBridge = new PythonBridge({ runtimeManager });

  const handleGenerate = async () => {
    const query = await vscode.window.showInputBox({
      title: "Offcode: Generate C++ Solution",
      prompt: "Enter a natural-language programming problem",
      placeHolder: "e.g., Insert a node at the end of a singly linked list."
    });

    if (!query || !query.trim()) {
      return;
    }

    const trimmed = query.trim();

    // Parse problem for structured context, constraints, and limits
    const normalized = normalizeInput(trimmed);
    const parsedProblem = parseProblem(normalized, trimmed);

    // Phase 4: Universal Capability-First Routing & Execution
    const solverResult = await vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: "Offcode: Resolving capability and generating solution...",
        cancellable: false
      },
      async () => {
        return UNIVERSAL_ROUTER.routeAndSolve(trimmed, parsedProblem);
      }
    );

    if (solverResult.success && solverResult.code) {
      vscode.window.showInformationMessage(
        `Offcode Detected: ${solverResult.approach}\nGenerating verified solution...`
      );
      try {
        const doc = await vscode.workspace.openTextDocument({
          content: "",
          language: "cpp"
        });
        await vscode.window.showTextDocument(doc);
        const typingDelayMs = getOffcodeConfig<number>("typingSpeedMs", 5);
        await typeCodeCharacterByCharacter(doc, solverResult.code, typingDelayMs);
      } catch (genErr) {
        vscode.window.showErrorMessage(
          `Offcode Code Generation Error: ${(genErr as Error).message}`
        );
      }
      return;
    }

    // Unresolved or failure handling with multi-layer failure taxonomy
    if (solverResult.failureCode) {
      vscode.window.showWarningMessage(
        `Offcode: ${solverResult.failureCode} [${solverResult.failureLayer || 'ROUTING'}]\n${solverResult.limitationMessage || solverResult.reasoning}`
      );
    } else {
      vscode.window.showErrorMessage(
        `Offcode: Unable to resolve solution.\n${solverResult.reasoning}`
      );
    }
  };

  const handleDiagnose = async () => {
    const envManager = new EnvironmentManager({
      pythonManager: runtimeManager,
      vscodeVersion: vscode.version
    });

    const report = await vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: "Offcode: Diagnosing Environment...",
        cancellable: false
      },
      async () => envManager.diagnose()
    );

    const outputChannel = vscode.window.createOutputChannel("Offcode Diagnostics");
    outputChannel.clear();
    outputChannel.appendLine(envManager.formatReport(report));
    outputChannel.show();

    if (report.overallStatus === "READY") {
      vscode.window.showInformationMessage("Offcode Environment is fully READY.");
    } else if (report.overallStatus === "DEGRADED") {
      vscode.window.showWarningMessage("Offcode Environment is DEGRADED: Python is ready, but C++ verification toolchain is missing.");
    } else {
      vscode.window.showErrorMessage(`Offcode Environment is BLOCKED: ${report.python.errorMessage || "Python runtime unavailable."}`);
    }
  };

  context.subscriptions.push(
    // Primary Offcode commands
    vscode.commands.registerCommand("offcode.generateCppSolution", handleGenerate),
    vscode.commands.registerCommand("offcode.openUniversalInput", () => {
      UniversalInputPanel.createOrShow(context.extensionUri, pythonBridge);
    }),
    vscode.commands.registerCommand("offcode.showExplanation", () => {
      UniversalInputPanel.showExplanationSector(context.extensionUri, pythonBridge);
    }),
    vscode.commands.registerCommand("offcode.diagnoseEnvironment", handleDiagnose),

    // Legacy backwards-compatible aliases
    vscode.commands.registerCommand("chup.generateCppSolution", handleGenerate),
    vscode.commands.registerCommand("codeforge.generateCppSolution", handleGenerate),
    vscode.commands.registerCommand("chup.openUniversalInput", () => {
      UniversalInputPanel.createOrShow(context.extensionUri, pythonBridge);
    }),
    vscode.commands.registerCommand("chup.showExplanation", () => {
      UniversalInputPanel.showExplanationSector(context.extensionUri, pythonBridge);
    }),
    vscode.commands.registerCommand("chup.diagnoseEnvironment", handleDiagnose)
  );
}

export function deactivate() {}


