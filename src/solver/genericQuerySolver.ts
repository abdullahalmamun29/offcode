/**
 * CHUP V2 — Generic Query Schema Solver
 *
 * Synthesizes C++ from a QuerySchema produced by querySchemaExtractor.
 * Zero problem-specific labels — all code is driven by SemanticOp vocabulary.
 */

import { QuerySchema, SemanticOp } from '../pipeline/querySchemaExtractor';
import { StructuredProblem } from '../models/problemSpec';

function containerDecl(container: string): { includes: string[]; decl: string } {
  switch (container) {
    case 'multiset_ordered':
      return { includes: ['<iostream>', '<set>'], decl: 'multiset<long long> s;' };
    case 'priority_queue_max':
      return { includes: ['<iostream>', '<queue>'], decl: 'priority_queue<long long> s;' };
    case 'priority_queue_min':
      return {
        includes: ['<iostream>', '<queue>', '<vector>'],
        decl: 'priority_queue<long long, vector<long long>, greater<long long>> s;',
      };
    case 'deque':
      return { includes: ['<iostream>', '<deque>'], decl: 'deque<long long> s;' };
    case 'queue':
      return { includes: ['<iostream>', '<queue>'], decl: 'queue<long long> s;' };
    default:
      return { includes: ['<iostream>', '<set>'], decl: 'multiset<long long> s;' };
  }
}

function opSnippet(op: SemanticOp, container: string, argVar: string, noMatch: string): string {
  switch (op) {
    case 'insert':
      if (container === 'deque')   return `long long ${argVar}; if (cin >> ${argVar}) s.push_back(${argVar});`;
      if (container === 'queue')   return `long long ${argVar}; if (cin >> ${argVar}) s.push(${argVar});`;
      return `long long ${argVar}; if (cin >> ${argVar}) s.insert(${argVar});`;
    case 'extract_min':
      if (container === 'multiset_ordered')
        return `if (!s.empty()) { auto it = s.begin(); cout << *it << "\\n"; s.erase(it); }`;
      return `if (!s.empty()) { cout << s.top() << "\\n"; s.pop(); }`;
    case 'extract_max':
      if (container === 'multiset_ordered')
        return `if (!s.empty()) { auto it = prev(s.end()); cout << *it << "\\n"; s.erase(it); }`;
      return `if (!s.empty()) { cout << s.top() << "\\n"; s.pop(); }`;
    case 'floor_remove':
      return `long long ${argVar}; if (cin >> ${argVar}) { auto it = s.upper_bound(${argVar}); if (it == s.begin()) cout << ${noMatch} << "\\n"; else { --it; cout << *it << "\\n"; s.erase(it); } }`;
    case 'ceiling_remove':
      return `long long ${argVar}; if (cin >> ${argVar}) { auto it = s.lower_bound(${argVar}); if (it == s.end()) cout << ${noMatch} << "\\n"; else { cout << *it << "\\n"; s.erase(it); } }`;
    case 'push_front':
      return `long long ${argVar}; if (cin >> ${argVar}) s.push_front(${argVar});`;
    case 'push_back':
      return `long long ${argVar}; if (cin >> ${argVar}) s.push_back(${argVar});`;
    case 'pop_front':
      return `if (!s.empty()) { cout << s.front() << "\\n"; s.pop_front(); }`;
    case 'pop_back':
      return `if (!s.empty()) { cout << s.back() << "\\n"; s.pop_back(); }`;
    case 'index_access':
      return `{ int idx; if (cin >> idx && idx >= 0 && idx < (int)s.size()) cout << s[idx] << "\\n"; }`;
    default:
      return `// unhandled op: ${op}`;
  }
}

export function solveWithQuerySchema(
  schema: QuerySchema,
  _problem: StructuredProblem
): string | null {
  const { includes, decl } = containerDecl(schema.container);
  const includeStr = includes.map(h => `#include ${h}`).join('\n');
  const n = schema.initialLoadVar;
  const q = schema.queryCountVar;
  const noMatch = schema.noMatchOutput;

  // ── Pattern A: Numbered command dispatch ──────────────────────────────────
  if (schema.pattern === 'numbered_commands') {
    const typeIsInt = schema.commands.every(c => /^[0-9]$/.test(c.token));
    const cases = schema.commands.map((cmd, i) => {
      const hasArg = cmd.argTypes.includes('int64');
      const snippet = opSnippet(cmd.semanticOp, schema.container, `v${i}`, noMatch);
      const cond = typeIsInt ? `type == ${cmd.token}` : `cmd == "${cmd.token}"`;
      return `        if (${cond}) { ${snippet} }`;
    }).join('\n        else ');

    const readType = typeIsInt
      ? `int type; if (!(cin >> type)) break;`
      : `string cmd; if (!(cin >> cmd)) break;`;

    return [
      includeStr,
      'using namespace std;',
      'int main() {',
      '    ios_base::sync_with_stdio(false);',
      '    cin.tie(NULL);',
      `    long long ${n}, ${q};`,
      `    if (!(cin >> ${n} >> ${q})) return 0;`,
      `    ${decl}`,
      `    for (long long i = 0; i < ${n}; i++) { long long x; if (cin >> x) s.insert(x); }`,
      `    while (${q}--) {`,
      `        ${readType}`,
      `        ${cases}`,
      '    }',
      '    return 0;',
      '}',
    ].join('\n') + '\n';
  }

  // ── Pattern B: Batch queries ───────────────────────────────────────────────
  if (schema.pattern === 'batch_queries') {
    const batchOp = schema.commands[0]?.semanticOp;
    if (!batchOp) return null;

    if (batchOp === 'floor_remove') {
      return [
        includeStr,
        'using namespace std;',
        'int main() {',
        '    ios_base::sync_with_stdio(false);',
        '    cin.tie(NULL);',
        `    long long ${n}, ${q};`,
        `    if (!(cin >> ${n} >> ${q})) return 0;`,
        `    ${decl}`,
        `    for (long long i = 0; i < ${n}; i++) { long long x; if (cin >> x) s.insert(x); }`,
        `    for (long long i = 0; i < ${q}; i++) {`,
        '        long long t; if (!(cin >> t)) break;',
        '        auto it = s.upper_bound(t);',
        `        if (it == s.begin()) cout << ${noMatch} << "\\n";`,
        '        else { --it; cout << *it << "\\n"; s.erase(it); }',
        '    }',
        '    return 0;',
        '}',
      ].join('\n') + '\n';
    }

    if (batchOp === 'ceiling_remove') {
      return [
        includeStr,
        'using namespace std;',
        'int main() {',
        '    ios_base::sync_with_stdio(false);',
        '    cin.tie(NULL);',
        `    long long ${n}, ${q};`,
        `    if (!(cin >> ${n} >> ${q})) return 0;`,
        `    ${decl}`,
        `    for (long long i = 0; i < ${n}; i++) { long long x; if (cin >> x) s.insert(x); }`,
        `    for (long long i = 0; i < ${q}; i++) {`,
        '        long long t; if (!(cin >> t)) break;',
        '        auto it = s.lower_bound(t);',
        `        if (it == s.end()) cout << ${noMatch} << "\\n";`,
        '        else { cout << *it << "\\n"; s.erase(it); }',
        '    }',
        '    return 0;',
        '}',
      ].join('\n') + '\n';
    }
  }

  return null;
}

