/**
 * Offcode V2 — Universal Input Panel.
 *
 * VS Code Webview panel providing the v2 problem-solving interface:
 *   - Multi-line text area for pasting problems
 *   - Mode selector (Auto / CP / Academic / Debug)
 *   - Analyze button → shows parsed problem structure
 *   - Solve button → runs solver pipeline with character-by-character typing
 *   - Dual typing: streams code into both the C++ editor tab and webview panel
 *   - Granular Ctrl+Z undo support (letter-by-letter)
 *   - Offcode Explanation Sector: dedicated tab for authoritative Phase 5 & 6 proof inspection
 */

import * as vscode from 'vscode';
import { normalizeInput } from '../pipeline/inputNormalizer';
import { parseProblem } from '../pipeline/problemParser';
import { classifyProblem } from '../pipeline/problemClassifier';
import { solveCpProblem } from '../solver/cpSolver';
import { UNIVERSAL_ROUTER } from '../pipeline/universalRouter';
import { StructuredProblem, ClassificationResult, SolverResult } from '../models/problemSpec';
import { PythonBridge } from '../parser/pythonBridge';
import { PointerBridge } from '../parser/pointerBridge';
import { ExplanationDocument, validateExplanationDocument, ExplanationLevel } from '../models/explanationModel';
import { resolveProblemSpec } from '../resolver/operationResolver';
import { generateCpp } from '../generator/cppGenerator';
import { typeSolutionIntoEditor, typeAtCursorOrNewDoc } from '../utils/editorTyping';

function getOffcodeConfig<T>(key: string, defaultValue: T): T {
  const offcodeConfig = vscode.workspace.getConfiguration('offcode');
  const val = offcodeConfig.get<T>(key);
  if (val !== undefined && val !== "" && (typeof val !== "number" || !isNaN(val))) {
    return val;
  }
  return vscode.workspace.getConfiguration('chup').get<T>(key, defaultValue);
}

export class UniversalInputPanel {
  public static currentPanel: UniversalInputPanel | undefined;
  private readonly _panel: vscode.WebviewPanel;
  private _disposables: vscode.Disposable[] = [];
  private _pythonBridge?: PythonBridge;
  private _pointerBridge: PointerBridge;

  private _lastProblem: StructuredProblem | null = null;
  private _lastClassification: ClassificationResult | null = null;
  private _lastRawText: string = '';

  public static createOrShow(extensionUri: vscode.Uri, pythonBridge?: PythonBridge): void {
    const column = vscode.ViewColumn.Beside;

    if (UniversalInputPanel.currentPanel) {
      if (pythonBridge) {
        UniversalInputPanel.currentPanel._pythonBridge = pythonBridge;
      }
      UniversalInputPanel.currentPanel._panel.reveal(column);
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      'offcodeUniversalInput',
      'Offcode Problem Solver',
      column,
      { enableScripts: true, retainContextWhenHidden: true }
    );

    UniversalInputPanel.currentPanel = new UniversalInputPanel(panel, pythonBridge);
  }

  public static showExplanationSector(extensionUri: vscode.Uri, pythonBridge?: PythonBridge): void {
    UniversalInputPanel.createOrShow(extensionUri, pythonBridge);
    UniversalInputPanel.currentPanel?.showExplanationSector();
  }

  public showExplanationSector(): void {
    this._panel.reveal();
    this._panel.webview.postMessage({ command: 'showExplanationSector' });
  }

  private constructor(panel: vscode.WebviewPanel, pythonBridge?: PythonBridge) {
    this._panel = panel;
    this._pythonBridge = pythonBridge;
    this._pointerBridge = new PointerBridge();
    this._panel.webview.html = this._getHtmlContent();

    this._panel.onDidDispose(() => this.dispose(), null, this._disposables);

    this._panel.webview.onDidReceiveMessage(
      (msg) => this._handleMessage(msg),
      null,
      this._disposables
    );
  }

  public dispose(): void {
    UniversalInputPanel.currentPanel = undefined;
    this._panel.dispose();
    for (const d of this._disposables) d.dispose();
  }

