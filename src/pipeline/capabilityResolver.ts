/**
 * CHUP / Offcode — Evidence-Based Capability Resolver (Phase 4)
 *
 * Implements capability-first resolution from structured SemanticInput.
 *
 * Invariants:
 * - Domain classification is NOT consulted anywhere in this pipeline.
 * - Explicit algorithm identity dominates generic objective phrases (dijkstra > shortest path).
 * - Operations, representations, and positions are extracted as attributes, not separate capabilities.
 * - Ambiguity is explicit: generic requests without algorithm or constraint disambiguation produce CAPABILITY_AMBIGUOUS.
 * - Conflicts are explicit: incompatible constraints produce CAPABILITY_CONFLICT.
 * - Unsupported requests fail closed: CAPABILITY_UNSUPPORTED without default CP fallback.
 */

import {
  CapabilityRequest,
  CapabilityEvidence,
  CapabilityMatch,
  CapabilityRequestStatus,
  CapabilityFailureCode,
  CapabilityFailureLayer
} from '../models/capabilityModel';
import { SemanticInput, StructuredProblem } from '../models/problemSpec';
import { CAPABILITY_REGISTRY, AuthoritativeCapabilityRegistry } from './capabilityCatalog';

export interface ResolverOptions {
  registry?: AuthoritativeCapabilityRegistry;
  allowAmbiguity?: boolean;
}

