/**
 * Operation Resolver for CodeForge.
 * Validates ProblemSpec and selects verified implementation modules.
 */

import { ProblemSpec, ResolutionResult } from "../models/problemSpec";
import { generateSinglyLinkedListInsertEnd } from "../generator/cppGenerator";

// Registry of verified modules available in the prototype
export interface VerifiedModule {
  id: string;
  name: string;
  structure: string;
  operation: string;
  language: string;
  generate: (spec: ProblemSpec) => string;
}

const VERIFIED_MODULES: Record<string, VerifiedModule> = {
  "singly_linked_list_insert_end_cpp": {
    id: "singly_linked_list_insert_end_cpp",
    name: "Singly Linked List — Insert at End",
    structure: "singly_linked_list",
    operation: "insert_end",
    language: "cpp",
    generate: (spec: ProblemSpec) => generateSinglyLinkedListInsertEnd(spec)
  }
};

/**
 * Resolves a ProblemSpec into a verified module or descriptive rejection.
 */
export function resolveProblemSpec(spec: ProblemSpec): ResolutionResult {
  // Case 1: Compound operations detected
  if (spec.error_code === "UNSUPPORTED_COMPOUND_PROBLEM") {
    return {
      code: "COMPOUND_UNSUPPORTED",
      message: spec.message || "Multiple operations detected. Compound problems are not supported.",
      spec
    };
  }

  // Case 2: Cannot identify (ambiguous, missing structure, empty query)
  if (spec.status === "ambiguous" || !spec.structure || !spec.operation) {
    return {
      code: "CANNOT_IDENTIFY",
      message: spec.message || "CodeForge could not confidently identify the data structure or operation.",
      spec
    };
  }

  // Case 3: Language check
  if (spec.language !== "cpp") {
    return {
      code: "IDENTIFIED_UNSUPPORTED",
      message: `Language '${spec.language}' is not supported yet (CodeForge currently supports C++).`,
      spec
    };
  }

  // Case 4: Check if a verified module exists in registry
  const lookupKey = `${spec.structure}_${spec.operation}_${spec.language}`;
  const verifiedModule = VERIFIED_MODULES[lookupKey];

  if (verifiedModule) {
    return {
      code: "SUCCESS",
      moduleId: verifiedModule.id,
      moduleName: verifiedModule.name,
      message: `Successfully resolved verified module: ${verifiedModule.name}`,
      spec
    };
  }

  // Case 5: Identified structure & operation, but no verified solution available yet
  return {
    code: "IDENTIFIED_UNSUPPORTED",
    message: `Identified target: ${spec.structure} + ${spec.operation}, but CodeForge does not have a verified solution available for this problem in Prototype V0.`,
    spec
  };
}

/**
 * Executes code generation for a resolved result.
 */
export function generateCodeForResolution(resolution: ResolutionResult): string {
  if (resolution.code !== "SUCCESS" || !resolution.moduleId) {
    throw new Error(`Cannot generate code for non-successful resolution: ${resolution.code}`);
  }

  const module = VERIFIED_MODULES[resolution.moduleId];
  if (!module) {
    throw new Error(`Module ${resolution.moduleId} not found in verified registry.`);
  }

  return module.generate(resolution.spec);
}
