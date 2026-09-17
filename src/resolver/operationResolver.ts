import { ProblemSpecV1, ResolutionResult } from '../models/problemSpec';
import { getStructureInfo, isStructureKnown, isOperationKnown, lookupDataStructureOp, lookupAlgorithm, lookupNumericalMethod } from '../knowledge/registry';

export function resolveProblemSpec(spec: ProblemSpecV1): ResolutionResult {
  if (spec.status === 'negated') {
    return { code: 'NEGATED', message: 'Negated operation', spec };
  }
  if (spec.status === 'question' || spec.intent === 'conceptual_question') {
    return { code: 'QUESTION', message: 'Conceptual question', spec };
  }
  if (spec.compound.is_compound || spec.error_code === 'UNSUPPORTED_COMPOUND_PROBLEM') {
    return { code: 'COMPOUND_UNSUPPORTED', message: 'Compound unsupported', spec };
  }
  if (spec.status === 'ambiguous') {
    return { code: 'AMBIGUOUS', message: spec.message || 'Ambiguous', spec };
  }

  if (spec.domain === 'numerical') {
    return resolveNumerical(spec);
  } else if (spec.domain === 'algorithm') {
    return resolveAlgorithm(spec);
  } else {
    return resolveDataStructure(spec);
  }
}

function resolveNumerical(spec: ProblemSpecV1): ResolutionResult {
  if (spec.generation_mode === 'menu' || spec.operation.combined === 'menu' || spec.numerical?.method === 'menu') {
    return {
      code: 'SUCCESS',
      moduleId: 'numerical.menu.cpp',
      moduleName: 'Numerical Methods Menu',
      message: 'Resolved numerical methods menu program',
      spec,
      generationMode: 'menu',
      operations: spec.menu_operations || undefined
    };
  }
  const method = spec.numerical.method;
  if (!method) return { code: 'UNSUPPORTED_OPERATION', message: 'Unknown method', spec };
  const entry = lookupNumericalMethod(method);
  if (!entry) return { code: 'UNSUPPORTED_OPERATION', message: 'Method unsupported', spec };
  return { code: 'SUCCESS', moduleId: entry.moduleId, moduleName: entry.name, message: 'Resolved', spec };
}

function resolveAlgorithm(spec: ProblemSpecV1): ResolutionResult {
  const structType = spec.structure.type;
  if (!structType) return { code: 'UNSUPPORTED_OPERATION', message: 'Unknown algo', spec };
  const entry = lookupAlgorithm(structType);
  if (!entry) return { code: 'UNSUPPORTED_OPERATION', message: 'Algo unsupported', spec };
  return { code: 'SUCCESS', moduleId: entry.moduleId, moduleName: entry.name, message: 'Resolved', spec };
}

function resolveDataStructure(spec: ProblemSpecV1): ResolutionResult {
  const structType = spec.structure.type;
  if (!structType) return { code: 'UNSUPPORTED_STRUCTURE', message: 'Unknown structure', spec };
  const structInfo = getStructureInfo(structType);
  if (!structInfo) return { code: 'UNSUPPORTED_STRUCTURE', message: 'Structure unsupported', spec };
  const canonicalId = structInfo.id;
  spec.structure.type = canonicalId;
  
  if (spec.generation_mode === 'menu' || spec.operation.combined === 'menu') {
    return {
      code: 'SUCCESS',
      moduleId: `${canonicalId}.menu.cpp`,
      moduleName: `${structInfo.displayName} Menu`,
      message: 'Resolved menu-driven program',
      spec,
      generationMode: 'menu',
      operations: spec.menu_operations || undefined
    };
  }

  if (canonicalId === 'polynomial') {
    return {
      code: 'SUCCESS',
      moduleId: 'polynomial.add.cpp',
      moduleName: 'Polynomial Addition (Linked List)',
      message: 'Resolved polynomial addition',
      spec
    };
  }

  const op = spec.operation.combined;
  if (!op) return { code: 'UNSUPPORTED_OPERATION', message: 'Unknown operation', spec };
  
  const entry = lookupDataStructureOp(structType, op);
  if (!entry) return { code: 'UNSUPPORTED_OPERATION', message: 'Operation unsupported', spec };
  
  return { code: 'SUCCESS', moduleId: entry.moduleId, moduleName: entry.name, message: 'Resolved', spec };
}