export function resolveCapabilityRequest(
  semantic: SemanticInput,
  problem?: StructuredProblem,
  options?: ResolverOptions
): CapabilityRequest {
  const registry = options?.registry || CAPABILITY_REGISTRY;
  const fullText = semantic.normalizedText.toLowerCase();

  const evidenceList: CapabilityEvidence[] = [];
  const candidateScores = new Map<string, { score: number; algorithms: Set<string>; evidence: CapabilityEvidence[] }>();

  // 1. Evidence Extraction from Semantic Entities & Canonical Terms
  for (const entity of semantic.entities) {
    const term = entity.value.toLowerCase().replace(/_/g, ' ');
    const directResolution = registry.resolveAlias(term) || registry.resolveAlias(entity.value);

    if (directResolution) {
      const capId = directResolution.capability?.id || directResolution.algorithm?.capabilityId;
      if (capId) {
        const evidence: CapabilityEvidence = {
          sourceText: semantic.originalText.slice(entity.startToken, entity.endToken) || entity.value,
          normalizedText: entity.value,
          evidenceType: directResolution.algorithm ? 'explicit_identifier' : 'objective',
          capabilityId: capId,
          algorithmId: directResolution.algorithm?.id,
          strength: directResolution.algorithm ? 1.0 : 0.85,
          tokenSpan: [entity.startToken, entity.endToken]
        };
        evidenceList.push(evidence);

        if (!candidateScores.has(capId)) {
          candidateScores.set(capId, { score: 0, algorithms: new Set(), evidence: [] });
        }
        const record = candidateScores.get(capId)!;
        record.score += evidence.strength;
        if (directResolution.algorithm) {
          record.algorithms.add(directResolution.algorithm.id);
        }
        record.evidence.push(evidence);
      }
    }
  }

  // 2. Direct Algorithm / Capability Alias Scanning across Tokens
  const allAlgorithms = registry.getAllAlgorithms();
  for (const algo of allAlgorithms) {
    for (const alias of algo.aliases) {
      const pattern = new RegExp(`\\b${alias.replace(/[-_]/g, '\\s+')}\\b`, 'i');
      if (pattern.test(fullText)) {
        const tokenCount = alias.trim().split(/\s+/).length;
        const weight = 1.0 + (tokenCount - 1) * 0.5;
        const capId = algo.capabilityId;
        const evidence: CapabilityEvidence = {
          sourceText: alias,
          normalizedText: alias,
          evidenceType: 'explicit_identifier',
          capabilityId: capId,
          algorithmId: algo.id,
          strength: weight,
          tokenSpan: [0, semantic.tokens.length]
        };
        evidenceList.push(evidence);

        if (!candidateScores.has(capId)) {
          candidateScores.set(capId, { score: 0, algorithms: new Set(), evidence: [] });
        }
        const record = candidateScores.get(capId)!;
        record.score += weight;
        record.algorithms.add(algo.id);
        record.evidence.push(evidence);
      }
    }
  }

  // Also scan canonical capability aliases
  const allCaps = registry.getAllCapabilities();
  for (const cap of allCaps) {
    for (const alias of cap.aliases) {
      const pattern = new RegExp(`\\b${alias.replace(/[-_]/g, '\\s+')}\\b`, 'i');
      if (pattern.test(fullText)) {
        const tokenCount = alias.trim().split(/\s+/).length;
        const weight = 0.80 + (tokenCount - 1) * 0.5;
        const evidence: CapabilityEvidence = {
          sourceText: alias,
          normalizedText: alias,
          evidenceType: 'objective',
          capabilityId: cap.id,
          strength: weight,
          tokenSpan: [0, semantic.tokens.length]
        };
        evidenceList.push(evidence);

        if (!candidateScores.has(cap.id)) {
          candidateScores.set(cap.id, { score: 0, algorithms: new Set(), evidence: [] });
        }
        const record = candidateScores.get(cap.id)!;
        record.score += weight;
        record.evidence.push(evidence);
      }
    }
  }

  // 3. Extract Operations & Attributes Independently
  const operations: string[] = [];
  for (const op of semantic.operations) {
    if (!operations.includes(op.operation)) {
      operations.push(op.operation);
    }
  }
  for (const intent of semantic.intents) {
    if (!operations.includes(intent.intent)) {
      operations.push(intent.intent);
    }
  }
  if (operations.length === 0) {
    operations.push('solve');
  }

  // Extract positional and representation attributes
  let position: string | undefined;
  for (const c of semantic.constraints) {
    if (c.type === 'position') {
      position = c.value;
      break;
    }
  }

  let stlAllowed: boolean | undefined;
  if (/without\s+stl|manually|no\s+stl|without\s+using\s+stl/i.test(fullText)) {
    stlAllowed = false;
  } else if (/using\s+stl|with\s+stl/i.test(fullText)) {
    stlAllowed = true;
  }

  let representation: string | undefined;
  if (/pointer\s*based|pointers/i.test(fullText)) {
    representation = 'pointer_based';
  } else if (/array\s*based|using\s+array/i.test(fullText)) {
    representation = 'array_based';
  }

  // Extract weight and graph attributes
  let weight: 'weighted' | 'unweighted' | 'nonnegative' | 'negative' | undefined;
  if (/non[\s-]*negative/i.test(fullText) || /positive\s+weights?/i.test(fullText)) {
    weight = 'nonnegative';
  } else if (/negative\s+(?:edge\s+)?weights?|negative\s+edges?|negative\s+cycles?/i.test(fullText)) {
    weight = 'negative';
  } else if (/weighted/i.test(fullText)) {
    weight = 'weighted';
  } else if (/unweighted/i.test(fullText)) {
    weight = 'unweighted';
  }

  const attributes = {
    position,
    representation,
    stlAllowed,
    weight,
    negativeWeights: weight === 'negative'
  };

  // 4. Resolve Candidate Capabilities & Dominance Rules
  if (candidateScores.has('single_source_shortest_path') && /shortest\s+path/i.test(fullText)) {
    candidateScores.delete('graph_traversal');
  }
  if (candidateScores.has('connected_components') && /connected\s+components/i.test(fullText)) {
    candidateScores.delete('graph_traversal');
  }
  if (candidateScores.has('topological_sort')) {
    candidateScores.delete('sort');
    candidateScores.delete('graph_traversal');
  }
  if (candidateScores.has('minimum_spanning_tree')) {
    candidateScores.delete('graph_traversal');
  }
  if (candidateScores.has('binary_search')) {
    candidateScores.delete('sort');
  }

  const sortedCandidates = Array.from(candidateScores.entries())
    .sort((a, b) => b[1].score - a[1].score);

  const resolvedCapabilities: string[] = [];
  const matches: CapabilityMatch[] = [];
  let primaryAlgorithmId: string | undefined;

  for (const [capId, data] of sortedCandidates) {
    const capDef = registry.getCapability(capId);
    if (!capDef) continue;

    // Determine chosen algorithm: prefer an algorithm belonging to THIS capability matching query
    let chosenAlgoId: string | undefined;
    for (const aId of capDef.algorithms) {
      const algoDef = registry.getAlgorithm(aId);
      if (!algoDef) continue;
      for (const alias of algoDef.aliases) {
        const pattern = new RegExp(`\\b${alias.replace(/[-_]/g, '\\s+')}\\b`, 'i');
        if (pattern.test(fullText)) {
          chosenAlgoId = aId;
          break;
        }
      }
      if (chosenAlgoId) break;
    }

    // Secondary fallback: check matched algorithms from data
    if (!chosenAlgoId && data.algorithms.size > 0) {
      chosenAlgoId = Array.from(data.algorithms)[0];
    }

    // Contextual algorithm heuristics if explicit alias wasn't found
    if (!chosenAlgoId && capId === 'single_source_shortest_path') {
      if (/bfs|breadth\s+first|unweighted/i.test(fullText)) {
        chosenAlgoId = 'bfs_shortest_path';
      } else if (/bellman|negative/i.test(fullText)) {
        chosenAlgoId = 'bellman_ford';
      } else {
        chosenAlgoId = 'dijkstra';
      }
    } else if (!chosenAlgoId && capId === 'topological_sort') {
      if (/dfs|postorder/i.test(fullText)) {
        chosenAlgoId = 'dfs_topological_sort';
      } else {
        chosenAlgoId = 'kahn_algorithm';
      }
    } else if (!chosenAlgoId && capId === 'connected_components') {
      if (/dsu|disjoint\s+set|union/i.test(fullText)) {
        chosenAlgoId = 'dsu_connected_components';
      } else {
        chosenAlgoId = 'bfs_connected_components';
      }
    }

    // Default algorithm fallback
    if (!chosenAlgoId && capDef.algorithms.length > 0) {
      chosenAlgoId = capDef.algorithms[0];
    }

    if (!primaryAlgorithmId && chosenAlgoId) {
      primaryAlgorithmId = chosenAlgoId;
    }

    resolvedCapabilities.push(capId);
    matches.push({
      capabilityId: capId,
      algorithmId: chosenAlgoId,
      evidence: data.evidence,
      source: chosenAlgoId ? 'direct_mention' : 'objective_inference',
      resolutionPath: [capId, ...(chosenAlgoId ? [chosenAlgoId] : [])],
      confidence: Math.min(1.0, data.score)
    });
  }

  // 5. Evaluate Multi-Layer Failure Modes: Conflict, Ambiguity, Unsupported

  let status: CapabilityRequestStatus = 'CAPABILITY_RESOLVED';
  let failureCode: CapabilityFailureCode | undefined;
  let failureLayer: CapabilityFailureLayer | undefined;
  let failureMessage: string | undefined;
  let ambiguousCandidates: string[] | undefined;
  let conflictReason: string | undefined;

  // Check 5.1: Incompatible Constraints & Preconditions -> CAPABILITY_CONFLICT
  if (
    (primaryAlgorithmId === 'dijkstra' || fullText.includes('dijkstra')) &&
    (weight === 'negative' || (/(?<!non-?)(?:negative\s+(?:edge\s+)?weights?|negative\s+cycle)/i.test(fullText) && weight !== 'nonnegative'))
  ) {
    status = 'CAPABILITY_CONFLICT';
    failureCode = 'CAPABILITY_CONFLICT';
    failureLayer = 'CAPABILITY_RESOLUTION';
    conflictReason = "Dijkstra's algorithm requires non-negative edge weights; cannot be used with negative weights or negative cycles.";
    failureMessage = conflictReason;
  } else if (/topological\s+sort/i.test(fullText) && /(?<!a)cyclic|with\s+cycles?/i.test(fullText)) {
    status = 'CAPABILITY_CONFLICT';
    failureCode = 'CAPABILITY_CONFLICT';
    failureLayer = 'CAPABILITY_RESOLUTION';
    conflictReason = "Topological sort requires a directed acyclic graph (DAG); cannot be applied to cyclic graphs.";
    failureMessage = conflictReason;
  } else if (/binary\s+search/i.test(fullText) && /unsorted|unordered|arbitrary\s+array/i.test(fullText)) {
    status = 'CAPABILITY_CONFLICT';
    failureCode = 'CAPABILITY_CONFLICT';
    failureLayer = 'CAPABILITY_RESOLUTION';
    conflictReason = "Binary search requires monotonic sorted domain; cannot be performed on unsorted arrays.";
    failureMessage = conflictReason;
  } else if (/bisection/i.test(fullText) && /same\s+sign|no\s+sign\s+change/i.test(fullText)) {
    status = 'CAPABILITY_CONFLICT';
    failureCode = 'CAPABILITY_CONFLICT';
    failureLayer = 'CAPABILITY_RESOLUTION';
    conflictReason = "Bisection method requires bracketed root with opposing signs f(a)*f(b) < 0.";
    failureMessage = conflictReason;
  } else if (/\bstack\b/i.test(fullText) && (/\bfifo\b/i.test(fullText) || /first\s+in\s+first\s+out/i.test(fullText))) {
    status = 'CAPABILITY_CONFLICT';
    failureCode = 'CAPABILITY_CONFLICT';
    failureLayer = 'CAPABILITY_RESOLUTION';
    conflictReason = "Stack is strictly a LIFO structure; cannot satisfy FIFO discipline.";
    failureMessage = conflictReason;
  } else if (/\bqueue\b/i.test(fullText) && (/\blifo\b/i.test(fullText) || /last\s+in\s+first\s+out/i.test(fullText))) {
    status = 'CAPABILITY_CONFLICT';
    failureCode = 'CAPABILITY_CONFLICT';
    failureLayer = 'CAPABILITY_RESOLUTION';
    conflictReason = "Queue is strictly a FIFO structure; cannot satisfy LIFO discipline.";
    failureMessage = conflictReason;
  }
  // Check 5.2: Generic Objective without Algorithm Disambiguation -> CAPABILITY_AMBIGUOUS
  else if (
    /^\s*(?:find\s+)?shortest\s+path\s*$/i.test(fullText) ||
    (resolvedCapabilities.includes('single_source_shortest_path') && !primaryAlgorithmId && !weight && !/bfs|dijkstra|bellman/i.test(fullText))
  ) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['dijkstra', 'bfs_shortest_path', 'bellman_ford'];
    failureMessage = `Generic shortest path requested without explicit algorithm or edge-weight specifications. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/^\s*search(?:\s+for\s+value)?\s*$/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['binary_search', 'singly_linked_list', 'bst'];
    failureMessage = `Generic search requested without target data structure or ordered domain. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/^\s*sort(?:\s+elements)?\s*$/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['standard_sort', 'merge_sort', 'quick_sort'];
    failureMessage = `Generic sort requested without explicit algorithm. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/traverse\s+graph(?:\s+nodes)?/i.test(fullText) && !/bfs|dfs/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['graph_bfs', 'graph_dfs'];
    failureMessage = `Generic graph traversal requested without traversal discipline. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/optimal\s+spanning\s+tree/i.test(fullText) && !/kruskal|prim/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['kruskal', 'prim'];
    failureMessage = `Generic spanning tree requested without algorithm choice. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/find\s+cycle\s+in\s+graph|cycle\s+in\s+graph/i.test(fullText) && !/directed|undirected|dfs|dsu/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['dfs_directed_cycle', 'dsu_undirected_cycle'];
    failureMessage = `Cycle detection requested without graph directedness. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/evaluate\s+root\s+of\s+function/i.test(fullText) && !/bisection|newton|secant/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['bisection', 'newton_raphson', 'secant'];
    failureMessage = `Root finding requested without algorithm method. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  } else if (/query\s+range\s+in\s+array/i.test(fullText) && !/prefix|fenwick|segment|static|update/i.test(fullText)) {
    status = 'CAPABILITY_AMBIGUOUS';
    failureCode = 'CAPABILITY_AMBIGUOUS';
    failureLayer = 'CAPABILITY_RESOLUTION';
    ambiguousCandidates = ['prefix_sum', 'binary_indexed_tree', 'segment_tree'];
    failureMessage = `Range query requested without static/dynamic update specifications. Plausible candidates: ${ambiguousCandidates.join(', ')}.`;
  }
  // Check 5.3: Explicitly Unsupported Algorithmic Domains -> CAPABILITY_UNSUPPORTED
  else if (
    (!/linked\s*list/i.test(fullText) && /detect\s+cycle|cycle\s+detection|find\s+cycle\s+in\s+(?:directed|undirected)\s+graph/i.test(fullText)) ||
    /bipartite/i.test(fullText) ||
    /longest\s+increasing\s+subsequence|\blis\b/i.test(fullText) ||
    /all\s*pairs\s+shortest\s+path|floyd\s+warshall/i.test(fullText) ||
    /bridges\s+in\s+graph|tarjan/i.test(fullText)
  ) {
    status = 'CAPABILITY_UNSUPPORTED';
    failureCode = 'CAPABILITY_UNSUPPORTED';
    failureLayer = 'CAPABILITY_RESOLUTION';
    failureMessage = `Requested algorithmic capability is unsupported: "${semantic.normalizedText}"`;
    resolvedCapabilities.length = 0;
    matches.length = 0;
    primaryAlgorithmId = undefined;
  }
  // Check 5.4: Zero Candidates -> CAPABILITY_UNSUPPORTED
  else if (resolvedCapabilities.length === 0) {
    status = 'CAPABILITY_UNSUPPORTED';
    failureCode = 'CAPABILITY_UNSUPPORTED';
    failureLayer = 'CAPABILITY_RESOLUTION';
    failureMessage = `No registered capability matched the input query: "${semantic.normalizedText}"`;
  }

  // Aggregate domain metadata from all resolved capabilities (METADATA ONLY!)
  const domainMetadataSet = new Set<string>();
  for (const capId of resolvedCapabilities) {
    const cap = registry.getCapability(capId);
    if (cap) {
      for (const d of cap.domains) domainMetadataSet.add(d);
    }
  }

  return {
    capabilities: resolvedCapabilities,
    primaryAlgorithmId,
    operations,
    attributes,
    representations: representation ? [representation] : (stlAllowed === false ? ['pointer_based', 'array_based'] : ['stl', 'pointer_based']),
    parameters: {},
    constraints: semantic.constraints.map(c => `${c.type}:${c.value}`),
    requiredStates: resolvedCapabilities.flatMap(c => registry.getCapability(c)?.requiredStates || []),
    producedStates: resolvedCapabilities.flatMap(c => registry.getCapability(c)?.producedStates || []),
    domains: Array.from(domainMetadataSet),
    evidence: evidenceList,
    matches,
    unresolved: [],
    status,
    failureCode,
    failureLayer,
    failureMessage,
    ambiguousCandidates,
    conflictReason
  };
}
