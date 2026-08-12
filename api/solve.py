"""
POST /api/solve
Body: {"question": "Find gcd(252, 105) using the Euclidean algorithm"}

Response: JSON with detected topic + step-by-step solution.
Currently GCD/Euclidean Algorithm is fully implemented.
Other 5 topics return a "not implemented yet" placeholder so the
frontend can be built against a stable API shape from day one.
"""

import json
from http.server import BaseHTTPRequestHandler

from _topic_detector import detect_topic, extract_integers
from _gcd_solver import solve_gcd_question


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

    # Placeholder for the other 5 topics (built in later steps)
    return {
        "ok": False,
        "topic": topic_key,
        "topic_label": topic_label,
        "error": f"'{topic_label}' solver is coming soon — GCD is the "
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
