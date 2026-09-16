/**
 * CodeForge Test Suite Runner.
 */

import { runResolverTests } from "./resolver.test";
import { runGeneratorTests } from "./generator.test";
import { runPythonBridgeTests } from "./parser.test";

async function main() {
  console.log("=================================================");
  console.log("      CodeForge TypeScript Test Suite Runner     ");
  console.log("=================================================");

  const resResolver = runResolverTests();
  const resGenerator = runGeneratorTests();
  const resBridge = await runPythonBridgeTests();

  const totalPassed = resResolver.passed + resGenerator.passed + resBridge.passed;
  const totalFailed = resResolver.failed + resGenerator.failed + resBridge.failed;

  console.log("\n=================================================");
  console.log(`Summary: ${totalPassed} passed, ${totalFailed} failed.`);
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
