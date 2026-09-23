"""
CHUP Phase 3O — String Algorithms & Automata Blind Holdout Evaluation.

Evaluates 12 unseen, real-world domain problem formulations with rich contextual vocabulary
across the string algorithms domain:
1. STR-BH-01: Genome Sequence Motif Search (KMP)
2. STR-BH-02: Network Packet Header Inspection (Z-Algorithm)
3. STR-BH-03: Plagiarism Document Fingerprint Matcher (Rabin-Karp)
4. STR-BH-04: DNA Inverted Repeat Hairpin Analysis (Manacher)
5. STR-BH-05: Intrusion Detection Virus Signature Scanning (Aho-Corasick)
6. STR-BH-06: Genome Suffix Indexing & Longest Repeated Factor (Suffix Array)
7. STR-BH-07: Cryptographic String Unique Token Counter (Suffix Automaton)
8. STR-BH-08: Circular DNA Sequence Canonical Representative (Duval Lyndon)
9. STR-BH-09: Genomic Protein Subsequence Query Engine (Subsequence Automaton)
10. STR-BH-10: Comparative Genomics Longest Synteny Block (SAM LCS)
11. STR-BH-11: Log Stream Exact Error Code Scanner (KMP)
12. STR-BH-12: Multi-Keyword Firewall Packet Filtering (Aho-Corasick)
"""

import sys
import os
import subprocess
import tempfile
import hashlib
from typing import Dict, Any, List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pointer_algorithms.bridge import handle_request

COMPILED_BINARIES: Dict[str, str] = {}


def compile_and_run_cpp(code: str, stdin_data: str, timeout: int = 10) -> str:
    code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
    exe = COMPILED_BINARIES.get(code_hash)
    if not exe or not os.path.exists(exe):
        tmp_cpp = tempfile.NamedTemporaryFile(suffix=".cpp", delete=False)
        tmp_cpp.write(code.encode("utf-8"))
        tmp_cpp.close()
        exe = tmp_cpp.name[:-4]
        compile_res = subprocess.run(
            ["g++", "-std=c++17", "-O2", tmp_cpp.name, "-o", exe],
            capture_output=True, text=True
        )
        if compile_res.returncode != 0:
            return f"COMPILE_ERROR: {compile_res.stderr[:200]}"
        COMPILED_BINARIES[code_hash] = exe
    try:
        run_res = subprocess.run(
            [exe], input=stdin_data, capture_output=True, text=True, timeout=timeout
        )
        if run_res.returncode != 0:
            return f"RUNTIME_ERROR: {run_res.stderr[:200]}"
        return run_res.stdout.strip()
    except subprocess.TimeoutExpired:
        return "RUNTIME_ERROR: TimeoutExpired"