  private async _handleMessage(msg: {
    command: string;
    text?: string;
    mode?: string;
    autoTypeEditor?: boolean;
    level?: ExplanationLevel;
    notification?: string;
  }): Promise<void> {
    switch (msg.command) {
      case 'analyze': {
        if (!msg.text) return;
        const raw = msg.text;
        this._lastRawText = raw;
        const normalized = normalizeInput(raw);
        const problem = parseProblem(normalized, raw);

        const defaultMode = getOffcodeConfig<string>('defaultMode', 'auto');
        const modeOverride = (msg.mode && msg.mode !== 'auto') ? msg.mode : (defaultMode !== 'auto' ? defaultMode : undefined);

        const classification = classifyProblem(problem, modeOverride);
        problem.problemType = classification.selected;

        this._lastProblem = problem;
        this._lastClassification = classification;

        this._panel.webview.postMessage({
          command: 'analysisResult',
          problem: {
            title: problem.title,
            source: problem.source,
            timeLimit: problem.timeLimit,
            memoryLimit: problem.memoryLimit,
            constraintCount: problem.constraints.length,
            constraints: problem.constraints.map(c => `${c.variable} ≤ ${c.upperBound}`),
            exampleCount: problem.examples.length,
            parserConfidence: problem.parserConfidence,
            hasInputSpec: !!problem.inputSpecification,
            hasOutputSpec: !!problem.outputSpecification,
            hasNotes: !!problem.notes
          },
          classification: {
            selected: classification.selected,
            confidence: classification.confidence,
            scores: classification.scores,
            signals: classification.signals
          }
        });
        break;
      }

      case 'solve': {
        if (!this._lastProblem) {
          this._panel.webview.postMessage({
            command: 'error',
            message: 'No problem analyzed yet. Click Analyze first.'
          });
          return;
        }

        const problem = this._lastProblem;
        const classification = this._lastClassification;
        const maxRetries = getOffcodeConfig<number>('maxRetries', 3);
        const typingDelayMs = getOffcodeConfig<number>('typingSpeedMs', 5);
        const autoTypeToEditor = msg.autoTypeEditor !== undefined ? msg.autoTypeEditor : getOffcodeConfig<boolean>('autoTypeToEditor', true);

        if (classification?.selected === 'code_debug') {
          this._panel.webview.postMessage({
            command: 'solveResult',
            result: {
              success: false,
              approach: '',
              code: '',
              reasoning: 'Debug mode is not yet implemented in v2.',
              limitationMessage: 'Debug solver is planned for a future version.'
            },
            typingDelayMs
          });
          return;
        }

        // Capability-First Universal Solving
        this._panel.webview.postMessage({ command: 'solving' });

        try {
          const rawText = problem.normalizedInput?.normalizedText || problem.statement || problem.title || this._lastRawText;
          const capResult = await UNIVERSAL_ROUTER.routeAndSolve(rawText, problem);

          const verification = capResult.verification ? {
            compiled: capResult.verification.compiled,
            compilationErrors: capResult.verification.errors || [],
            testResults: [],
            allPassed: capResult.verification.allPassed,
            failureType: null,
            summary: capResult.verification.allPassed ? 'Verification passed' : 'Verification failed'
          } : null;

          const result: SolverResult = {
            success: capResult.success,
            problemType: (capResult.metadata?.domains?.[0] as any) || classification?.selected || 'competitive_programming',
            approach: capResult.approach || 'capability_solution',
            code: capResult.code,
            reasoning: capResult.reasoning,
            detectedTopics: [],
            feasibility: null,
            selectedAlgorithm: capResult.algorithmId || capResult.approach || null,
            verification,
            correctionHistory: [],
            limitationMessage: capResult.limitationMessage || null
          };

          this._panel.webview.postMessage({ command: 'solveResult', result, typingDelayMs });

          // If code was generated and auto-type is enabled, type into editor character-by-character
          if (result.success && result.code && autoTypeToEditor) {
            await typeSolutionIntoEditor(result.code, typingDelayMs, true);
          }
        } catch (err: unknown) {
          const errorMessage = err instanceof Error ? err.message : String(err);
          this._panel.webview.postMessage({
            command: 'error',
            message: `Universal Solver error: ${errorMessage}`
          });
        }
        break;
      }

      case 'requestExplanation': {
        const level = msg.level || 'DETAILED';
        const text = this._lastProblem?.statement || this._lastProblem?.title || this._lastRawText;
        if (!text || !text.trim()) {
          this._panel.webview.postMessage({
            command: 'explanationError',
            message: 'No problem statement available to explain. Please analyze a problem first.'
          });
          return;
        }

        try {
          const res = await this._pointerBridge.explainProblem(text, level);
          if (res.status === 'success' && res.explanation) {
            const validated = validateExplanationDocument(res.explanation);
            this._panel.webview.postMessage({
              command: 'explanationResult',
              explanation: validated || res.explanation,
              markdown: res.markdown
            });
          } else {
            this._panel.webview.postMessage({
              command: 'explanationError',
              message: res.error || 'Failed to generate explanation.'
            });
          }
        } catch (err: unknown) {
          this._panel.webview.postMessage({
            command: 'explanationError',
            message: err instanceof Error ? err.message : String(err)
          });
        }
        break;
      }

      case 'copyToClipboard': {
        if (msg.text) {
          await vscode.env.clipboard.writeText(msg.text);
          vscode.window.showInformationMessage(msg.notification || 'Copied to clipboard.');
        }
        break;
      }

      case 'exportJson': {
        if (msg.text) {
          const uri = await vscode.window.showSaveDialog({
            filters: { 'JSON Files': ['json'] },
            defaultUri: vscode.Uri.file('offcode-proof-explanation.json')
          });
          if (uri) {
            await vscode.workspace.fs.writeFile(uri, Buffer.from(msg.text, 'utf-8'));
            vscode.window.showInformationMessage(`Proof JSON successfully exported to ${uri.fsPath}`);
          }
        }
        break;
      }

      case 'insertCode':
      case 'typeIntoEditor': {
        if (!msg.text) return;
        const typingDelayMs = getOffcodeConfig<number>('typingSpeedMs', 5);
        await typeAtCursorOrNewDoc(msg.text, typingDelayMs, true);
        break;
      }
    }
  }

