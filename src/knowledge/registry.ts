import * as fs from 'fs';
import * as path from 'path';

export interface KnowledgeEntry {
  id: string;
  name: string;
  aliases?: string[];
  verified?: boolean;
  moduleId?: string;
  action?: string;
  position?: string;
  runtime_input?: boolean;
}

export interface StructureInfo {
  id: string;
  name?: string;
  displayName?: string;
  aliases?: string[];
  operations: KnowledgeEntry[];
}

export interface AlgorithmInfo {
  methods: KnowledgeEntry[];
}

export interface NumericalInfo {
  methods: KnowledgeEntry[];
}

const registry = {
  dataStructures: new Map<string, StructureInfo>(),
  algorithms: new Map<string, AlgorithmInfo>(),
  numerical: new Map<string, NumericalInfo>()
};

function loadJsonFiles(dir: string): any[] {
  const result: any[] = [];
  if (!fs.existsSync(dir)) return result;
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (file.endsWith('.json')) {
      const content = fs.readFileSync(path.join(dir, file), 'utf-8');
      result.push(JSON.parse(content));
    }
  }
  return result;
}

export function loadRegistry() {
  const candidateDirs = [
    __dirname,
    path.join(__dirname, '..', '..', 'src', 'knowledge'),
    path.join(__dirname, '..', 'knowledge'),
    path.join(__dirname, '..', '..', 'knowledge')
  ];
  const baseDir = candidateDirs.find(d => fs.existsSync(path.join(d, 'data_structures'))) || path.join(__dirname, '..', '..', 'src', 'knowledge');
  
  const dsDir = path.join(baseDir, 'data_structures');
  const dsData = loadJsonFiles(dsDir);
  for (const ds of dsData) {
    registry.dataStructures.set(ds.id, ds as StructureInfo);
  }

  const algDir = path.join(baseDir, 'algorithms');
  const algData = loadJsonFiles(algDir);
  for (const alg of algData) {
    if (alg.id) {
      registry.algorithms.set(alg.id, alg as AlgorithmInfo);
    }
  }

  const numDir = path.join(baseDir, 'numerical');
  const numData = loadJsonFiles(numDir);
  for (const num of numData) {
    if (num.id) {
      registry.numerical.set(num.id, num as NumericalInfo);
    }
  }
}

// Ensure registry is loaded on import
loadRegistry();

export function getStructureInfo(structureId: string): StructureInfo | null {
  if (registry.dataStructures.has(structureId)) {
    return registry.dataStructures.get(structureId)!;
  }
  const clean = structureId.replace(/_/g, ' ').toLowerCase();
  for (const ds of registry.dataStructures.values()) {
    if (ds.id.toLowerCase() === structureId.toLowerCase()) return ds;
    if (ds.aliases && ds.aliases.some((a: string) => a.toLowerCase() === clean || a.toLowerCase() === structureId.toLowerCase())) {
      return ds;
    }
  }
  return null;
}

export function isStructureKnown(structureId: string): boolean {
  return getStructureInfo(structureId) !== null;
}

export function isOperationKnown(structureId: string, operationId: string): boolean {
  const ds = getStructureInfo(structureId);
  if (!ds) return false;
  return ds.operations.some(op => op.id === operationId || (op.aliases && op.aliases.includes(operationId)) || op.action === operationId);
}

export function lookupDataStructureOp(structureId: string, operationId: string): KnowledgeEntry | null {
  const ds = getStructureInfo(structureId);
  if (!ds) return null;
  return ds.operations.find(op => op.id === operationId || (op.aliases && op.aliases.includes(operationId)) || op.action === operationId) || null;
}

export function lookupAlgorithm(algorithmId: string): KnowledgeEntry | null {
  for (const algGroup of registry.algorithms.values()) {
    const method = algGroup.methods?.find(m => m.id === algorithmId);
    if (method) return method;
  }
  return null;
}

export function lookupNumericalMethod(methodId: string): KnowledgeEntry | null {
  for (const numGroup of registry.numerical.values()) {
    const method = numGroup.methods?.find(m => m.id === methodId);
    if (method) return method;
  }
  return null;
}
