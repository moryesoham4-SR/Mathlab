"""
POST /api/solve
Body: {"question": "Find gcd(252, 105) using the Euclidean algorithm"}

Response: JSON with detected topic + step-by-step solution.
Currently GCD/Euclidean Algorithm is fully implemented.
Other 5 topics return a "not implemented yet" placeholder so the
frontend can be built against a stable API shape from day one.

NOTE: Everything lives in this one file on purpose. Vercel's Python
runtime treats every .py file directly inside api/ as its own function
entrypoint, so splitting shared logic into separate files in the same
folder causes deploy errors ("Could not find a top-level handler").
Once there are multiple topics, shared logic will move into a
top-level /lib folder instead and be imported from there.
"""

import json
import re
from http.server import BaseHTTPRequestHandler

# ---------------------------------------------------------------------------
# Topic detection (keyword-based)
# ---------------------------------------------------------------------------

TOPIC_KEYWORDS = {
    "gcd": [
        "gcd", "greatest common divisor", "euclidean algorithm",
        "hcf", "highest common factor",
    ],
    "complex": [
        "complex number", "polar form", "modulus", "argument of",
        "imaginary", "rectangular form", "a+bi", "a + bi",
    ],
    "demoivre": [
        "de moivre", "demoivre", "de-moivre", "nth root of",
        "z^n", "z**n", "cis theta", "cis(theta)",
    ],
    "permcomb": [
        "permutation", "combination", "arrangement", "npr", "ncr",
        "factorial", "how many ways", "choose",
    ],
    "functions": [
        "injective", "surjective", "bijective", "one-to-one",
        "onto", "one to one function", "codomain",
    ],
    "limits": [
        "limit", "continuity", "continuous", "lim ", "l'hopital",
        "l'hospital", "discontinuous",
    ],
}

TOPIC_LABELS = {
    "gcd": "Euclidean Algorithm & GCD",
    "complex": "Complex Numbers & Polar Form",
    "demoivre": "De Moivre's Theorem",
    "permcomb": "Permutations & Combinations",
    "functions": "Injective, Surjective & Bijective Functions",
    "limits": "Limits & Continuity",
}


def detect_topic(question_text: str):
    text = question_text.lower()
    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[topic] = score
    if not scores:
        return None, "Unknown", 0
    best_topic = max(scores, key=scores.get)
    return best_topic, TOPIC_LABELS[best_topic], scores[best_topic]


def extract_integers(text: str):
    matches = re.findall(r"-?\d+", text)
    return [int(m) for m in matches]


# ---------------------------------------------------------------------------
# GCD / Euclidean Algorithm solver
# ---------------------------------------------------------------------------

def euclidean_steps(a: int, b: int):
    a, b = abs(a), abs(b)
    if b == 0:
        return [], a
    steps = []
    while b != 0:
        q, r = divmod(a, b)
        steps.append({"a": a, "b": b, "quotient": q, "remainder": r})
        a, b = b, r
    return steps, a


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
            "We repeatedly apply the division algorithm: a = b*q + r, "
            "replacing (a, b) with (b, r) until the remainder is 0."
        )
        for i, s in enumerate(steps, start=1):
            explanation_lines.append(
                f"Step {i}: {s['a']} = {s['b']} \u00d7 {s['quotient']} + {s['remainder']}"
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
            "equation": f"{a}\u00d7({x}) + {b}\u00d7({y}) = {gcd}",
            "x": x,
            "y": y,
        },
    }


# ---------------------------------------------------------------------------
# Request handling
# ---------------------------------------------------------------------------

def build_response(question_text: str):
    topic_key, topic_label, confidence = detect_topic(question_text)

    if topic_key is None:
        return {
            "ok": False,
            "error": "Could not detect a topic for this question. "
                     "Try rephrasing or check spelling of key terms.",
        }

    if topic_key == "gcd":
        numbers = extract_integers(question_text)
        if len(numbers) < 2:
            return {
                "ok": False,
                "topic": topic_key,
                "topic_label": topic_label,
                "error": "Detected a GCD/Euclidean Algorithm question, but "
                         "couldn't find two numbers in the text. "
                         "Try a format like 'Find gcd(252, 105)'.",
            }
        a, b = numbers[0], numbers[1]
        result = solve_gcd_question(a, b)
        result["ok"] = True
        result["confidence"] = confidence
        return result

    return {
        "ok": False,
        "topic": topic_key,
        "topic_label": topic_label,
        "error": f"'{topic_label}' solver is coming soon \u2014 GCD is the "
                 f"only topic wired up so far.",
    }


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(204, {})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            data = json.loads(raw.decode("utf-8") or "{}")
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"ok": False, "error": "Invalid JSON body."})
            return

        question_text = (data.get("question") or "").strip()
        if not question_text:
            self._send_json(400, {"ok": False, "error": "Missing 'question' field."})
            return

        result = build_response(question_text)
        self._send_json(200, result)

    def do_GET(self):
        self._send_json(
            200,
            {
                "ok": True,
                "message": "This endpoint expects POST with a JSON body: "
                           "{\"question\": \"...\"}",
            },
        )
