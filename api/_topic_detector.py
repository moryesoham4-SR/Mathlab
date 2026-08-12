"""
Keyword-based topic detector for Interactive Mathematics Lab.
Shared by all /api/solve_*.py endpoints (imported directly, no external deps).
"""

import re

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
    """
    Returns (topic_key, topic_label, confidence_score).
    topic_key is None if nothing matched.
    """
    text = question_text.lower()
    scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                score += 1
        if score > 0:
            scores[topic] = score

    if not scores:
        return None, "Unknown", 0

    best_topic = max(scores, key=scores.get)
    return best_topic, TOPIC_LABELS[best_topic], scores[best_topic]


def extract_integers(text: str):
    """Pull out all integers mentioned in a question (handles negatives)."""
    matches = re.findall(r"-?\d+", text)
    return [int(m) for m in matches]
