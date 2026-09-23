/**
 * Deterministic Project/Extension Root Resolution.
 *
 * Locates the directory containing CHUP/Offcode Python modules
 * (python_parser, pointer_algorithms, architecture_v2).
 *
 * Prioritizes:
 * 1. Explicitly configured/passed project root (if specified).
 * 2. process.cwd() if it directly contains python_parser.
 * 3. VS Code extension host extensionPath (via vscode.extensions API if running in VS Code).
 * 4. Upward traversal from __dirname (out/runtime/ -> extension root).
 * 5. Parent directory of process.cwd().
 * 6. Active VS Code workspace folders.
 * 7. Fallback to process.cwd().
 */

import * as path from "path";
import * as fs from "fs";
import { IFileSystem } from "./fileSystem";

export function detectProjectRoot(explicitRoot?: string, customFs?: IFileSystem): string {
  // 1. Explicitly passed root takes precedence
  if (explicitRoot && explicitRoot.trim().length > 0) {
    return path.normalize(explicitRoot.trim());
  }

  const fileExists = (filePath: string): boolean => {
    try {
      if (customFs) {
        return customFs.existsSync(filePath);
      }
      return fs.existsSync(filePath);
    } catch {
      return false;
    }
  };

  const hasPythonParser = (candidate: string): boolean => {
    if (!candidate || candidate.trim().length === 0) return false;
    return (
      fileExists(path.join(candidate, "python_parser", "parser.py")) ||
      fileExists(path.join(candidate, "python_parser", "__init__.py"))
    );
  };

  // 2. process.cwd() if it directly contains python_parser (standard repo workflow / tests)
  const cwd = process.cwd();
  if (hasPythonParser(cwd)) {
    return path.normalize(cwd);
  }

  // 3. Check VS Code extension API if running in extension host
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const vscode = require("vscode");
    if (vscode && vscode.extensions) {
      const knownIds = [
        "adullahALMamun.offcode",
        "adullahalmamun.offcode",
        "abdullahalmamun29.chup",
        "chup",
        "offcode",
        "codeforge"
      ];
      for (const id of knownIds) {
        const ext = vscode.extensions.getExtension(id);
        if (ext?.extensionPath && hasPythonParser(ext.extensionPath)) {
          return path.normalize(ext.extensionPath);
        }
      }
      if (Array.isArray(vscode.extensions.all)) {
        for (const ext of vscode.extensions.all) {
          if (ext?.extensionPath && hasPythonParser(ext.extensionPath)) {
            return path.normalize(ext.extensionPath);
          }
        }
      }
    }
  } catch (_) {}

  // 4. Upward traversal from __dirname
  const dirCandidates = [
    path.resolve(__dirname, "..", ".."),
    path.resolve(__dirname, ".."),
    path.resolve(__dirname),
    path.resolve(__dirname, "..", "..", "..")
  ];
  for (const d of dirCandidates) {
    if (hasPythonParser(d)) {
      return path.normalize(d);
    }
  }

  // 5. Parent directory of process.cwd()
  const parentCwd = path.resolve(cwd, "..");
  if (hasPythonParser(parentCwd)) {
    return path.normalize(parentCwd);
  }

  // 6. Check VS Code workspace folders
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const vscode = require("vscode");
    if (vscode && vscode.workspace && Array.isArray(vscode.workspace.workspaceFolders)) {
      for (const wf of vscode.workspace.workspaceFolders) {
        const p = wf.uri?.fsPath;
        if (p && hasPythonParser(p)) {
          return path.normalize(p);
        }
      }
    }
  } catch (_) {}

  return cwd;
}
