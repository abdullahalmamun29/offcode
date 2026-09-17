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

          await typeCodeCharacterByCharacter(doc, generatedCode, typingDelayMs);
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
 * Types the generated code into the target document character-by-character.
 * Seamlessly continues typing even if the user switches to another file tab
 * or switches outside of VS Code (e.g. to Code::Blocks).
 * Each character edit is an atomic undo transaction, so Ctrl+Z undoes letter-by-letter.
 */
async function typeCodeCharacterByCharacter(
  targetDoc: vscode.TextDocument,
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
      if (targetDoc.isClosed) {
        break;
      }

      const char = code[i];
      const insertPos = new vscode.Position(currentLine, currentChar);

      // 1. Try to edit through visible editor if this document is currently displayed
      const visibleEditor = vscode.window.visibleTextEditors.find(
        e => e.document.uri.toString() === targetDoc.uri.toString()
      );

      let applied = false;
      if (visibleEditor) {
        try {
          applied = await visibleEditor.edit(
            editBuilder => {
              editBuilder.insert(insertPos, char);
            },
            { undoStopBefore: true, undoStopAfter: true }
          );
        } catch {
          applied = false;
        }
      }

      // 2. If tab is in background or editor.edit did not apply (e.g. switched to another file or app),
      // apply directly via WorkspaceEdit so typing NEVER stops!
      if (!applied && !targetDoc.isClosed) {
        try {
          const wsEdit = new vscode.WorkspaceEdit();
          wsEdit.insert(targetDoc.uri, insertPos, char);
          applied = await vscode.workspace.applyEdit(wsEdit);
        } catch {
          if (targetDoc.isClosed) {
            break;
          }
        }
      }

      if (targetDoc.isClosed) {
        break;
      }

      // Advance cursor tracking
      if (char === "\n") {
        currentLine++;
        currentChar = 0;
      } else {
        currentChar++;
      }

      // 3. Keep cursor and viewport synced if currently visible in any editor split/tab
      const activeEditor = vscode.window.visibleTextEditors.find(
        e => e.document.uri.toString() === targetDoc.uri.toString()
      );
      if (activeEditor) {
        const nextPos = new vscode.Position(currentLine, currentChar);
        activeEditor.selection = new vscode.Selection(nextPos, nextPos);
        if (char === "\n" || i % 15 === 0 || i === code.length - 1) {
          activeEditor.revealRange(
            new vscode.Range(nextPos, nextPos),
            vscode.TextEditorRevealType.Default
          );
        }
      }

      if (delayMs > 0) {
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    }

    if (!targetDoc.isClosed) {
      statusBar.text = "$(check) Chup: Solution ready";
      setTimeout(() => statusBar.dispose(), 3000);
    }
  } catch (err) {
    console.error("Chup typing error:", err);
  } finally {
    if (targetDoc.isClosed) {
      statusBar.dispose();
    }
  }
}

export function deactivate() {}

