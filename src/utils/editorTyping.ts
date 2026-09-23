/**
 * CHUP — Editor Typing Utility.
 *
 * Types code into VS Code text documents character-by-character.
 * Each character edit is executed with `undoStopBefore: true` and `undoStopAfter: true`,
 * guaranteeing that pressing Ctrl+Z (Undo) undoes exactly ONE letter at a time.
 */

import * as vscode from 'vscode';

/**
 * Types raw code into the target document character-by-character.
 *
 * Key behaviors:
 * 1. Single-character atomic undo: `undoStopBefore: true` and `undoStopAfter: true` on every edit
 *    ensure that Ctrl+Z undoes letter-by-letter rather than a whole block.
 * 2. Human-like cadence: Subtle natural variance with slight pauses at newlines and delimiters.
 * 3. Robust background typing: Falls back to WorkspaceEdit if tab switches or is in background.
 * 4. Cursor tracking: Keeps the cursor and active viewport synced with the typing position.
 */
export async function typeCodeCharacterByCharacter(
  targetDoc: vscode.TextDocument,
  rawCode: string,
  delayMs: number = 5,
  startPosition?: vscode.Position,
  humanize: boolean = true
): Promise<void> {
  const code = rawCode.replace(/\r\n/g, '\n');
  let currentLine = startPosition ? startPosition.line : 0;
  let currentChar = startPosition ? startPosition.character : 0;

  const statusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Left,
    100
  );
  statusBar.text = '$(pencil) Chup: Writing solution...';
  statusBar.show();

  try {
    for (let i = 0; i < code.length; i++) {
      if (targetDoc.isClosed) {
        break;
      }

      const char = code[i];
      const insertPos = new vscode.Position(currentLine, currentChar);

      // 1. Try to edit through the visible editor if this document is currently displayed
      const visibleEditor = vscode.window.visibleTextEditors.find(
        e => e.document.uri.toString() === targetDoc.uri.toString()
      );

      let applied = false;
      if (visibleEditor) {
        try {
          // CRITICAL: undoStopBefore and undoStopAfter on every character insertion
          // guarantee that Ctrl+Z pops exactly ONE character from the undo stack.
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

      // 2. If tab is in background or editor.edit did not apply,
      // apply directly via WorkspaceEdit so typing continues seamlessly
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
      if (char === '\n') {
        currentLine++;
        currentChar = 0;
      } else {
        currentChar++;
      }

      // 3. Keep cursor and viewport synced if currently visible in any editor tab/split
      const activeEditor = vscode.window.visibleTextEditors.find(
        e => e.document.uri.toString() === targetDoc.uri.toString()
      );
      if (activeEditor) {
        const nextPos = new vscode.Position(currentLine, currentChar);
        activeEditor.selection = new vscode.Selection(nextPos, nextPos);
        if (char === '\n' || i % 15 === 0 || i === code.length - 1) {
          activeEditor.revealRange(
            new vscode.Range(nextPos, nextPos),
            vscode.TextEditorRevealType.Default
          );
        }
      }

      // 4. Human-like typing delay
      if (delayMs > 0) {
        let sleepMs = delayMs;
        if (humanize) {
          // Natural micro-jitter (±1.5ms)
          sleepMs += (Math.random() * 3 - 1.5);
          // Natural pause at statement ends, newlines, and brackets
          if (char === '\n') {
            sleepMs += Math.min(25, delayMs * 2);
          } else if (char === ';' || char === '{' || char === '}') {
            sleepMs += Math.min(15, delayMs * 1.5);
          }
        }
        if (sleepMs > 0) {
          await new Promise(resolve => setTimeout(resolve, Math.max(1, sleepMs)));
        }
      }
    }

    if (!targetDoc.isClosed) {
      statusBar.text = '$(check) Chup: Solution ready';
      setTimeout(() => statusBar.dispose(), 3000);
    }
  } catch (err) {
    console.error('Chup typing error:', err);
  } finally {
    if (targetDoc.isClosed) {
      statusBar.dispose();
    }
  }
}

/**
 * Finds or opens an appropriate C++ editor in ViewColumn.One and types the solution into it.
 */
export async function typeSolutionIntoEditor(
  code: string,
  delayMs: number = 5,
  humanize: boolean = true
): Promise<vscode.TextDocument> {
  // 1. Check for an empty visible C++ editor
  const emptyCppEditor = vscode.window.visibleTextEditors.find(
    e => e.document.languageId === 'cpp' && e.document.getText().trim().length === 0
  );

  let doc: vscode.TextDocument;
  if (emptyCppEditor) {
    doc = emptyCppEditor.document;
    await vscode.window.showTextDocument(doc, emptyCppEditor.viewColumn || vscode.ViewColumn.One, true);
  } else {
    // 2. Check for an existing empty untitled C++ document
    const untitledCpp = vscode.workspace.textDocuments.find(
      d => !d.isClosed && d.isUntitled && d.languageId === 'cpp' && d.getText().trim().length === 0
    );

    if (untitledCpp) {
      doc = untitledCpp;
      await vscode.window.showTextDocument(doc, vscode.ViewColumn.One, true);
    } else {
      // 3. Create a fresh untitled C++ document in ViewColumn.One (beside the Webview panel)
      doc = await vscode.workspace.openTextDocument({
        content: '',
        language: 'cpp'
      });
      await vscode.window.showTextDocument(doc, vscode.ViewColumn.One, true);
    }
  }

  await typeCodeCharacterByCharacter(doc, code, delayMs, new vscode.Position(0, 0), humanize);
  return doc;
}

/**
 * Types code at the current cursor position in the active editor if present,
 * or delegates to typeSolutionIntoEditor.
 */
export async function typeAtCursorOrNewDoc(
  code: string,
  delayMs: number = 5,
  humanize: boolean = true
): Promise<vscode.TextDocument> {
  const activeEditor = vscode.window.activeTextEditor;
  if (activeEditor && !activeEditor.document.isClosed) {
    const startPos = activeEditor.selection.active;
    await typeCodeCharacterByCharacter(activeEditor.document, code, delayMs, startPos, humanize);
    return activeEditor.document;
  }
  return typeSolutionIntoEditor(code, delayMs, humanize);
}
