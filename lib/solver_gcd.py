"""
GCD and Euclidean Algorithm Solver
"""

def euclidean_steps(a: int, b: int):
    a_abs, b_abs = abs(a), abs(b)
    if b_abs == 0:
        return [], a_abs
    steps = []
    curr_a, curr_b = a_abs, b_abs
    while curr_b != 0:
        q, r = divmod(curr_a, curr_b)
        steps.append({"a": curr_a, "b": curr_b, "quotient": q, "remainder": r})
        curr_a, curr_b = curr_b, r
    return steps, curr_a


def extended_gcd(a: int, b: int):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def solve_gcd_question(a: int, b: int):
    steps, gcd = euclidean_steps(a, b)
    _, x, y = extended_gcd(a, b)

    explanation_lines = []
    if not steps:
        explanation_lines.append(f"Since one number is 0, gcd({a}, {b}) = {gcd} directly.")
    else:
        explanation_lines.append(
            "We repeatedly apply the division algorithm: a = b × q + r, "
            "replacing (a, b) with (b, r) until the remainder is 0."
        )
        for i, s in enumerate(steps, start=1):
            explanation_lines.append(
                f"Step {i}: {s['a']} = {s['b']} × {s['quotient']} + {s['remainder']}"
            )
        explanation_lines.append(
            f"The last nonzero remainder is {gcd}, so gcd({a}, {b}) = {gcd}."
        )

    return {
        "ok": True,
        "topic": "gcd",
        "topic_label": "Euclidean Algorithm & GCD",
        "input": {"a": a, "b": b},
        "steps": steps,
        "answer": f"gcd({a}, {b}) = {gcd}",
        "explanation": explanation_lines,
        "bonus_bezout": {
            "equation": f"{a} × ({x}) + {b} × ({y}) = {gcd}",
            "x": x,
            "y": y,
        },
    }
