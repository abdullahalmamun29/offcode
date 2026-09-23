/**
 * CHUP V2 — Composition Engine.
 *
 * Discovers and constructs valid algorithmic pipelines through state-transition
 * reasoning:
 *
 *   Initial States (data structure)
 *         ↓
 *   Find concepts whose preconditions (requires) are satisfied
 *         ↓
 *   Concept produces new state(s)
 *         ↓
 *   Feed new states into downstream concepts
 *         ↓
 *   Verify 100% operation coverage
 *
 * If all required operations are satisfied by a valid ordered pipeline:
 *   → StrategyPlan (mode: 'composed', steps: [...])
 * Else:
 *   → StrategyPlan (mode: 'compound_unsupported', uncoveredOperations: [...])
 */

import {
  ProblemRequirements,
  RequiredOperation,
  StrategyPlan,
  StrategyStep,
  DiagnosticTraceEntry,
  KnowledgeConcept
} from '../models/problemSpec';
import {
  canSatisfyPreconditions,
  getAllUnifiedConcepts
} from '../knowledge/compositionKnowledge';

export function composePipeline(
  requirements: ProblemRequirements,
  excludedConceptIds?: Set<string>
): StrategyPlan {
  const diagnosticTrace: DiagnosticTraceEntry[] = [];

  // Determine initial state from data structure
  const availableStates = new Set<string>();
  if (requirements.dataStructure === 'grid') {
    availableStates.add('grid');
    availableStates.add('graph_unweighted');
  } else if (requirements.dataStructure === 'graph_unweighted') {
    availableStates.add('graph_unweighted');
  } else if (requirements.dataStructure === 'graph_weighted') {
    availableStates.add('graph_weighted');
  } else if (requirements.dataStructure === 'intervals') {
    availableStates.add('intervals');
    availableStates.add('sequence');
  } else {
    availableStates.add('sequence');
  }

  // If problem statement indicates sequence is already sorted
  if (requirements.requiresSorted && !requirements.operations.includes('sorting')) {
    availableStates.add('sorted_sequence');
  }

  const initialStates = Array.from(availableStates);
  const remainingOps = new Set<RequiredOperation>(requirements.operations);
  const steps: StrategyStep[] = [];
  const usedConceptIds = new Set<string>();

  // Filter unified concepts based on explicit implementation constraints & exclusions
  let candidatePool = getAllUnifiedConcepts();
  if (excludedConceptIds && excludedConceptIds.size > 0) {
    candidatePool = candidatePool.filter(c => !excludedConceptIds.has(c.id));
  }
  if (requirements.implementationConstraint === 'manual_array' || requirements.implementationConstraint === 'manual') {
    candidatePool = candidatePool.filter(c => !c.isSTL);
  }

  // State-transition search: up to 5 steps
  let progress = true;
  while (remainingOps.size > 0 && progress && steps.length < 5) {
    progress = false;

    // Find eligible concepts whose preconditions are currently met
    const eligible = candidatePool.filter(c =>
      !usedConceptIds.has(c.id) &&
      canSatisfyPreconditions(availableStates, c.requires)
    );

    // Record precondition evaluations in diagnostic trace
    for (const c of candidatePool) {
      if (usedConceptIds.has(c.id)) continue;
      const isEligible = eligible.includes(c);
      const matchesNeededOp = c.satisfies.some(op => remainingOps.has(op));
      if (matchesNeededOp || isEligible) {
        diagnosticTrace.push({
          requirement: c.satisfies.filter(op => remainingOps.has(op)).join(', ') || 'state_transition',
          candidate: c.id,
          accepted: isEligible && matchesNeededOp,
          reason: isEligible
            ? (matchesNeededOp ? `Preconditions [${c.requires.join(', ')}] met; directly satisfies required operations` : `Preconditions [${c.requires.join(', ')}] met but does not directly satisfy remaining operations`)
            : `Preconditions [${c.requires.join(', ')}] not satisfied by current available states [${Array.from(availableStates).join(', ')}]`,
          requiredStates: c.requires,
          availableStates: Array.from(availableStates),
          producedStates: c.produces,
          complexityAssessment: c.complexity?.time
        });
      }
    }

    // Prioritize concepts that satisfy the most currently needed operations
    let chosenConcept: KnowledgeConcept | undefined;
    const directCandidates = eligible
      .map(c => ({
        concept: c,
        matchedOps: c.satisfies.filter(op => remainingOps.has(op))
      }))
      .filter(item => item.matchedOps.length > 0)
      .sort((a, b) => b.matchedOps.length - a.matchedOps.length);

    if (directCandidates.length > 0) {
      chosenConcept = directCandidates[0].concept;
    }

    // If no concept directly satisfies an operation, check if an eligible concept
    // produces a state needed by a concept that satisfies an unsatisfied operation (lookahead)
    if (!chosenConcept) {
      for (const candidate of eligible) {
        // Hypothesize adding candidate's produced states
        const hypotheticalStates = new Set(availableStates);
        candidate.produces.forEach(st => hypotheticalStates.add(st));

        const downstream = candidatePool.find(down =>
          !usedConceptIds.has(down.id) &&
          down.id !== candidate.id &&
          down.satisfies.some(op => remainingOps.has(op)) &&
          canSatisfyPreconditions(hypotheticalStates, down.requires)
        );

        if (downstream) {
          chosenConcept = candidate;
          diagnosticTrace.push({
            requirement: downstream.satisfies.filter(op => remainingOps.has(op)).join(', '),
            candidate: candidate.id,
            accepted: true,
            reason: `Intermediate transformation: produces [${candidate.produces.join(', ')}] to satisfy downstream concept '${downstream.id}' preconditions [${downstream.requires.join(', ')}]`,
            requiredStates: candidate.requires,
            availableStates: Array.from(availableStates),
            producedStates: candidate.produces,
            complexityAssessment: candidate.complexity?.time
          });
          break;
        }
      }
    }

    if (chosenConcept) {
      const satisfiedNow = chosenConcept.satisfies.filter(op => remainingOps.has(op));
      for (const op of satisfiedNow) {
        remainingOps.delete(op);
      }

      for (const st of chosenConcept.produces) {
        availableStates.add(st);
      }

      usedConceptIds.add(chosenConcept.id);
      steps.push({
        conceptId: chosenConcept.id,
        satisfies: satisfiedNow,
        produces: [...chosenConcept.produces]
      });

      progress = true;
    }
  }

  const finalStates = Array.from(availableStates);
  const uncoveredOperations = Array.from(remainingOps);
  const coveredOperations = requirements.operations.filter(op => !remainingOps.has(op));

  if (uncoveredOperations.length === 0 && steps.length > 0) {
    const pipelineStr = steps
      .map(s => `${s.conceptId} [produces: ${s.produces.join(', ')}]`)
      .join(' → ');

    return {
      mode: 'composed',
      steps,
      initialStates,
      finalStates,
      coveredOperations,
      uncoveredOperations: [],
      reasoning: `Composition pipeline discovered: ${pipelineStr}. Satisfies operations [${coveredOperations.join(', ')}].`,
      diagnosticTrace
    };
  }

  // If operations remain unsatisfied
  for (const uncov of uncoveredOperations) {
    diagnosticTrace.push({
      requirement: uncov,
      candidate: 'none',
      accepted: false,
      reason: `No supported concept currently produces the required state or satisfies operation '${uncov}' on current data structure (${requirements.dataStructure}).`,
      availableStates: finalStates
    });
  }

  return {
    mode: 'compound_unsupported',
    steps: [],
    initialStates,
    finalStates,
    coveredOperations,
    uncoveredOperations,
    reasoning: `Unsatisfiable requirements: [${uncoveredOperations.join(', ')}]. No supported concept or state transition satisfies these operations on current data structure (${requirements.dataStructure}).`,
    diagnosticTrace
  };
}
