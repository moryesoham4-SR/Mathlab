"""
Automated Test Suite for Mathlab Solvers
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from api.solve import build_response

TEST_QUESTIONS = [
    # 1. GCD / Euclidean Algorithm
    ("Find gcd(252, 105) using the Euclidean algorithm", "gcd"),
    ("What is the greatest common divisor of 1071 and 462?", "gcd"),

    # 2. Complex Numbers & Polar Form
    ("Convert 3 + 4i to polar form", "complex"),
    ("Multiply (2 + 3i) * (1 - 4i)", "complex"),
    ("Divide (5 + 2i) / (1 + i)", "complex"),

    # 3. De Moivre's Theorem & Nth Roots
    ("Find (1 + i)^8 using De Moivre's theorem", "demoivre"),
    ("Find the 3 cube roots of 8", "demoivre"),

    # 4. Permutations & Combinations
    ("Calculate 10C4 combinations", "permcomb"),
    ("Calculate P(7, 3) permutations", "permcomb"),
    ("How many distinct arrangements of the letters of MISSISSIPPI", "permcomb"),

    # 5. Injective, Surjective & Bijective Functions
    ("Is f(x) = 2x + 3 injective and surjective from R to R?", "functions"),
    ("Is f(x) = x^2 injective from R to R?", "functions"),

    # 6. Limits & Continuity
    ("Find limit x->2 of (x^2 - 4)/(x - 2)", "limits"),
    ("Find limit x->inf of (3x^2 + 5)/(2x^2 - 1)", "limits"),
    ("Find limit x->0 of sin(x)/x", "limits"),
]

def run_tests():
    print("==================================================")
    print("Running Mathlab 6-Topic Solvers Test Suite...")
    print("==================================================\n")
    
    passed = 0
    failed = 0

    for i, (q, expected_topic) in enumerate(TEST_QUESTIONS, start=1):
        print(f"Test {i}: {q}")
        res = build_response(q)
        
        ok = res.get("ok", False)
        topic = res.get("topic")
        answer = res.get("answer")
        explanation = res.get("explanation", [])
        
        if ok and topic == expected_topic:
            print(f"  ✓ PASSED [Topic: {topic}]")
            print(f"    Answer: {answer}")
            print(f"    Steps count: {len(explanation)}")
            passed += 1
        else:
            print(f"  ✗ FAILED [Expected: {expected_topic}, Got: {topic}]")
            print(f"    Error: {res.get('error')}")
            failed += 1
        print("-" * 50)

    print(f"\nTest Summary: {passed} PASSED, {failed} FAILED out of {len(TEST_QUESTIONS)} tests.")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
