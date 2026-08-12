"""
Complex Numbers & Polar Form Solver
"""

import math
import re


def parse_single_complex(text: str):
    """
    Parses strings like '3 + 4i', '1 - i', '-2.5 + 3i', '4i', '-5', 'sqrt(3) + i'
    Returns tuple (real, imag) or None if parsing fails.
    """
    text = text.lower().replace(" ", "").replace("*i", "i").replace("j", "i")
    text = text.replace("sqrt(3)", "1.7320508").replace("√3", "1.7320508")
    text = text.replace("sqrt(2)", "1.4142135").replace("√2", "1.4142135")
    
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
        
    if not text:
        return None

    # Match pure imaginary like 4i, -i, +i
    if re.fullmatch(r"[-+]?\d*\.?\d*i", text):
        val_str = text.replace("i", "")
        if val_str in ("", "+"):
            return 0.0, 1.0
        if val_str == "-":
            return 0.0, -1.0
        return 0.0, float(val_str)

    # Match pure real
    if re.fullmatch(r"[-+]?\d*\.?\d+", text):
        return float(text), 0.0

    # Match full a + bi or a - bi
    match = re.fullmatch(r"([-+]?\d*\.?\d+)([-+]\d*\.?\d*)i", text)
    if match:
        real_part = float(match.group(1))
        imag_str = match.group(2)
        if imag_str in ("+", ""):
            imag_part = 1.0
        elif imag_str == "-":
            imag_part = -1.0
        else:
            imag_part = float(imag_str)
        return real_part, imag_part

    return None


def extract_complex_numbers(text: str):
    """Extracts all complex numbers from a user prompt string."""
    # Look for patterns in parentheses or raw complex strings
    pattern = r"\(?[-+]?\d*\.?\d+(?:[-+]\d*\.?\d*)?i\)?|\(?[-+]?\d*\.?\d*i\)|[-+]?\d+\.?\d*"
    matches = re.findall(r"[-+]?\d*\.?\d+[-+]\d*\.?\d*i|[-+]?\d*\.?\d*i|[-+]?\d+\.?\d*", text)
    results = []
    for m in matches:
        if not m:
            continue
        c = parse_single_complex(m)
        if c is not None:
            results.append(c)
    return results


def format_num(n: float) -> str:
    """Formats float cleanly: integers without decimal, floats rounded to 4 decimals."""
    if abs(n - round(n)) < 1e-7:
        return str(int(round(n)))
    return f"{round(n, 4):g}"


def format_complex(real: float, imag: float) -> str:
    """Formats (real, imag) cleanly into standard a + bi form."""
    r_str = format_num(real)
    i_str = format_num(abs(imag))
    
    if abs(imag) < 1e-7:
        return r_str
    if abs(real) < 1e-7:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return f"{format_num(imag)}i"
        
    sign = "+" if imag > 0 else "-"
    i_term = "i" if i_str == "1" else f"{i_str}i"
    return f"{r_str} {sign} {i_term}"


