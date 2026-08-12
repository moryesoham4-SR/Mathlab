"""
De Moivre's Theorem & Nth Roots Solver
"""

import math
import re
from lib.solver_complex import extract_complex_numbers, format_complex, format_num


def solve_demoivre_question(question_text: str):
    text = question_text.lower()

    # Determine if question is asking for nth roots or powers
    is_roots = any(kw in text for kw in ["root", "roots", "z^n", "z**n", "nth root", "cube root", "square root"])
    
    # Extract integer exponent or root degree n
    n_matches = re.findall(r"(?:power|pow|\^|\*\*|degree|roots? of order|roots?|nth)\s*=?\s*(\d+)", text)
    if not n_matches:
        # Check for standalone numbers like "^6" or "6th root" or "cube roots"
        if "cube" in text:
            n = 3
        elif "square" in text:
            n = 2
        elif "fourth" in text or "4th" in text:
            n = 4
        elif "fifth" in text or "5th" in text:
            n = 5
        else:
            match = re.search(r"[\^]\s*(\d+)", text)
            n = int(match.group(1)) if match else 3
    else:
        n = int(n_matches[0])

    # Extract base complex number
    complex_nums = extract_complex_numbers(question_text)
    if complex_nums:
        real, imag = complex_nums[0]
    else:
        # Default to 1 + i or 1 if no complex parsed
        if "i" in text:
            real, imag = 1.0, 1.0
        else:
            real, imag = 1.0, 0.0

    z_str = format_complex(real, imag)
    r = math.hypot(real, imag)
    theta_rad = math.atan2(imag, real)
    theta_deg = math.degrees(theta_rad)

    explanation_lines = []

    if is_roots:
        # 1. N-TH ROOTS OF Z
        explanation_lines.append(f"Find the {n} roots of w = {z_str} using De Moivre's Theorem for Roots.")
        explanation_lines.append(f"Step 1: Convert w to polar form w = r (cos θ + i sin θ)")
        explanation_lines.append(f"        r = √({format_num(real)}² + {format_num(imag)}²) = {format_num(r)}")
        explanation_lines.append(f"        θ = atan2({format_num(imag)}, {format_num(real)}) = {format_num(theta_deg)}° ({format_num(theta_rad)} rad)")
        
        explanation_lines.append(f"Step 2: Formula for the n-th roots zₖ (k = 0, 1, ..., {n-1}):")
        explanation_lines.append(f"        zₖ = ⁿ√r × [cos((θ + 360°k)/n) + i sin((θ + 360°k)/n)]")
        
        r_root = r ** (1.0 / n)
        explanation_lines.append(f"        ⁿ√r = {format_num(r)}^(1/{n}) = {format_num(r_root)}")

        roots_list = []
        explanation_lines.append("Step 3: Calculate each root for k = 0 to n-1:")
        for k in range(n):
            angle_deg = (theta_deg + 360.0 * k) / n
            angle_rad = math.radians(angle_deg)
            root_real = r_root * math.cos(angle_rad)
            root_imag = r_root * math.sin(angle_rad)
            root_str = format_complex(root_real, root_imag)
            roots_list.append(root_str)
            explanation_lines.append(
                f"        k = {k}: angle = ({format_num(theta_deg)}° + 360°×{k})/{n} = {format_num(angle_deg)}° "
                f"⇒ z_{k} = {root_str}"
            )

        ans_str = ", ".join([f"z_{k} = {r_s}" for k, r_s in enumerate(roots_list)])

        return {
            "ok": True,
            "topic": "demoivre",
            "topic_label": "De Moivre's Theorem & Nth Roots",
            "input": {"w": z_str, "n": n, "mode": "roots"},
            "answer": f"The {n} roots of {z_str} are: {ans_str}",
            "explanation": explanation_lines,
            "roots": roots_list,
        }

    # 2. POWER Z^N USING DE MOIVRE
    explanation_lines.append(f"Evaluate ({z_str})^{n} using De Moivre's Theorem.")
    explanation_lines.append(f"Step 1: Convert z = {z_str} to polar form r (cos θ + i sin θ)")
    explanation_lines.append(f"        r = √({format_num(real)}² + {format_num(imag)}²) = {format_num(r)}")
    explanation_lines.append(f"        θ = {format_num(theta_deg)}° ({format_num(theta_rad)} rad)")

    explanation_lines.append(f"Step 2: Apply De Moivre's Theorem: z^{n} = r^{n} [cos({n}θ) + i sin({n}θ)]")
    
    r_n = r ** n
    n_theta_deg = n * theta_deg
    n_theta_rad = math.radians(n_theta_deg)
    
    explanation_lines.append(f"        r^{n} = {format_num(r)}^{n} = {format_num(r_n)}")
    explanation_lines.append(f"        {n}θ = {n} × {format_num(theta_deg)}° = {format_num(n_theta_deg)}°")

    ans_real = r_n * math.cos(n_theta_rad)
    ans_imag = r_n * math.sin(n_theta_rad)
    ans_str = format_complex(ans_real, ans_imag)

    explanation_lines.append(f"Step 3: Convert back to rectangular form a + bi")
    explanation_lines.append(f"        a = {format_num(r_n)} × cos({format_num(n_theta_deg)}°) = {format_num(ans_real)}")
    explanation_lines.append(f"        b = {format_num(r_n)} × sin({format_num(n_theta_deg)}°) = {format_num(ans_imag)}")
    explanation_lines.append(f"        ⇒ ({z_str})^{n} = {ans_str}")

    return {
        "ok": True,
        "topic": "demoivre",
        "topic_label": "De Moivre's Theorem & Nth Roots",
        "input": {"z": z_str, "n": n, "mode": "power"},
        "answer": f"({z_str})^{n} = {ans_str}",
        "explanation": explanation_lines,
    }
