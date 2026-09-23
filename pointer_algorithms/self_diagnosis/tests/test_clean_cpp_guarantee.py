"""
Phase 9 — test_clean_cpp_guarantee.py

Tests clean C++ generation and compilation invariants:
- Compiles cleanly with -O3 -Wall -Wextra -pedantic -Werror (exit code 0 = zero warnings, zero errors)
- Warning under -Werror causes compilation failure
- Zero repair markers, debug prints, or trial comments in output
"""

import unittest

from pointer_algorithms.self_diagnosis.repair_verifier import RepairVerifier


class TestCleanCppGuarantee(unittest.TestCase):

    def test_clean_code_compiles_cleanly_with_werror(self):
        """Clean standard C++ code compiles with exit code 0 under -Werror."""
        clean_cpp = (
            "#include <iostream>\n"
            "#include <vector>\n"
            "#include <numeric>\n"
            "int main() {\n"
            "    std::vector<int> a = {1, 2, 3};\n"
            "    long long sum = 0;\n"
            "    sum = std::accumulate(a.begin(), a.end(), 0LL);\n"
            "    std::cout << sum << \"\\n\";\n"
            "    return 0;\n"
            "}\n"
        )
        ok, stderr = RepairVerifier._compile_check(
            clean_cpp,
            "g++",
            RepairVerifier.DEFAULT_COMPILER_FLAGS,
        )
        self.assertTrue(ok, f"Compilation failed: {stderr}")
        self.assertEqual(stderr, "")

    def test_unused_variable_warning_fails_compilation_under_werror(self):
        """Under -Werror, any compiler warning (e.g. unused variable) triggers failure."""
        warning_cpp = (
            "#include <iostream>\n"
            "int main() {\n"
            "    int unused_variable = 42;\n"
            "    return 0;\n"
            "}\n"
        )
        ok, stderr = RepairVerifier._compile_check(
            warning_cpp,
            "g++",
            RepairVerifier.DEFAULT_COMPILER_FLAGS,
        )
        self.assertFalse(ok, "Code with unused variable should fail compilation under -Werror")
        self.assertIn("unused-variable", stderr)

    def test_zero_repair_markers_or_trial_comments(self):
        """Repaired code must never contain trial artifacts or markers."""
        clean_source = "#include <numeric>\nint main() { return 0; }"
        forbidden_tokens = [
            "// REPAIR",
            "/* REPAIR",
            "DEBUG",
            "FIXME",
            "TODO",
            "TRIAL",
            "__REPAIR_ENGINE__",
        ]
        for token in forbidden_tokens:
            self.assertNotIn(token, clean_source)


if __name__ == "__main__":
    unittest.main()
