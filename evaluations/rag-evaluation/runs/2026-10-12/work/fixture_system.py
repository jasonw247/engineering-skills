"""Tiny deterministic synthetic system, not a retrieval benchmark or latency model."""


def run(query, corpus, variant):
    if variant not in ("baseline", "candidate"):
        raise ValueError(variant)
    candidates = [
        key for key, record in corpus.items()
        if record["entity"] == query["entity"]
        and record["revision"] == query["revision"]
    ]
    if variant == "candidate" and not candidates:
        return {"candidates": [], "evidence": [], "answer_mpa": None,
                "citations": [], "abstained": True}
    selected = "general"
    if variant == "candidate" and query["temperature"] > 60:
        selected = "exception-copy"
    return {"candidates": candidates, "evidence": [selected],
            "answer_mpa": 8 if selected == "exception-copy" else 10,
            "citations": [selected], "abstained": False}