BLIND_HOLDOUT_PROBLEMS = [
    {
        "id": "STR-BH-01",
        "title": "Genome Sequence Motif Search",
        "text": "Find all exact occurrences of gene regulatory motif in genomic strand using Knuth-Morris-Pratt prefix function.",
        "expected_pattern": "string_kmp_search",
        "input": "attgcatcagattg attg",
        "expected_output": "0 10"
    },
    {
        "id": "STR-BH-02",
        "title": "Network Packet Header Inspection",
        "text": "Calculate longest common prefix between packet header prefix and every suffix using Z-box algorithm.",
        "expected_pattern": "string_z_algorithm",
        "input": "abcabxabc",
        "expected_output": "9 0 0 2 0 0 3 0 0"
    },
    {
        "id": "STR-BH-03",
        "title": "Plagiarism Document Fingerprint Matcher",
        "text": "Search for fingerprint passage within thesis document text using Rabin-Karp polynomial rolling hash.",
        "expected_pattern": "string_rabin_karp",
        "input": "deepmindadvancedcoding deepmind",
        "expected_output": "0"
    },
    {
        "id": "STR-BH-04",
        "title": "DNA Inverted Repeat Hairpin Analysis",
        "text": "Find the longest palindromic substring in the nucleotide sequence using Manacher algorithm in linear time.",
        "expected_pattern": "string_manacher",
        "input": "gatcctag",
        "expected_output": "8\ngatcctag"
    },
    {
        "id": "STR-BH-05",
        "title": "Intrusion Detection Virus Signature Scanning",
        "text": "Scan network stream against multiple malicious virus signature keywords simultaneously using Aho-Corasick automaton with failure links.",
        "expected_pattern": "string_aho_corasick",
        "input": "3\ntrojan\nworm\nvirus\nthecomputervirusandworm",
        "expected_output": "0\n1\n1"
    },
    {
        "id": "STR-BH-06",
        "title": "Genome Suffix Indexing & Longest Repeated Factor",
        "text": "Construct lexicographically sorted suffix array and compute LCP array using prefix doubling and Kasai algorithm.",
        "expected_pattern": "string_suffix_array",
        "input": "gattaca",
        "expected_output": "6 4 1 5 0 3 2\n1 1 0 0 0 1"
    },
    {
        "id": "STR-BH-07",
        "title": "Cryptographic String Unique Token Counter",
        "text": "Count total number of distinct substrings present in cipher text using Suffix Automaton SAM.",
        "expected_pattern": "string_suffix_automaton",
        "input": "ciphertoken",
        "expected_output": "65"
    },
    {
        "id": "STR-BH-08",
        "title": "Circular DNA Sequence Canonical Representative",
        "text": "Determine the lexicographically minimal rotation of circular bacterial plasmid using Duval's algorithm.",
        "expected_pattern": "string_lyndon_duval",
        "input": "ttagcat",
        "expected_output": "agcattt"
    },
    {
        "id": "STR-BH-09",
        "title": "Genomic Protein Subsequence Query Engine",
        "text": "Process multiple peptide subsequence existence queries against target protein using subsequence automaton.",
        "expected_pattern": "string_subsequence_automaton",
        "input": "proteinseq\n2\npts\nxyz",
        "expected_output": "YES\nNO"
    },
    {
        "id": "STR-BH-10",
        "title": "Comparative Genomics Longest Synteny Block",
        "text": "Identify the longest common contiguous substring between two chromosomes using Suffix Automaton SAM.",
        "expected_pattern": "string_longest_common_substring_sam",
        "input": "chromatid chromatogram",
        "expected_output": "7\nchromat"
    },
    {
        "id": "STR-BH-11",
        "title": "Log Stream Exact Error Code Scanner",
        "text": "Find occurrences of fatal error substring in server log stream using KMP prefix function pi table.",
        "expected_pattern": "string_kmp_search",
        "input": "error404notfoundfatalerror404 fatalerror404",
        "expected_output": "16"
    },
    {
        "id": "STR-BH-12",
        "title": "Multi-Keyword Firewall Packet Filtering",
        "text": "Match multiple blacklisted domain keywords in URL text simultaneously using Aho-Corasick automaton.",
        "expected_pattern": "string_aho_corasick",
        "input": "2\nspam\nphish\nantiaphishingspamfilter",
        "expected_output": "1\n1"
    }
]


def run_blind_holdout():
    total = len(BLIND_HOLDOUT_PROBLEMS)
    passed = 0
    failed = 0

    print("=" * 80)
    print(f"CHUP Phase 3O — String Algorithms Blind Holdout Evaluation ({total} Problems)")
    print("=" * 80)

    for p in BLIND_HOLDOUT_PROBLEMS:
        pid = p["id"]
        title = p["title"]
        text = p["text"]
        expected_pat = p["expected_pattern"]
        stdin_data = p["input"]
        expected_output = p["expected_output"]

        resp = handle_request({"problemText": text})
        selected_pat = resp.get("selectedPattern")
        family = resp.get("family")
        code = resp.get("code", "")

        if selected_pat != expected_pat:
            print(f"{pid} FAIL: Pattern mismatch: expected {expected_pat}, got {selected_pat} ({title})")
            failed += 1
            continue

        if family != "string":
            print(f"{pid} FAIL: Family mismatch: expected 'string', got {family} ({title})")
            failed += 1
            continue

        if not code:
            print(f"{pid} FAIL: No C++ code generated ({title})")
            failed += 1
            continue

        cpp_output = compile_and_run_cpp(code, stdin_data)

        if cpp_output.startswith("COMPILE_ERROR") or cpp_output.startswith("RUNTIME_ERROR"):
            print(f"{pid} FAIL: Execution error: {cpp_output} ({title})")
            failed += 1
            continue

        # Match check
        if expected_pat == "string_manacher" or expected_pat == "string_longest_common_substring_sam":
            exp_lines = expected_output.strip().splitlines()
            act_lines = cpp_output.strip().splitlines()
            match = (exp_lines[0].strip() == act_lines[0].strip()) if exp_lines and act_lines else False
        else:
            match = (cpp_output.strip() == expected_output.strip())

        if match:
            passed += 1
            print(f"{pid} PASS: {title} (Pattern={expected_pat})")
        else:
            failed += 1
            print(f"{pid} FAIL: Output mismatch: expected '{expected_output}', got '{cpp_output}' ({title})")

    print("=" * 80)
    print(f"Blind Holdout Results: {passed}/{total} Passed ({(passed/total)*100:.1f}%)")
    print("=" * 80)
    return passed == total


if __name__ == "__main__":
    success = run_blind_holdout()
    sys.exit(0 if success else 1)
