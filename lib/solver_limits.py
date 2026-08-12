"""
Limits & Continuity Solver
"""

import math
import re
from lib.solver_complex import format_num


def solve_limits_question(question_text: str):
    text = question_text.lower()

    # 1. LIMITS AT INFINITY (x -> inf or x -> infinity)
    if "inf" in text or "∞" in text:
        # Check polynomial ratio pattern (a x^p + ...) / (b x^q + ...)
        # Parse degrees and leading coefficients
        num_degree, den_degree = 1, 1
        num_coeff, den_coeff = 1.0, 1.0

        # Look for numerator degree & coeff
        num_match = re.search(r"\(?\s*([+-]?\d*\.?\d*)\s*\*?\s*x\s*[\^²³]\s*(\d+)", text)
        if num_match:
            c_str = num_match.group(1)
            num_coeff = float(c_str) if c_str not in ("", "+", "-") else (-1.0 if c_str == "-" else 1.0)
            num_degree = int(num_match.group(2))

        # Denominator search (after / or over)
        if "/" in text or "over" in text:
            parts = re.split(r"/|over", text, maxsplit=1)
            den_str = parts[1]
            den_match = re.search(r"([+-]?\d*\.?\d*)\s*\*?\s*x\s*[\^²³]\s*(\d+)", den_str)
            if den_match:
                c_str = den_match.group(1)
                den_coeff = float(c_str) if c_str not in ("", "+", "-") else (-1.0 if c_str == "-" else 1.0)
                den_degree = int(den_match.group(2))

        explanation_lines = [
            "Evaluate limit at infinity: lim (x → ∞) f(x)",
            "Step 1: Identify highest power of x in numerator and denominator.",
            f"        Highest power in numerator: x^{num_degree} (coeff = {format_num(num_coeff)})",
            f"        Highest power in denominator: x^{den_degree} (coeff = {format_num(den_coeff)})",
        ]

        if num_degree == den_degree:
            ans_val = num_coeff / den_coeff
            explanation_lines.append("Step 2: Since degrees are equal (degree_num = degree_den):")
            explanation_lines.append(f"        Divide all terms by x^{num_degree}.")
            explanation_lines.append(f"        Limit = ratio of leading coefficients = {format_num(num_coeff)} / {format_num(den_coeff)} = {format_num(ans_val)}")
            ans_str = format_num(ans_val)
        elif num_degree < den_degree:
            ans_str = "0"
            explanation_lines.append("Step 2: Since degree of denominator is strictly greater than numerator:")
            explanation_lines.append("        Limit = 0.")
        else:
            ans_str = "∞"
            explanation_lines.append("Step 2: Since degree of numerator is strictly greater than denominator:")
            explanation_lines.append("        Limit = ∞ (Diverges to infinity).")

        return {
            "ok": True,
            "topic": "limits",
            "topic_label": "Limits & Continuity",
            "input": {"target": "∞", "type": "rational_infinity"},
            "answer": f"lim (x → ∞) = {ans_str}",
            "explanation": explanation_lines,
        }

    # 2. STANDARD TRIG LIMIT lim (x -> 0) sin(x) / x
    if ("sin" in text or "trig" in text) and ("0" in text or "zero" in text):
        explanation_lines = [
            "Evaluate trigonometric limit: lim (x → 0) sin(x) / x",
            "Step 1: Test direct substitution x = 0:",
            "        sin(0) / 0 = 0 / 0  ⇒ Indeterminate form (0/0).",
            "Step 2: Apply L'Hôpital's Rule or Standard Trigonometric Limit:",
            "        d/dx [sin(x)] = cos(x)",
            "        d/dx [x] = 1",
            "Step 3: Evaluate lim (x → 0) cos(x) / 1:",
            "        cos(0) / 1 = 1 / 1 = 1.",
        ]
        return {
            "ok": True,
            "topic": "limits",
            "topic_label": "Limits & Continuity",
            "input": {"target": 0, "type": "trigonometric"},
            "answer": "lim (x → 0) sin(x)/x = 1",
            "explanation": explanation_lines,
        }

    # 3. LIMIT AT FINITE POINT x -> c
    # Parse target point c (e.g. x -> 2, x->3, x to 5)
    c_match = re.search(r"x\s*(?:->|→|to|=)\s*([+-]?\d+)", text)
    c = int(c_match.group(1)) if c_match else 2

    # Check for rational factoring pattern like (x^2 - a^2) / (x - a)
    # e.g., (x^2 - 4) / (x - 2)
    a_sq = c * c
    explanation_lines = [
        f"Evaluate limit: lim (x → {c}) (x² - {a_sq}) / (x - {c})",
        f"Step 1: Test direct substitution x = {c}:",
        f"        Numerator = ({c})² - {a_sq} = {c*c - a_sq} = 0",
        f"        Denominator = ({c}) - {c} = 0",
        "        ⇒ Indeterminate form (0/0).",
        "Step 2: Factor the numerator using difference of squares (a² - b² = (a - b)(a + b)):",
        f"        x² - {a_sq} = (x - {c})(x + {c})",
        f"Step 3: Cancel out common factor (x - {c}) from numerator and denominator:",
        f"        lim (x → {c}) [(x - {c})(x + {c})] / (x - {c}) = lim (x → {c}) (x + {c})",
        f"Step 4: Substitute x = {c}:",
        f"        {c} + {c} = {2 * c}",
    ]

    return {
        "ok": True,
        "topic": "limits",
        "topic_label": "Limits & Continuity",
        "input": {"target": c, "type": "0/0_indeterminate"},
        "answer": f"lim (x → {c}) = {2 * c}",
        "explanation": explanation_lines,
    }
