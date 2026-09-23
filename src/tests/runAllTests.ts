/**
 * CodeForge Test Suite Runner (V1 + V2).
 */

import { runResolverTests } from "./resolver.test";
import { runGeneratorTests } from "./generator.test";
import { runPythonBridgeTests } from "./parser.test";
import { runV2PipelineTests } from "./v2Pipeline.test";
import { runCompositionTests } from "./composition.test";
import { runStlTests } from "./stl.test";
import { runTwoPointersDomainTests } from "./twoPointersDomain.test";
import { runBatch3ExpansionTests } from "./batch3Expansion.test";
import { runRuntimeResolutionTests } from "./runtimeResolution.test";
import { runExplanationIpcTests } from "./explanationIpc.test";
import { runAdversarialGeneralizationTests } from "./adversarialGeneralization.test";
import { runSelfDiagnosisTests } from "./selfDiagnosis.test";
import { runResearchReasoningTests } from "./researchReasoning.test";
import { runUniversalNormalizerTests } from "./universalNormalizer.test";
import { runFuzzyMatcherTests } from "./fuzzyMatcher.test";
import { runSemanticExtractionTests } from "./semanticExtraction.test";
import { runCapabilityScoringTests } from "./capabilityScoring.test";
import { runCapabilityRoutingTests } from "./capabilityRouting.test";
import { runPhase4Benchmark } from "./phase4Benchmark";
import { runPhase5BackendIntegrationTests } from "./phase5BackendIntegration.test";
import { runAdversarialNormalizationTests } from "./adversarialNormalization.test";

async function main() {
  console.log("=================================================");
  console.log("   CHUP Runtime Resolution Test Suite            ");
  console.log("=================================================");

  const resRuntime = await runRuntimeResolutionTests();

  console.log("\n=================================================");
  console.log("      CodeForge V1 TypeScript Test Suite Runner   ");
  console.log("=================================================");

  const resResolver = runResolverTests();
  const resGenerator = runGeneratorTests();
  const resBridge = await runPythonBridgeTests();

  const v1Passed = resResolver.passed + resGenerator.passed + resBridge.passed;
  const v1Failed = resResolver.failed + resGenerator.failed + resBridge.failed;

  console.log(`\nV1 Summary: ${v1Passed} passed, ${v1Failed} failed.`);

  console.log("\n=================================================");
  console.log("      CHUP V2 Pipeline Test Suite                ");
  console.log("=================================================");

  const resFuzzy = runFuzzyMatcherTests();
  const resNormalizer = runUniversalNormalizerTests();
  const resSemantic = runSemanticExtractionTests();
  const resCapability = runCapabilityScoringTests();
  const resV2 = runV2PipelineTests();

  console.log(`\nV2 Summary: ${resV2.passed} passed, ${resV2.failed} failed.`);

  const resComp = runCompositionTests();
  console.log(`\nComposition Summary: ${resComp.passed} passed, ${resComp.failed} failed.`);

  const resStl = runStlTests();
  console.log(`\nSTL Summary: ${resStl.passed} passed, ${resStl.failed} failed.`);

  const resTwoPointers = runTwoPointersDomainTests();
  console.log(`\nPointer Algorithms Summary: ${resTwoPointers.totalPassed} passed, ${resTwoPointers.totalFailed} failed.`);

  const resBatch3 = runBatch3ExpansionTests();
  console.log(`\nBatch 3 Expansion Summary: ${resBatch3.passed} passed, ${resBatch3.failed} failed.`);

  console.log("\n=================================================");
  console.log("   CHUP Phase 7 — Explanation IPC & Schema Suite ");
  console.log("=================================================");
  const resExplanation = runExplanationIpcTests();
  console.log(`\nExplanation IPC Summary: ${resExplanation.passed} passed, ${resExplanation.failed} failed.`);

  console.log("\n=================================================");
  console.log("   CHUP Phase 8 — Adversarial Generalization IPC ");
  console.log("=================================================");
  const resAdversarial = runAdversarialGeneralizationTests();
  console.log(`\nAdversarial IPC Summary: ${resAdversarial.passed} passed, ${resAdversarial.failed} failed.`);

  console.log("\n=================================================");
  console.log("   CHUP Phase 9 — Self-Diagnosis & Correction    ");
  console.log("=================================================");
  const resSelfDiagnosis = runSelfDiagnosisTests();
  console.log(`\nSelf-Diagnosis Summary: ${resSelfDiagnosis.passed} passed, ${resSelfDiagnosis.failed} failed.`);

  console.log("\n=================================================");
  console.log("   CHUP Phase 10 — Research-Level Reasoning IPC  ");
  console.log("=================================================");
  const resResearch = runResearchReasoningTests();
  console.log(`\nResearch Reasoning Summary: ${resResearch.passed} passed, ${resResearch.failed} failed.`);

  console.log("\n=================================================");
  console.log("   CHUP Phase 4 — Capability Routing Unit Suite  ");
  console.log("=================================================");
  const resCapabilityRouting = runCapabilityRoutingTests();
  console.log(`\nCapability Routing Summary: ${resCapabilityRouting.passed} passed, ${resCapabilityRouting.failed} failed.`);

  console.log("\n=================================================");
  console.log("   CHUP Phase 4 — Held-Out Benchmark (105 Cases)  ");
  console.log("=================================================");
  const resBenchmark = await runPhase4Benchmark();
  console.log(`\nPhase 4 Benchmark Summary: ${resBenchmark.passed} passed, ${resBenchmark.failed} failed.`);

  const resPhase5 = runPhase5BackendIntegrationTests();
  const resAdvNorm = runAdversarialNormalizationTests();

  const totalPassed = resRuntime.passed + v1Passed + resFuzzy.passed + resNormalizer.passed + resSemantic.passed + resCapability.passed + resV2.passed + resComp.passed + resStl.passed + resTwoPointers.totalPassed + resBatch3.passed + resExplanation.passed + resAdversarial.passed + resSelfDiagnosis.passed + resResearch.passed + resCapabilityRouting.passed + resBenchmark.passed + resPhase5.passed + resAdvNorm.passed;
  const totalFailed = resRuntime.failed + v1Failed + resFuzzy.failed + resNormalizer.failed + resSemantic.failed + resCapability.failed + resV2.failed + resComp.failed + resStl.failed + resTwoPointers.totalFailed + resBatch3.failed + resExplanation.failed + resAdversarial.failed + resSelfDiagnosis.failed + resResearch.failed + resCapabilityRouting.failed + resBenchmark.failed + resPhase5.failed + resAdvNorm.failed;

  console.log("\n=================================================");
  console.log(`Total: ${totalPassed} passed, ${totalFailed} failed.`);
  console.log("=================================================\n");

  if (totalFailed > 0) {
    process.exit(1);
  } else {
    process.exit(0);
  }
}

main().catch((err) => {
  console.error("Test runner error:", err);
  process.exit(1);
});

