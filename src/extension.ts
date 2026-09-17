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
            content: "",
            language: "cpp"
          });
          const editor = await vscode.window.showTextDocument(doc);

          const config = vscode.workspace.getConfiguration("chup");
          const typingDelayMs = config.get<number>("typingSpeedMs", 5);

          await typeCodeCharacterByCharacter(editor, generatedCode, typingDelayMs);
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

/**
 * Types the generated code into the active editor character-by-character.
 * Each character edit is executed with `undoStopBefore: true` and `undoStopAfter: true`,
 * ensuring that pressing Ctrl+Z (Undo) undoes one individual character at a time.
 */
async function typeCodeCharacterByCharacter(
  editor: vscode.TextEditor,
  rawCode: string,
  delayMs: number
): Promise<void> {
  const code = rawCode.replace(/\r\n/g, "\n");
  let currentLine = 0;
  let currentChar = 0;

  const statusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    100
  );
  statusBar.text = "$(pencil) Chup: Writing solution...";
  statusBar.show();

  try {
    for (let i = 0; i < code.length; i++) {
      if (editor.document.isClosed) {
        break;
      }

      const char = code[i];
      const insertPos = new vscode.Position(currentLine, currentChar);

      const success = await editor.edit(
        editBuilder => {
          editBuilder.insert(insertPos, char);
        },
        { undoStopBefore: true, undoStopAfter: true }
      );

      if (!success) {
        break;
      }

      if (char === "\n") {
        currentLine++;
        currentChar = 0;
      } else {
        currentChar++;
      }

      const nextPos = new vscode.Position(currentLine, currentChar);

      // Follow cursor and viewport safely
      if (vscode.window.visibleTextEditors.includes(editor)) {
        editor.selection = new vscode.Selection(nextPos, nextPos);
        if (char === "\n" || i % 20 === 0 || i === code.length - 1) {
          editor.revealRange(
            new vscode.Range(nextPos, nextPos),
            vscode.TextEditorRevealType.Default
          );
        }
      }

      if (delayMs > 0) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    }
  } finally {
    statusBar.dispose();
  }
}

export function deactivate() {}