def solve_complex_question(question_text: str):
    text = question_text.lower()
    
    # Try finding complex numbers in text
    complex_nums = extract_complex_numbers(question_text)
    
    # Check operation type
    is_polar = any(kw in text for kw in ["polar", "modulus", "argument", "arg", "mod", "r cis"])
    is_mult = "*" in text or "multiply" in text or "product" in text or "times" in text or "×" in text
    is_div = "/" in text or "divide" in text or "quotient" in text or "over" in text
    is_sub = "-" in text and not is_polar and len(complex_nums) >= 2
    is_add = "+" in text and not is_polar and len(complex_nums) >= 2

    if not complex_nums:
        # Fallback default example if no numbers parsed
        real, imag = 3.0, 4.0
        explanation_lines = [
            f"No specific complex number parsed from prompt. Using default z = 3 + 4i.",
        ]
    else:
        real, imag = complex_nums[0]
        explanation_lines = []

    # 1. POLAR / MODULUS / ARGUMENT
    if is_polar or len(complex_nums) == 1:
        r = math.hypot(real, imag)
        theta_rad = math.atan2(imag, real)
        theta_deg = math.degrees(theta_rad)
        
        z_str = format_complex(real, imag)
        explanation_lines.append(f"Given complex number z = {z_str}")
        explanation_lines.append(f"Step 1: Calculate modulus r = √(a² + b²) = √(({format_num(real)})² + ({format_num(imag)})²)")
        explanation_lines.append(f"        r = √({format_num(real**2)} + {format_num(imag**2)}) = {format_num(r)}")
        
        explanation_lines.append(f"Step 2: Calculate principal argument θ = atan2(b, a)")
        explanation_lines.append(f"        θ = atan2({format_num(imag)}, {format_num(real)}) = {format_num(theta_rad)} rad ({format_num(theta_deg)}°)")
        
        polar_form = f"{format_num(r)} (cos({format_num(theta_deg)}°) + i sin({format_num(theta_deg)}°))"
        euler_form = f"{format_num(r)} e^({format_num(theta_rad)}i)"
        explanation_lines.append(f"Step 3: Express in polar form z = r (cos θ + i sin θ)")
        explanation_lines.append(f"        z = {polar_form}")

        return {
            "ok": True,
            "topic": "complex",
            "topic_label": "Complex Numbers & Polar Form",
            "input": {"z": z_str, "a": real, "b": imag},
            "answer": f"z = {z_str} | Polar: {polar_form} | r = {format_num(r)}, θ = {format_num(theta_deg)}°",
            "explanation": explanation_lines,
            "details": {
                "modulus": r,
                "argument_rad": theta_rad,
                "argument_deg": theta_deg,
                "polar_form": polar_form,
                "euler_form": euler_form,
            },
        }

    # 2. TWO COMPLEX NUMBERS OPERATIONS
    z1_real, z1_imag = complex_nums[0]
    z2_real, z2_imag = complex_nums[1]
    z1_str = format_complex(z1_real, z1_imag)
    z2_str = format_complex(z2_real, z2_imag)

    if is_div:
        # Division (z1 / z2)
        denom = z2_real**2 + z2_imag**2
        if abs(denom) < 1e-9:
            return {
                "ok": False,
                "topic": "complex",
                "topic_label": "Complex Numbers & Polar Form",
                "error": "Division by zero complex number (0 + 0i) is undefined.",
            }
        
        ans_real = (z1_real * z2_real + z1_imag * z2_imag) / denom
        ans_imag = (z1_imag * z2_real - z1_real * z2_imag) / denom
        ans_str = format_complex(ans_real, ans_imag)
        
        z2_conj_str = format_complex(z2_real, -z2_imag)
        
        explanation_lines.append(f"Evaluate ({z1_str}) / ({z2_str}):")
        explanation_lines.append(f"Step 1: Multiply numerator and denominator by the complex conjugate of denominator ({z2_conj_str})")
        explanation_lines.append(f"        [({z1_str}) * ({z2_conj_str})] / [({z2_str}) * ({z2_conj_str})]")
        explanation_lines.append(f"Step 2: Simplify denominator = a² + b² = {format_num(z2_real)}² + {format_num(z2_imag)}² = {format_num(denom)}")
        explanation_lines.append(f"Step 3: Expand numerator = ({format_num(z1_real*z2_real + z1_imag*z2_imag)}) + ({format_num(z1_imag*z2_real - z1_real*z2_imag)})i")
        explanation_lines.append(f"Step 4: Divide each part by {format_num(denom)} => {ans_str}")

        return {
            "ok": True,
            "topic": "complex",
            "topic_label": "Complex Numbers & Polar Form",
            "input": {"z1": z1_str, "z2": z2_str, "operation": "division"},
            "answer": f"({z1_str}) / ({z2_str}) = {ans_str}",
            "explanation": explanation_lines,
        }

    # Multiplication default / explicit
    ans_real = z1_real * z2_real - z1_imag * z2_imag
    ans_imag = z1_real * z2_imag + z1_imag * z2_real
    ans_str = format_complex(ans_real, ans_imag)
    
    explanation_lines.append(f"Evaluate ({z1_str}) * ({z2_str}):")
    explanation_lines.append(f"Step 1: Expand using FOIL: (a₁a₂ - b₁b₂) + (a₁b₂ + a₂b₁)i")
    explanation_lines.append(f"        Real part = ({format_num(z1_real)})({format_num(z2_real)}) - ({format_num(z1_imag)})({format_num(z2_imag)}) = {format_num(ans_real)}")
    explanation_lines.append(f"        Imag part = ({format_num(z1_real)})({format_num(z2_imag)}) + ({format_num(z1_imag)})({format_num(z2_real)}) = {format_num(ans_imag)}")
    explanation_lines.append(f"Step 2: Combine terms => {ans_str}")

    return {
        "ok": True,
        "topic": "complex",
        "topic_label": "Complex Numbers & Polar Form",
        "input": {"z1": z1_str, "z2": z2_str, "operation": "multiplication"},
        "answer": f"({z1_str}) × ({z2_str}) = {ans_str}",
        "explanation": explanation_lines,
    }