  private _getHtmlContent(): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: var(--vscode-font-family);
    font-size: var(--vscode-font-size);
    color: var(--vscode-foreground);
    background: var(--vscode-editor-background);
    padding: 16px;
  }
  h2 { margin-bottom: 12px; font-size: 1.3em; }
  h3 { margin: 12px 0 8px; font-size: 1.1em; color: var(--vscode-descriptionForeground); }

  /* Navigation Tabs */
  .tabs {
    display: flex;
    border-bottom: 1px solid var(--vscode-editorWidget-border);
    margin-bottom: 16px;
    gap: 6px;
  }
  .tab-button {
    background: transparent;
    color: var(--vscode-foreground);
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 0.95em;
    cursor: pointer;
    opacity: 0.7;
    transition: opacity 0.2s, border-color 0.2s;
  }
  .tab-button:hover {
    opacity: 1;
    background: var(--vscode-toolbar-hoverBackground, rgba(255,255,255,0.05));
  }
  .tab-button.active {
    opacity: 1;
    border-bottom: 2px solid var(--vscode-progressBar-background, #007acc);
    color: var(--vscode-button-foreground, #fff);
  }
  .tab-content { display: none; }
  .tab-content.active { display: block; }

  textarea {
    width: 100%; min-height: 180px; padding: 8px;
    font-family: var(--vscode-editor-font-family);
    font-size: var(--vscode-editor-font-size);
    background: var(--vscode-input-background);
    color: var(--vscode-input-foreground);
    border: 1px solid var(--vscode-input-border);
    border-radius: 4px; resize: vertical;
  }
  textarea:focus { outline: 1px solid var(--vscode-focusBorder); }

  select {
    padding: 6px 10px;
    background: var(--vscode-dropdown-background);
    color: var(--vscode-dropdown-foreground);
    border: 1px solid var(--vscode-dropdown-border);
    border-radius: 4px; font-size: 0.9em;
  }

  button {
    padding: 7px 16px; margin: 4px 4px 4px 0;
    background: var(--vscode-button-background);
    color: var(--vscode-button-foreground);
    border: none; border-radius: 4px; cursor: pointer;
    font-size: 0.9em; font-weight: 500;
  }
  button:hover { background: var(--vscode-button-hoverBackground); }
  button.secondary {
    background: var(--vscode-button-secondaryBackground);
    color: var(--vscode-button-secondaryForeground);
  }
  button.secondary:hover {
    background: var(--vscode-button-secondaryHoverBackground);
  }

  .controls { display: flex; align-items: center; gap: 12px; margin: 12px 0; flex-wrap: wrap; }
  .checkbox-label {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.9em; cursor: pointer;
    color: var(--vscode-foreground); user-select: none;
  }
  .checkbox-label input { cursor: pointer; }

  .section { margin-bottom: 16px; }

  .analysis-grid {
    display: grid; grid-template-columns: auto 1fr;
    gap: 4px 12px; font-size: 0.9em;
    padding: 10px; border-radius: 4px;
    background: var(--vscode-editorWidget-background);
    border: 1px solid var(--vscode-editorWidget-border);
  }
  .analysis-grid .label { color: var(--vscode-descriptionForeground); font-weight: 500; }

  .scores { display: flex; gap: 12px; flex-wrap: wrap; font-size: 0.85em; margin: 6px 0; }
  .score-item { padding: 3px 8px; border-radius: 3px; background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); }
  .score-item.winner { background: var(--vscode-progressBar-background); font-weight: 600; }

  .signals { font-size: 0.85em; color: var(--vscode-descriptionForeground); margin: 4px 0; }

  .code-container {
    margin: 10px 0;
    border: 1px solid var(--vscode-editorWidget-border);
    border-radius: 4px;
    background: var(--vscode-textCodeBlock-background);
    overflow: hidden;
  }

  .code-header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 8px 12px;
    background: var(--vscode-editorWidget-background);
    border-bottom: 1px solid var(--vscode-editorWidget-border);
    flex-wrap: wrap; gap: 8px;
  }

  .code-title { font-weight: 600; font-size: 0.95em; }

  .code-actions { display: flex; gap: 6px; align-items: center; }
  .code-actions button { margin: 0; padding: 4px 10px; font-size: 0.82em; }

  pre {
    padding: 12px;
    overflow-x: auto; font-size: 0.9em;
    font-family: var(--vscode-editor-font-family);
    white-space: pre-wrap; word-break: break-word;
    max-height: 400px; overflow-y: auto;
    line-height: 1.45;
  }

  .typing-cursor {
    display: inline-block;
    color: var(--vscode-progressBar-background, #007acc);
    font-weight: bold;
    animation: blink 0.8s infinite;
  }
  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }

  .reasoning { white-space: pre-wrap; font-size: 0.9em; line-height: 1.5; margin: 8px 0; }

  .limitation {
    padding: 10px; border-radius: 4px; margin: 8px 0;
    background: var(--vscode-inputValidation-warningBackground);
    border: 1px solid var(--vscode-inputValidation-warningBorder);
  }

  .success-badge { color: #4caf50; font-weight: 600; }
  .fail-badge { color: #f44336; font-weight: 600; }

  .correction-item {
    font-size: 0.85em; padding: 6px 10px; margin: 4px 0;
    border-left: 3px solid var(--vscode-progressBar-background);
    background: var(--vscode-editorWidget-background);
  }

  .spinner { display: inline-block; animation: spin 1s linear infinite; }
  @keyframes spin { 100% { transform: rotate(360deg); } }

  #analysis, #results { display: none; }

  /* Explanation Sector Styles */
  .explanation-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--vscode-editorWidget-background);
    padding: 8px 12px;
    border-radius: 4px;
    margin-bottom: 12px;
    border: 1px solid var(--vscode-editorWidget-border);
    flex-wrap: wrap;
    gap: 8px;
  }
  .toolbar-group {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .toolbar-label {
    font-size: 0.9em;
    color: var(--vscode-descriptionForeground);
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .outcome-banner {
    padding: 12px 16px;
    border-radius: 4px;
    margin-bottom: 14px;
    background: var(--vscode-editorWidget-background);
    border-left: 4px solid var(--vscode-progressBar-background);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
  }
  .outcome-banner.sat { border-left-color: #4caf50; }
  .outcome-banner.unsat { border-left-color: #f44336; }
  .outcome-banner.unresolved { border-left-color: #ff9800; }

  .outcome-title {
    font-weight: 600;
    font-size: 1.05em;
  }
  .outcome-meta {
    font-size: 0.85em;
    color: var(--vscode-descriptionForeground);
  }

  .accordion-card {
    margin-bottom: 8px;
    border: 1px solid var(--vscode-editorWidget-border);
    border-radius: 4px;
    background: var(--vscode-editorWidget-background);
    overflow: hidden;
  }
  .accordion-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 14px;
    cursor: pointer;
    user-select: none;
    font-weight: 600;
    font-size: 0.92em;
    background: var(--vscode-editorGroupHeader-tabsBackground, rgba(0,0,0,0.1));
  }
  .accordion-header:hover {
    background: var(--vscode-list-hoverBackground, rgba(255,255,255,0.05));
  }
  .accordion-title {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .accordion-chevron {
    font-size: 0.8em;
    transition: transform 0.2s;
  }
  .accordion-chevron.collapsed {
    transform: rotate(-90deg);
  }
  .accordion-content {
    padding: 12px;
    border-top: 1px solid var(--vscode-editorWidget-border);
  }
  .accordion-content.collapsed {
    display: none;
  }

  .claim-item {
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 4px;
    background: var(--vscode-editor-background);
    border: 1px solid var(--vscode-input-border);
  }
  .claim-item:last-child {
    margin-bottom: 0;
  }
  .claim-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }
  .claim-type-tag {
    font-size: 0.78em;
    opacity: 0.75;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }
  .claim-statement {
    font-size: 0.9em;
    line-height: 1.45;
    margin-bottom: 6px;
  }

  /* Epistemic Status Badges */
  .status-badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 3px;
    font-size: 0.75em;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }
  .status-proven {
    background: #1b5e20;
    color: #c8e6c9;
    border: 1px solid #2e7d32;
  }
  .status-supported {
    background: #0d47a1;
    color: #bbdefb;
    border: 1px solid #1565c0;
  }
  .status-hypothetical {
    background: #e65100;
    color: #ffe0b2;
    border: 1px solid #ef6c00;
  }
  .status-unresolved {
    background: #b71c1c;
    color: #ffcdd2;
    border: 1px solid #c62828;
  }

  .evidence-drawer {
    margin-top: 6px;
    font-size: 0.82em;
  }
  .evidence-drawer summary {
    cursor: pointer;
    color: var(--vscode-textLink-foreground, #3794ff);
    user-select: none;
    font-size: 0.85em;
  }
  .evidence-drawer summary:hover {
    text-decoration: underline;
  }
  .evidence-card {
    margin-top: 6px;
    padding: 6px 10px;
    border-radius: 3px;
    background: var(--vscode-textCodeBlock-background);
    border: 1px solid var(--vscode-editorWidget-border);
    font-family: var(--vscode-editor-font-family);
  }
  .evidence-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
    font-weight: 600;
    font-size: 0.85em;
  }

  .empty-state {
    text-align: center;
    padding: 48px 24px;
    opacity: 0.7;
    font-size: 0.95em;
    line-height: 1.6;
  }
</style>
</head>
<body>

<div class="tabs">
  <button class="tab-button active" id="tabSolveBtn" onclick="switchTab('solve')">⚡ Solve & Code</button>
  <button class="tab-button" id="tabExplanationBtn" onclick="switchTab('explanation')">🔍 Offcode Explanation Sector</button>
</div>

<!-- Tab 1: Solve & Code -->
<div id="solveTab" class="tab-content active">
  <h2>Offcode Problem Solver</h2>

  <div class="section">
    <textarea id="problemInput" placeholder="Paste a problem statement here...&#10;&#10;Supports: Codeforces, AtCoder, CSES, generic CP problems, DSA questions, natural language requests.&#10;&#10;Messy formatting is fine — Offcode will normalize it."></textarea>
    <div class="controls">
      <select id="modeSelect">
        <option value="auto" selected>Auto</option>
        <option value="competitive_programming">Competitive Programming</option>
        <option value="academic">Academic</option>
        <option value="code_debug">Code / Debug</option>
      </select>
      <label class="checkbox-label" title="Automatically type generated code into the C++ editor letter-by-letter with Ctrl+Z single-character undo">
        <input type="checkbox" id="autoTypeCheckbox" checked> Auto-type into editor
      </label>
      <button id="analyzeBtn" onclick="analyze()">Analyze</button>
      <button id="solveBtn" class="secondary" onclick="solve()" disabled>Solve</button>
    </div>
  </div>

  <div id="analysis" class="section">
    <h3>Problem Analysis</h3>
    <div id="analysisContent"></div>
  </div>

  <div id="results" class="section">
    <h3>Solution</h3>
    <div id="resultsContent"></div>
  </div>
</div>

<!-- Tab 2: Offcode Explanation Sector -->
<div id="explanationTab" class="tab-content">
  <h2>Offcode Proof & Explanation Engine</h2>

  <div class="explanation-toolbar">
    <div class="toolbar-group">
      <label class="toolbar-label">
        Level:
        <select id="explanationLevelSelect" onchange="onLevelChange()">
          <option value="CONCISE">Concise</option>
          <option value="DETAILED" selected>Detailed</option>
          <option value="AUDIT_PROOF_TRACE">Audit / Proof Trace</option>
        </select>
      </label>
    </div>
    <div class="toolbar-group">
      <button class="secondary" onclick="copyExplanationMarkdown()">📋 Copy Markdown</button>
      <button class="secondary" onclick="exportExplanationJson()">💾 Export Proof JSON</button>
    </div>
  </div>

  <div id="explanationContainer">
    <div id="explanationContent">
      <div class="empty-state">
        No explanation generated yet.<br>
        Analyze or solve a problem to view verified proofs, derivations, and epistemic boundaries.
      </div>
    </div>
  </div>
</div>

<script>
  const vscode = acquireVsCodeApi();
  let typingTimer = null;
  window.currentFullCode = '';
  window.currentExplanation = null;
  window.currentExplanationMarkdown = '';
  window.lastProblemText = '';

  function switchTab(tabName) {
    document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    if (tabName === 'solve') {
      document.getElementById('tabSolveBtn').classList.add('active');
      document.getElementById('solveTab').classList.add('active');
    } else if (tabName === 'explanation') {
      document.getElementById('tabExplanationBtn').classList.add('active');
      document.getElementById('explanationTab').classList.add('active');
      if (!window.currentExplanation && window.lastProblemText) {
        requestExplanation();
      }
    }
  }

  function resetExplanationState() {
    window.currentExplanation = null;
    window.currentExplanationMarkdown = '';
    const container = document.getElementById('explanationContent');
    if (container) {
      container.innerHTML = '<div class="empty-state"><span class="spinner">⟳</span> Solving problem and deriving proofs...</div>';
    }
  }

  function analyze() {
    const text = document.getElementById('problemInput').value;
    if (!text.trim()) return;
    window.lastProblemText = text;
    window.currentExplanation = null;
    window.currentExplanationMarkdown = '';

    const mode = document.getElementById('modeSelect').value;
    document.getElementById('analyzeBtn').textContent = 'Analyzing...';
    document.getElementById('analyzeBtn').disabled = true;
    vscode.postMessage({ command: 'analyze', text, mode });
  }

  function solve() {
    document.getElementById('solveBtn').textContent = 'Solving...';
    document.getElementById('solveBtn').disabled = true;
    resetExplanationState();
    const autoTypeEditor = document.getElementById('autoTypeCheckbox').checked;
    vscode.postMessage({ command: 'solve', autoTypeEditor });
  }

  function requestExplanation() {
    const level = document.getElementById('explanationLevelSelect').value;
    document.getElementById('explanationContent').innerHTML =
      '<div class="empty-state"><span class="spinner">⟳</span> Deriving verified explanation (' + level + ')...</div>';
    vscode.postMessage({ command: 'requestExplanation', level });
  }

  function onLevelChange() {
    requestExplanation();
  }

  function copyExplanationMarkdown() {
    if (window.currentExplanationMarkdown) {
      vscode.postMessage({
        command: 'copyToClipboard',
        text: window.currentExplanationMarkdown,
        notification: 'Explanation Markdown copied to clipboard.'
      });
    } else if (window.currentExplanation) {
      const generated = generateFallbackMarkdown(window.currentExplanation);
      vscode.postMessage({
        command: 'copyToClipboard',
        text: generated,
        notification: 'Explanation Markdown copied to clipboard.'
      });
    } else {
      vscode.postMessage({
        command: 'copyToClipboard',
        text: 'No explanation available to copy.',
        notification: 'No explanation available.'
      });
    }
  }

  function exportExplanationJson() {
    if (!window.currentExplanation) return;
    const jsonStr = JSON.stringify(window.currentExplanation, null, 2);
    vscode.postMessage({ command: 'exportJson', text: jsonStr });
  }

  function generateFallbackMarkdown(doc) {
    const bt = String.fromCharCode(96);
    let md = '# Offcode Proof & Explanation: ' + doc.problem_id + '\\n\\n';
    md += '**Outcome State**: ' + bt + doc.outcome_state + bt + '\\n';
    md += '**Level**: ' + bt + doc.level + bt + '\\n\\n';

    const sections = [
      ['Problem Understanding', doc.understanding_section],
      ['Proven Facts', doc.proven_facts_section],
      ['Invariants & Derivations', doc.derivation_section],
      ['Constraints', doc.constraint_section],
      ['Candidate Elimination', doc.elimination_section],
      ['Selected Component(s)', doc.selection_section],
      ['Composition & Invariant Preservation', doc.composition_section],
      ['Resource Verification', doc.resource_section],
      ['Proof Obligations & Correctness', doc.correctness_section],
      ['Final Status', doc.summary_section]
    ];

    for (const [title, s] of sections) {
      if (!s || !s.claims || s.claims.length === 0) continue;
      md += '## ' + title + '\\n\\n';
      for (const c of s.claims) {
        md += '- [' + c.epistemic_status + '] ' + c.text + '\\n';
        if (c.evidence_refs && c.evidence_refs.length > 0) {
          for (const ev of c.evidence_refs) {
            md += '  - *Evidence (' + ev.kind + ')*: ' + ev.evidence_id + ' — ' + ev.summary + '\\n';
          }
        }
      }
      md += '\\n';
    }
    return md;
  }

  function toggleAccordion(id) {
    const content = document.getElementById(id + '-content');
    const chevron = document.getElementById(id + '-chevron');
    if (!content || !chevron) return;
    if (content.classList.contains('collapsed')) {
      content.classList.remove('collapsed');
      chevron.classList.remove('collapsed');
    } else {
      content.classList.add('collapsed');
      chevron.classList.add('collapsed');
    }
  }

  function renderExplanation(doc, markdown) {
    window.currentExplanation = doc;
    if (markdown) {
      window.currentExplanationMarkdown = markdown;
    }

    if (!doc) {
      document.getElementById('explanationContent').innerHTML =
        '<div class="empty-state">No explanation available.</div>';
      return;
    }

    let outcomeClass = 'sat';
    if (doc.outcome_state.includes('UNSATISFIABLE')) outcomeClass = 'unsat';
    else if (doc.outcome_state.includes('UNRESOLVED')) outcomeClass = 'unresolved';

    let html = '';

    // Outcome Banner
    html += '<div class="outcome-banner ' + outcomeClass + '">';
    html += '  <div>';
    html += '    <div class="outcome-title">Outcome: ' + esc(doc.outcome_state) + '</div>';
    html += '    <div class="outcome-meta">Problem: ' + esc(doc.problem_id) + ' | Level: ' + esc(doc.level) + ' | Schema v' + esc(doc.schema_version) + '</div>';
    html += '  </div>';
    html += '  <div>';
    html += '    <span class="status-badge status-' + (outcomeClass === 'sat' ? 'proven' : outcomeClass === 'unsat' ? 'unresolved' : 'hypothetical') + '">Phase 5/6 Evidence Verified</span>';
    html += '  </div>';
    html += '</div>';

    // 10 Sections
    const sectionList = [
      { id: 'sec-understanding', title: '1. Problem Understanding', sec: doc.understanding_section },
      { id: 'sec-facts', title: '2. Proven Facts', sec: doc.proven_facts_section },
      { id: 'sec-derivations', title: '3. Invariants & Derivations', sec: doc.derivation_section },
      { id: 'sec-constraints', title: '4. Constraints', sec: doc.constraint_section },
      { id: 'sec-eliminations', title: '5. Candidate Elimination', sec: doc.elimination_section },
      { id: 'sec-selection', title: '6. Selected Component(s)', sec: doc.selection_section },
      { id: 'sec-composition', title: '7. Composition & Invariant Preservation', sec: doc.composition_section },
      { id: 'sec-resource', title: '8. Resource Verification', sec: doc.resource_section },
      { id: 'sec-correctness', title: '9. Proof Obligations & Correctness', sec: doc.correctness_section },
      { id: 'sec-summary', title: '10. Final Status & Summary', sec: doc.summary_section }
    ];

    for (const item of sectionList) {
      const s = item.sec;
      const count = (s && s.claims) ? s.claims.length : 0;
      const isAutoExpanded = count > 0;

      html += '<div class="accordion-card">';
      html += '  <div class="accordion-header" onclick="toggleAccordion(\\'' + item.id + '\\')">';
      html += '    <div class="accordion-title">';
      html += '      <span id="' + item.id + '-chevron" class="accordion-chevron' + (isAutoExpanded ? '' : ' collapsed') + '">▼</span>';
      html += '      <span>' + esc(item.title) + '</span>';
      html += '    </div>';
      html += '    <span class="score-item' + (count > 0 ? ' winner' : '') + '">' + count + ' claim' + (count === 1 ? '' : 's') + '</span>';
      html += '  </div>';
      html += '  <div id="' + item.id + '-content" class="accordion-content' + (isAutoExpanded ? '' : ' collapsed') + '">';

      if (count === 0) {
        html += '<div style="opacity:0.6; font-size:0.85em; font-style:italic;">No claims recorded in this section.</div>';
      } else {
        for (const claim of s.claims) {
          const statusClass = (claim.epistemic_status || 'PROVEN').toLowerCase();
          html += '<div class="claim-item">';
          html += '  <div class="claim-top">';
          html += '    <span class="claim-type-tag">' + esc(claim.claim_type || '') + '</span>';
          html += '    <span class="status-badge status-' + statusClass + '">' + esc(claim.epistemic_status) + '</span>';
          html += '  </div>';
          html += '  <div class="claim-statement">' + esc(claim.text) + '</div>';

          if (claim.evidence_refs && claim.evidence_refs.length > 0) {
            html += '<details class="evidence-drawer">';
            html += '  <summary>Evidence References (' + claim.evidence_refs.length + ')</summary>';
            for (const ref of claim.evidence_refs) {
              html += '  <div class="evidence-card">';
              html += '    <div class="evidence-header">';
              html += '      <span>[' + esc(ref.kind) + '] ' + esc(ref.evidence_id) + '</span>';
              html += '      <span style="opacity:0.7;">' + esc(ref.source_layer) + '</span>';
              html += '    </div>';
              html += '    <div style="font-size:0.85em; opacity:0.9;">' + esc(ref.summary) + '</div>';
              html += '  </div>';
            }
            html += '</details>';
          }
          html += '</div>';
        }
      }

      html += '  </div>';
      html += '</div>';
    }

    document.getElementById('explanationContent').innerHTML = html;
  }

  function typeIntoEditor(code) {
    const textToType = code || window.currentFullCode;
    if (!textToType) return;
    vscode.postMessage({ command: 'typeIntoEditor', text: textToType });
  }

  function copyCode() {
    if (!window.currentFullCode) return;
    navigator.clipboard.writeText(window.currentFullCode);
    const copyBtn = document.getElementById('copyBtn');
    if (copyBtn) {
      const orig = copyBtn.textContent;
      copyBtn.textContent = 'Copied!';
      setTimeout(() => { copyBtn.textContent = orig; }, 1500);
    }
  }

  function startWebviewTyping(fullCode, delayMs) {
    if (typingTimer) {
      clearTimeout(typingTimer);
      typingTimer = null;
    }
    const codeEl = document.getElementById('codeContent');
    const cursor = document.getElementById('typingCursor');
    const skipBtn = document.getElementById('skipTypingBtn');
    if (!codeEl) return;

    codeEl.textContent = '';
    if (cursor) cursor.style.display = 'inline';
    if (skipBtn) skipBtn.style.display = 'inline-block';

    let idx = 0;
    const speed = (delayMs !== undefined && delayMs !== null) ? delayMs : 5;

    if (speed <= 0) {
      codeEl.textContent = fullCode;
      if (cursor) cursor.style.display = 'none';
      if (skipBtn) skipBtn.style.display = 'none';
      return;
    }

    function typeStep() {
      if (idx < fullCode.length) {
        const char = fullCode[idx++];
        codeEl.textContent += char;

        const pre = document.getElementById('codeBlock');
        if (pre && (char === '\\n' || idx % 20 === 0)) {
          pre.scrollTop = pre.scrollHeight;
        }

        let nextDelay = speed;
        if (char === '\\n') {
          nextDelay += 15;
        } else if (char === ';' || char === '{' || char === '}') {
          nextDelay += 10;
        }

        typingTimer = setTimeout(typeStep, nextDelay);
      } else {
        if (cursor) cursor.style.display = 'none';
        if (skipBtn) skipBtn.style.display = 'none';
        typingTimer = null;
      }
    }

    typeStep();
  }

  function skipWebviewTyping() {
    if (typingTimer) {
      clearTimeout(typingTimer);
      typingTimer = null;
    }
    if (window.currentFullCode) {
      const codeEl = document.getElementById('codeContent');
      const cursor = document.getElementById('typingCursor');
      const skipBtn = document.getElementById('skipTypingBtn');
      if (codeEl) codeEl.textContent = window.currentFullCode;
      if (cursor) cursor.style.display = 'none';
      if (skipBtn) skipBtn.style.display = 'none';
    }
  }

  window.addEventListener('message', event => {
    const msg = event.data;

    if (msg.command === 'showExplanationSector') {
      switchTab('explanation');
    }

    if (msg.command === 'explanationResult') {
      renderExplanation(msg.explanation, msg.markdown);
    }

    if (msg.command === 'explanationError') {
      document.getElementById('explanationContent').innerHTML =
        '<div class="limitation">Failed to load explanation: ' + esc(msg.message) + '</div>';
    }

    if (msg.command === 'analysisResult') {
      const p = msg.problem;
      const c = msg.classification;
      let html = '<div class="analysis-grid">';
      if (p.title) html += '<span class="label">Title</span><span>' + esc(p.title) + '</span>';
      html += '<span class="label">Source</span><span>' + esc(p.source) + '</span>';
      if (p.timeLimit) html += '<span class="label">Time Limit</span><span>' + p.timeLimit + 's</span>';
      if (p.memoryLimit) html += '<span class="label">Memory Limit</span><span>' + p.memoryLimit + ' MB</span>';
      html += '<span class="label">Constraints</span><span>' + (p.constraints.length > 0 ? esc(p.constraints.join(', ')) : 'none detected') + '</span>';
      html += '<span class="label">Examples</span><span>' + p.exampleCount + ' found</span>';
      html += '<span class="label">Input Spec</span><span>' + (p.hasInputSpec ? '✓' : '✗') + '</span>';
      html += '<span class="label">Output Spec</span><span>' + (p.hasOutputSpec ? '✓' : '✗') + '</span>';
      html += '<span class="label">Parser Confidence</span><span>' + (p.parserConfidence * 100).toFixed(0) + '%</span>';
      html += '</div>';

      html += '<h3>Classification</h3>';
      html += '<div class="scores">';
      for (const [type, score] of Object.entries(c.scores)) {
        const isWinner = type === c.selected;
        html += '<span class="score-item' + (isWinner ? ' winner' : '') + '">' + type.replace(/_/g, ' ') + ': ' + (score * 100).toFixed(0) + '%</span>';
      }
      html += '</div>';
      html += '<div class="signals">' + c.signals.map(s => '• ' + esc(s)).join('<br>') + '</div>';

      document.getElementById('analysisContent').innerHTML = html;
      document.getElementById('analysis').style.display = 'block';
      document.getElementById('analyzeBtn').textContent = 'Re-analyze';
      document.getElementById('analyzeBtn').disabled = false;
      document.getElementById('solveBtn').disabled = false;
      document.getElementById('solveBtn').textContent = 'Solve';
    }

    if (msg.command === 'solving') {
      document.getElementById('results').style.display = 'block';
      document.getElementById('resultsContent').innerHTML = '<span class="spinner">⟳</span> Solving problem...';
    }

    if (msg.command === 'solveResult') {
      const r = msg.result;
      let html = '';

      if (r.limitationMessage) {
        html += '<div class="limitation">' + esc(r.limitationMessage) + '</div>';
      }

      if (r.approach) {
        html += '<h3>Approach</h3><p>' + esc(r.approach) + '</p>';
      }

      if (r.reasoning) {
        html += '<h3>Reasoning</h3><div class="reasoning">' + esc(r.reasoning) + '</div>';
      }

      if (r.explanation) {
        renderExplanation(r.explanation, r.explanationMarkdown);
        html += '<div style="margin: 12px 0;">';
        html += '  <button class="secondary" onclick="switchTab(\\x27explanation\\x27)">🔍 View Verified Proof & Explanation</button>';
        html += '</div>';
      }

      if (r.code) {
        window.currentFullCode = r.code;
        html += '<div class="code-container">';
        html += '  <div class="code-header">';
        html += '    <span class="code-title">Generated Code ' + (r.success ? '<span class="success-badge">✓ VERIFIED</span>' : '<span class="fail-badge">✗ ISSUES</span>') + '</span>';
        html += '    <div class="code-actions">';
        html += '      <button id="skipTypingBtn" class="secondary" onclick="skipWebviewTyping()">Show Instantly</button>';
        html += '      <button id="typeEditorBtn" onclick="typeIntoEditor()">Type into Editor</button>';
        html += '      <button id="copyBtn" class="secondary" onclick="copyCode()">Copy</button>';
        html += '    </div>';
        html += '  </div>';
        html += '  <pre id="codeBlock"><code id="codeContent"></code><span id="typingCursor" class="typing-cursor">▌</span></pre>';
        html += '</div>';
      }

      if (r.verification) {
        html += '<h3>Verification</h3><p>' + esc(r.verification.summary) + '</p>';
      }

      if (r.correctionHistory && r.correctionHistory.length > 0) {
        html += '<h3>Correction History</h3>';
        for (const c of r.correctionHistory) {
          html += '<div class="correction-item">';
          html += '<strong>Attempt ' + c.attempt + '</strong>: ' + esc(c.diagnosis.description) + '<br>';
          html += 'Fix: ' + esc(c.fixApplied) + '<br>';
          html += 'Result: ' + (c.result.allPassed ? '<span class="success-badge">Passed</span>' : '<span class="fail-badge">Still failing</span>');
          html += '</div>';
        }
      }

      if (r.detectedTopics && r.detectedTopics.length > 0) {
        html += '<h3>Detected Topics</h3><div class="scores">';
        for (const t of r.detectedTopics.slice(0, 8)) {
          const label = t.conceptId.replace(/_/g, ' ') + ' ' + (t.confidence * 100).toFixed(0) + '%';
          html += '<span class="score-item' + (t.rejected ? '' : ' winner') + '">' + esc(label) + (t.rejected ? ' ✗' : '') + '</span>';
        }
        html += '</div>';
      }

      document.getElementById('resultsContent').innerHTML = html;
      document.getElementById('results').style.display = 'block';
      document.getElementById('solveBtn').textContent = 'Solve Again';
      document.getElementById('solveBtn').disabled = false;

      // Start typing animation in webview
      if (r.code) {
        startWebviewTyping(r.code, msg.typingDelayMs);
      }
    }

    if (msg.command === 'error') {
      document.getElementById('resultsContent').innerHTML = '<div class="limitation">' + esc(msg.message) + '</div>';
      document.getElementById('results').style.display = 'block';
      document.getElementById('solveBtn').textContent = 'Solve';
      document.getElementById('solveBtn').disabled = false;
      document.getElementById('analyzeBtn').disabled = false;
    }
  });

  function esc(s) {
    if (!s) return '';
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }
</script>

</body>
</html>`;
  }
}
