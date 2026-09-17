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

  const disposable = vscode.commands.registerCommand(
    "codeforge.generateCppSolution",
    async () => {
      const query = await vscode.window.showInputBox({
        title: "CodeForge: Generate C++ Solution",
        prompt: "Enter a natural-language programming problem",
        placeHolder: "e.g., Insert a node at the end of a singly linked list."
      });

      if (!query || !query.trim()) {
        return;
      }

      const spec = await vscode.window.withProgress(
        {
          location: vscode.ProgressLocation.Notification,
          title: "CodeForge: Analyzing problem statement...",
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
            `CodeForge: ${resolution.code}\n${resolution.message}`
          );
          break;

        case "SUCCESS": {
          vscode.window.showInformationMessage(
            `CodeForge Detected: ${resolution.moduleName}\nGenerating verified solution...`
          );

          try {
            const generatedCode = generateCpp(resolution);

            const doc = await vscode.workspace.openTextDocument({
              content: generatedCode,
              language: "cpp"
            });
            await vscode.window.showTextDocument(doc);
            
            // Optionally, we could compile and run the generated code here, but it's typically an IDE action.
          } catch (genErr) {
            vscode.window.showErrorMessage(
              `CodeForge Code Generation Error: ${(genErr as Error).message}`
            );
          }
          break;
        }
      }
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {}
