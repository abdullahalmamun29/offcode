import * as vscode from "vscode";
import { PythonBridge } from "./parser/pythonBridge";
import { resolveProblemSpec } from "./resolver/operationResolver";
import { generateCpp } from "./generator/cppGenerator";
import { compileCpp } from "./verifier/compiler";
import { executeProgram } from "./verifier/runner";
import * as path from 'path';
import * as os from 'os';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
  const pythonBridge = new PythonBridge();

  const handleGenerate = async () => {
    const query = await vscode.window.showInputBox({
      title: "Chup: Generate C++ Solution",
      prompt: "Enter a natural-language programming problem",
      placeHolder: "e.g., Insert a node at the end of a singly linked list."
    });

    if (!query || !query.trim()) {
      return;
    }

    const spec = await vscode.window.withProgress(
      {
        location: vscode.ProgressLocation.Notification,
        title: "Chup: Analyzing problem statement...",
        cancellable: false
      },
      async () => {
        return await pythonBridge.parseQuery(query.trim());
      }
    );

    const resolution = resolveProblemSpec(spec);

    switch (resolution.code) {
      case "NEGATED":
      case "QUESTION":
      case "COMPOUND_UNSUPPORTED":
      case "AMBIGUOUS":
      case "UNSUPPORTED_STRUCTURE":
      case "UNSUPPORTED_OPERATION":
      case "IDENTIFIED_UNSUPPORTED":
        vscode.window.showWarningMessage(
          `Chup: ${resolution.code}\n${resolution.message}`
        );
        break;

      case "SUCCESS": {
        vscode.window.showInformationMessage(
          `Chup Detected: ${resolution.moduleName}\nGenerating verified solution...`
        );

        try {
          const generatedCode = generateCpp(resolution);

          const doc = await vscode.workspace.openTextDocument({
            content: generatedCode,
            language: "cpp"
          });
          await vscode.window.showTextDocument(doc);
        } catch (genErr) {
          vscode.window.showErrorMessage(
            `Chup Code Generation Error: ${(genErr as Error).message}`
          );
        }
        break;
      }
    }
  };

  context.subscriptions.push(
    vscode.commands.registerCommand("chup.generateCppSolution", handleGenerate),
    vscode.commands.registerCommand("codeforge.generateCppSolution", handleGenerate)
  );
}

export function deactivate() {}

