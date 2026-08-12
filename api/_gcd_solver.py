"""
Euclidean Algorithm solver.
Given two integers, returns full step-by-step division trace,
the GCD, and Bezout coefficients (extended Euclidean algorithm) as a bonus.
"""


def euclidean_steps(a: int, b: int):
    """
    Returns a list of step dicts:
      {"a": a, "b": b, "quotient": q, "remainder": r}
    representing a = b*q + r at each stage, plus the final gcd.
    """
    a, b = abs(a), abs(b)
    if b == 0:
        return [], a  # gcd(a, 0) = a, no division needed

    steps = []
    while b != 0:
        q, r = divmod(a, b)
        steps.append({"a": a, "b": b, "quotient": q, "remainder": r})
        a, b = b, r

    gcd = a
    return steps, gcd


def extended_gcd(a: int, b: int):
    """Returns (gcd, x, y) such that a*x + b*y = gcd."""
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
    """
    Builds the full explanation payload for the frontend:
    step-by-step trace in human-readable form + final answer.
    """
    steps, gcd = euclidean_steps(a, b)
    _, x, y = extended_gcd(a, b)

    explanation_lines = []
    if not steps:
        explanation_lines.append(f"Since one number is 0, gcd({a}, {b}) = {gcd} directly.")
    else:
        explanation_lines.append(
            f"We repeatedly apply the division algorithm: a = b*q + r, "
            f"replacing (a, b) with (b, r) until the remainder is 0."
        )
        for i, s in enumerate(steps, start=1):
            explanation_lines.append(
                f"Step {i}: {s['a']} = {s['b']} × {s['quotient']} + {s['remainder']}"
            )
        explanation_lines.append(
            f"The last nonzero remainder is {gcd}, so gcd({a}, {b}) = {gcd}."
        )

    return {
        "topic": "gcd",
        "topic_label": "Euclidean Algorithm & GCD",
        "input": {"a": a, "b": b},
        "steps": steps,
        "answer": gcd,
        "explanation": explanation_lines,
        "bonus_bezout": {
            "equation": f"{a}×({x}) + {b}×({y}) = {gcd}",
            "x": x,
            "y": y,
        },
    }
