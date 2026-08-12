"""
POST /api/solve
Body: {"question": "..."}

Response: JSON with detected topic + step-by-step solution.
Supported topics:
1. GCD / Euclidean Algorithm (gcd)
2. Complex Numbers & Polar Form (complex)
3. De Moivre's Theorem & Nth Roots (demoivre)
4. Permutations & Combinations (permcomb)
5. Injective, Surjective & Bijective Functions (functions)
6. Limits & Continuity (limits)
"""

import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Ensure project root is in sys.path for lib package imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from lib.solver_gcd import solve_gcd_question
from lib.solver_complex import solve_complex_question
from lib.solver_demoivre import solve_demoivre_question
from lib.solver_permcomb import solve_permcomb_question
from lib.solver_functions import solve_functions_question
from lib.solver_limits import solve_limits_question


TOPIC_KEYWORDS = {
    "gcd": [
        "gcd", "greatest common divisor", "euclidean algorithm",
        "hcf", "highest common factor", "bezout",
    ],
    "demoivre": [
        "de moivre", "demoivre", "de-moivre", "nth root", "cube root",
        "square root of complex", "z^n", "z**n", "roots of",
    ],
    "complex": [
        "complex number", "polar form", "modulus", "argument",
        "imaginary", "rectangular form", "a+bi", "a + bi", "arg(", "mod(",
    ],
    "permcomb": [
        "permutation", "combination", "arrangement", "npr", "ncr",
        "factorial", "how many ways", "choose", "anagram", "word",
    ],
    "functions": [
        "injective", "surjective", "bijective", "one-to-one",
        "onto", "one to one function", "codomain", "f(x)",
    ],
    "limits": [
        "limit", "continuity", "continuous", "lim ", "l'hopital",
        "l'hospital", "discontinuous", "infinity", "x->", "x →",
    ],
}

TOPIC_LABELS = {
    "gcd": "Euclidean Algorithm & GCD",
    "complex": "Complex Numbers & Polar Form",
    "demoivre": "De Moivre's Theorem & Nth Roots",
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


def build_response(question_text: str):
    topic_key, topic_label, confidence = detect_topic(question_text)

    if topic_key is None:
        return {
            "ok": False,
            "error": "Could not detect a topic for this question. "
                     "Try rephrasing or check spelling of key terms (e.g., 'gcd', 'complex', 'permutations', 'limit').",
        }

    try:
        if topic_key == "gcd":
            numbers = extract_integers(question_text)
            if len(numbers) < 2:
                return {
                    "ok": False,
                    "topic": topic_key,
                    "topic_label": topic_label,
                    "error": "Detected a GCD/Euclidean Algorithm question, but couldn't find two numbers. "
                             "Try a format like 'Find gcd(252, 105)'.",
                }
            result = solve_gcd_question(numbers[0], numbers[1])

        elif topic_key == "demoivre":
            result = solve_demoivre_question(question_text)

        elif topic_key == "complex":
            result = solve_complex_question(question_text)

        elif topic_key == "permcomb":
            result = solve_permcomb_question(question_text)

        elif topic_key == "functions":
            result = solve_functions_question(question_text)

        elif topic_key == "limits":
            result = solve_limits_question(question_text)

        else:
            return {
                "ok": False,
                "error": f"No solver available for topic '{topic_key}'.",
            }

        result["confidence"] = confidence
        return result

    except Exception as err:
        return {
            "ok": False,
            "topic": topic_key,
            "topic_label": topic_label,
            "error": f"Error solving question: {str(err)}",
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
