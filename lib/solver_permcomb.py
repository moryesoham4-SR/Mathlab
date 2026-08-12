"""
Permutations & Combinations Solver
"""

import math
import re
from collections import Counter


def solve_permcomb_question(question_text: str):
    text = question_text.lower()

    # 1. ANAGRAM / WORD REARRANGEMENT
    # Look for "arrange the letters of WORD" or "permutations of WORD"
    word_match = re.search(r"(?:arrange|permutations? of|word|letters in|letters of)\s+['\"]?([a-zA-Z]{3,})['\"]?", text)
    if word_match and not any(kw in text for kw in ["p(", "c(", "npr", "ncr"]):
        word = word_match.group(1).upper()
        n = len(word)
        counts = Counter(word)
        repeat_counts = {char: count for char, count in counts.items() if count > 1}
        
        explanation_lines = [
            f"Calculate the number of distinct permutations of the word '{word}'.",
            f"Step 1: Total number of letters n = {n}.",
        ]

        if not repeat_counts:
            ans = math.factorial(n)
            explanation_lines.append(f"Step 2: All letters are unique, so number of arrangements = {n}! = {ans}.")
        else:
            explanation_lines.append(f"Step 2: Count repeated letters:")
            denom_terms = []
            denom_val = 1
            for char, count in repeat_counts.items():
                explanation_lines.append(f"        Letter '{char}' appears {count} times ({count}!).")
                denom_terms.append(f"{count}!")
                denom_val *= math.factorial(count)
                
            num_val = math.factorial(n)
            ans = num_val // denom_val
            
            denom_str = " × ".join(denom_terms)
            explanation_lines.append(f"Step 3: Apply multiset permutation formula: n! / (n₁! × n₂! × ...)")
            explanation_lines.append(f"        Total arrangements = {n}! / ({denom_str})")
            explanation_lines.append(f"        = {num_val} / {denom_val} = {ans}")

        return {
            "ok": True,
            "topic": "permcomb",
            "topic_label": "Permutations & Combinations",
            "input": {"type": "anagram", "word": word, "length": n},
            "answer": f"The number of distinct arrangements of '{word}' is {ans}.",
            "explanation": explanation_lines,
        }

    # 2. PARSE N and R FOR P(n, r) or C(n, r) OR FACTORIAL
    # Look for P(n,r), nPr, P(n, r), 7P3
    p_match = re.search(r"p\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)|(\d+)\s*p\s*(\d+)", text)
    c_match = re.search(r"c\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)|(\d+)\s*c\s*(\d+)|(?:choose|select)\s+(\d+)\s+from\s+(\d+)", text)
    fact_match = re.search(r"(\d+)\s*!|factorial of\s+(\d+)", text)

    is_combination = "combination" in text or "choose" in text or "select" in text or c_match is not None
    is_permutation = "permutation" in text or "arrange" in text or p_match is not None

    if p_match:
        n = int(p_match.group(1) or p_match.group(3))
        r = int(p_match.group(2) or p_match.group(4))
        is_permutation = True
    elif c_match:
        if c_match.group(1):
            n, r = int(c_match.group(1)), int(c_match.group(2))
        elif c_match.group(3):
            n, r = int(c_match.group(3)), int(c_match.group(4))
        else:
            r, n = int(c_match.group(5)), int(c_match.group(6))
        is_combination = True
    elif fact_match and not (is_combination or is_permutation):
        n = int(fact_match.group(1) or fact_match.group(2))
        ans = math.factorial(n)
        explanation_lines = [
            f"Calculate factorial of {n} ({n}!):",
            f"Step 1: {n}! = " + " × ".join(str(i) for i in range(n, 0, -1)),
            f"Step 2: {n}! = {ans}",
        ]
        return {
            "ok": True,
            "topic": "permcomb",
            "topic_label": "Permutations & Combinations",
            "input": {"type": "factorial", "n": n},
            "answer": f"{n}! = {ans}",
            "explanation": explanation_lines,
        }
    else:
        # Fallback: extract two integers from prompt
        nums = [int(m) for m in re.findall(r"\d+", text)]
        if len(nums) >= 2:
            n, r = max(nums[0], nums[1]), min(nums[0], nums[1])
        else:
            n, r = 7, 3

    if r > n:
        return {
            "ok": False,
            "topic": "permcomb",
            "topic_label": "Permutations & Combinations",
            "error": f"Invalid inputs: r ({r}) cannot be greater than n ({n}).",
        }

    explanation_lines = []

    # 3. COMBINATIONS C(n, r)
    if is_combination or not is_permutation:
        ans = math.comb(n, r)
        n_fact = math.factorial(n)
        r_fact = math.factorial(r)
        nr_fact = math.factorial(n - r)

        explanation_lines.append(f"Calculate Combinations C({n}, {r}) [or ⁿCᵣ]:")
        explanation_lines.append(f"Step 1: Apply formula C(n, r) = n! / [r! × (n - r)!]")
        explanation_lines.append(f"        C({n}, {r}) = {n}! / [{r}! × ({n} - {r})!]")
        explanation_lines.append(f"        = {n}! / [{r}! × {n - r}!]")
        
        # Product reduction trace
        num_terms = [str(i) for i in range(n, n - r, -1)]
        den_terms = [str(i) for i in range(r, 0, -1)]
        explanation_lines.append(f"Step 2: Cancel out ({n - r})! from numerator and denominator:")
        explanation_lines.append(f"        Numerator = " + " × ".join(num_terms))
        explanation_lines.append(f"        Denominator = " + " × ".join(den_terms))
        explanation_lines.append(f"Step 3: Divide numerator by denominator:")
        explanation_lines.append(f"        C({n}, {r}) = {ans}")

        return {
            "ok": True,
            "topic": "permcomb",
            "topic_label": "Permutations & Combinations",
            "input": {"type": "combination", "n": n, "r": r},
            "answer": f"C({n}, {r}) = {ans}",
            "explanation": explanation_lines,
        }

    # 4. PERMUTATIONS P(n, r)
    ans = math.perm(n, r)
    explanation_lines.append(f"Calculate Permutations P({n}, {r}) [or ⁿPᵣ]:")
    explanation_lines.append(f"Step 1: Apply formula P(n, r) = n! / (n - r)!")
    explanation_lines.append(f"        P({n}, {r}) = {n}! / ({n} - {r})! = {n}! / {n - r}!")
    
    num_terms = [str(i) for i in range(n, n - r, -1)]
    explanation_lines.append(f"Step 2: Cancel out ({n - r})! from numerator:")
    explanation_lines.append(f"        P({n}, {r}) = " + " × ".join(num_terms))
    explanation_lines.append(f"Step 3: Multiply terms:")
    explanation_lines.append(f"        P({n}, {r}) = {ans}")

    return {
        "ok": True,
        "topic": "permcomb",
        "topic_label": "Permutations & Combinations",
        "input": {"type": "permutation", "n": n, "r": r},
        "answer": f"P({n}, {r}) = {ans}",
        "explanation": explanation_lines,
    }
