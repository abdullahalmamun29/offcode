/**
 * CodeForge - Deterministic Educational Programming Assistant
 * VS Code Extension Entry Point
 */

import * as vscode from "vscode";
import { PythonBridge } from "./parser/pythonBridge";
import { resolveProblemSpec, generateCodeForResolution } from "./resolver/operationResolver";

export function activate(context: vscode.ExtensionContext) {
  const pythonBridge = new PythonBridge();

  const disposable = vscode.commands.registerCommand(
    "codeforge.generateCppSolution",
    async () => {
      // 1. Ask the user to enter/paste a problem statement
      const query = await vscode.window.showInputBox({
        title: "CodeForge: Generate C++ Solution",
        prompt: "Enter a natural-language programming problem",
        placeHolder: "e.g., Insert a node at the end of a singly linked list."
      });

      if (!query || !query.trim()) {
        return;
      }

      // 2. Parse problem statement using local Python NLP process
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

      // 3. Resolve problem specification against verified modules
      const resolution = resolveProblemSpec(spec);

      // 4. Handle resolution outcomes
      switch (resolution.code) {
        case "CANNOT_IDENTIFY":
          vscode.window.showWarningMessage(
            `CodeForge: Could not identify the problem.\n${resolution.message}`
          );
          break;

        case "COMPOUND_UNSUPPORTED":
          vscode.window.showWarningMessage(
            `CodeForge: Compound problem detected.\n${resolution.message}`
          );
          break;

        case "IDENTIFIED_UNSUPPORTED":
          vscode.window.showInformationMessage(
            `CodeForge: Problem identified, but unsupported.\n${resolution.message}`
          );
          break;

        case "SUCCESS": {
          const detectedStructure = spec.structure?.replace(/_/g, " ");
          const detectedOperation = spec.operation?.replace(/_/g, " ");

          vscode.window.showInformationMessage(
            `CodeForge Detected:\nData Structure: ${detectedStructure}\nOperation: ${detectedOperation}\nLanguage: C++\nGenerating verified solution...`
          );

          try {
            // 5. Generate verified C++ implementation
            const generatedCode = generateCodeForResolution(resolution);

            // 6. Open a new editor containing the generated C++ code
            const doc = await vscode.workspace.openTextDocument({
              content: generatedCode,
              language: "cpp"
            });
            await vscode.window.showTextDocument(doc);
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
