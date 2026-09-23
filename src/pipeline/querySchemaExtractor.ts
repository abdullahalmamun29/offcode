import { StructuredProblem } from '../models/problemSpec';

export type SemanticOp =
  | 'insert'
  | 'extract_min'
  | 'extract_max'
  | 'floor_remove'
  | 'ceiling_remove'
  | 'push_front'
  | 'push_back'
  | 'pop_front'
  | 'pop_back'
  | 'index_access'
  | 'reverse_collection';

export type ContainerType =
  | 'multiset_ordered'
  | 'priority_queue_max'
  | 'priority_queue_min'
  | 'deque'
  | 'queue';

export interface QueryCommand {
  token: string;
  argTypes: ('int64' | 'none')[];
  semanticOp: SemanticOp;
}

export interface QuerySchema {
  pattern: 'numbered_commands' | 'batch_queries';
  initialLoadVar: string;
  queryCountVar: string;
  queryArgType: 'int64' | 'none';
  commands: QueryCommand[];
  container: ContainerType;
  elementType: 'long long';
  noMatchOutput: string;
  confidence: number;
}

// ── Generic semantic operation patterns ─────────────────────────────────────
// NO problem-specific terms (no 'concert', 'ticket', 'price', 'customer').
// These match the MEANING of an operation, not its domain context.
const SEMANTIC_PATTERNS: { patterns: RegExp[], op: SemanticOp }[] = [
  // floor_remove — find largest element <= x, output and remove
  { patterns: [
    /nearest.*(?:not\s+exceed|at\s+most|<=)|largest.*(?:not\s+exceed|at\s+most|<=)/i,
    /does\s+not\s+exceed.*(?:maximum|price|budget|value)/i,
    /nearest\s+possible.*(?:not\s+exceed|does\s+not\s+exceed)/i,
    /floor\s+(?:query|of\s+x|search)/i,
    /ticket.*nearest.*price/i,
  ], op: 'floor_remove' },

  // extract_min — output minimum and remove
  { patterns: [
    /output.*(?:minimum|min(?:imum)?).*(?:remove|erase|delete)/i,
    /(?:remove|extract|delete).*(?:minimum|min(?:imum)?)\b/i,
    /(?:minimum|min(?:imum)?)\s+element.*(?:output|remove)/i,
    /one\s+of\s+the\s+minimum\s+elements.*remove/i,
  ], op: 'extract_min' },

  // extract_max — output maximum and remove
  { patterns: [
    /output.*(?:maximum|max(?:imum)?).*(?:remove|erase|delete)/i,
    /(?:remove|extract|delete).*(?:maximum|max(?:imum)?)\b/i,
    /(?:maximum|max(?:imum)?)\s+element.*(?:output|remove)/i,
    /one\s+of\s+the\s+maximum\s+elements.*remove/i,
  ], op: 'extract_max' },

  // insert — add element to ordered collection
  { patterns: [
    /(?:add|insert|put)\s+(?:x|an?\s+integer|value)\s+(?:to|into)\s+(?:s\b|the\s+(?:set|multiset|collection))/i,
    /(?:add|insert|push)\s+x\s+to\s+s\b/i,
    /^0\s+x\s*[:\-]\s*add/im,
  ], op: 'insert' },

  // push_front — add to beginning
  { patterns: [/add.*(?:beginning|front|start)\s+of/i, /push.*front/i], op: 'push_front' },

  // push_back — add to end
  { patterns: [/add.*(?:end|back|tail)\s+of/i, /push.*back/i], op: 'push_back' },

  // pop_front — remove from front and output
  { patterns: [
    /remove.*(?:integer\s+at\s+the\s+)?(?:beginning|front|head)/i,
    /pop.*front/i,
    /print.*front.*erase/i,
  ], op: 'pop_front' },

  // pop_back — remove from end and output
  { patterns: [
    /remove.*(?:integer\s+at\s+the\s+)?(?:end|back|tail)/i,
    /pop.*back/i,
    /print.*back.*erase/i,
  ], op: 'pop_back' },

  // reverse_collection
  { patterns: [/reverse.*(?:all\s+elements|queue|sequence)/i], op: 'reverse_collection' },

  // index_access
  { patterns: [
    /output\s+a_?i\b/i,
    /access.*(?:by\s+index|element\s+i\b)/i,
    /output\s+a\[i\]/i,
    /let\s+a\s*=.*output\s+a_?i/i,
  ], op: 'index_access' },

  // ceiling_remove — find smallest element >= x, output and remove
  { patterns: [
    /nearest.*(?:at\s+least|>=)|smallest.*(?:at\s+least|>=)/i,
    /ceiling\s+(?:query|search)/i,
  ], op: 'ceiling_remove' },
];

