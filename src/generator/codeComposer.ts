/**
 * CodeForge C++ Code Composer.
 * Helper utility to assemble clean, beginner-friendly C++ source files.
 */

export interface CodeBlockMetadata {
  title: string;
  structure: string;
  operation: string;
  timeComplexity: string;
  spaceComplexity: string;
  description: string;
}

export function composeHeaderComment(meta: CodeBlockMetadata): string {
  return `/**
 * ============================================================================
 * CodeForge Verified Educational Implementation
 * ============================================================================
 * Problem Statement : ${meta.title}
 * Data Structure    : ${meta.structure}
 * Operation         : ${meta.operation}
 * Time Complexity   : ${meta.timeComplexity}
 * Space Complexity  : ${meta.spaceComplexity}
 *
 * Description:
 *   ${meta.description}
 *
 * Deterministic generation by CodeForge Engine.
 * ============================================================================
 */\n\n`;
}