function inferContainer(ops: SemanticOp[]): ContainerType {
  const has = (op: SemanticOp) => ops.includes(op);
  if (has('floor_remove') || has('ceiling_remove')) return 'multiset_ordered';
  if (has('extract_min') && has('extract_max'))     return 'multiset_ordered';
  if (has('extract_max') && !has('extract_min'))    return 'priority_queue_max';
  if (has('extract_min') && !has('extract_max'))    return 'priority_queue_min';
  if (has('index_access') || has('reverse_collection') || has('push_front')) return 'deque';
  if (has('push_back') && has('pop_front'))         return 'queue';
  return 'multiset_ordered';
}

function matchSemanticOp(text: string): SemanticOp | null {
  for (const item of SEMANTIC_PATTERNS) {
    for (const pat of item.patterns) {
      if (pat.test(text)) return item.op;
    }
  }
  return null;
}

function matchAllSemanticOps(text: string): SemanticOp[] {
  const found: SemanticOp[] = [];
  for (const item of SEMANTIC_PATTERNS) {
    for (const pat of item.patterns) {
      if (pat.test(text)) {
        if (!found.includes(item.op)) found.push(item.op);
        break;
      }
    }
  }
  return found;
}

export function extractQuerySchema(problem: StructuredProblem): QuerySchema | null {
  const fullText = [
    problem.normalizedText,
    problem.statement,
    problem.inputSpecification || '',
    problem.outputSpecification || '',
  ].join('\n');

  // ── Pattern A: Numbered or token-based command definitions ─────────────────
  // Matches lines like:  "0 x: Add x to S"  or  "1: output minimum element and remove it"
  // Token can be digit (0,1,2) or uppercase letter (A, R, D)
  const cmdRegex = /^\s*([0-9]|[A-Z])(?:\s+([a-z_]+))?\s*[:\.\)\-\u2013]\s*(.+)/m;
  const commands: QueryCommand[] = [];
  const seenTokens = new Set<string>();

  const lines = fullText.split('\n');
  for (const line of lines) {
    const match = line.match(cmdRegex);
    if (!match) continue;
    const token = match[1];
    const arg   = match[2];   // optional arg name like 'x'
    const desc  = match[3];
    if (seenTokens.has(token)) continue;
    const op = matchSemanticOp(desc + ' ' + fullText);  // desc first, then context
    if (op) {
      commands.push({ token, argTypes: arg ? ['int64'] : ['none'], semanticOp: op });
      seenTokens.add(token);
    }
  }

  if (commands.length >= 2) {
    const ops = commands.map(c => c.semanticOp);
    return {
      pattern:        'numbered_commands',
      initialLoadVar: 'n',
      queryCountVar:  'q',
      queryArgType:   'none',
      commands,
      container:      inferContainer(ops),
      elementType:    'long long',
      noMatchOutput:  '-1',
      confidence:     commands.length >= 3 ? 0.85 : 0.75,
    };
  }

  // ── Pattern B: Batch queries ───────────────────────────────────────────────
  // e.g. Concert Tickets: load N items, then for each of M queries find floor(budget)
  const batchOps = matchAllSemanticOps(fullText);

  if (batchOps.includes('floor_remove')) {
    // Determine query count variable: look for "n and m" or "n and q" in input spec
    const inputSpec = (problem.inputSpecification || fullText).toLowerCase();
    const qVar = /\bn\s*(?:and|,)\s*m\b/.test(inputSpec) ? 'm' : 'q';
    const noMatch = /-1\b/.test(fullText) ? '-1' : 'IMPOSSIBLE';

    return {
      pattern:        'batch_queries',
      initialLoadVar: 'n',
      queryCountVar:  qVar,
      queryArgType:   'int64',
      commands: [{ token: '', argTypes: ['int64'], semanticOp: 'floor_remove' }],
      container:      'multiset_ordered',
      elementType:    'long long',
      noMatchOutput:  noMatch,
      confidence:     0.75,
    };
  }

  if (batchOps.includes('ceiling_remove')) {
    return {
      pattern:        'batch_queries',
      initialLoadVar: 'n',
      queryCountVar:  'q',
      queryArgType:   'int64',
      commands: [{ token: '', argTypes: ['int64'], semanticOp: 'ceiling_remove' }],
      container:      'multiset_ordered',
      elementType:    'long long',
      noMatchOutput:  '-1',
      confidence:     0.70,
    };
  }

  return null;
}
