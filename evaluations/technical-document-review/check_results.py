#!/usr/bin/env python3
"""Recheck retained artifact integrity and metadata routing; no model calls.

Semantic acceptance remains in the author's grades.json, not a wording matcher.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re

from run_trials import hashes, protected_section


def load(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    run = args.run.resolve()
    baseline = load(run / "baseline.json")
    assert hashes(run / "original-skill") == baseline["skill_sha256"], "original skill changed"
    assert hashes(run / "inputs") == baseline["input_sha256"], "raw input snapshot changed"
    assert hashlib.sha256((run / "expected.json").read_bytes()).hexdigest() == baseline["expected_sha256"], "acceptance keys changed"
    cases = {c["id"]: c for c in load(run / "expected.json")["cases"]}
    packages = {"original": hashes(run / "original-skill"), "no-skill": {},
                "candidate": hashes(run / "candidate-skill")}
    records, routing = [], []
    for arm in ("original", "no-skill", "candidate"):
        for record_path in sorted((run / arm).glob("*/*/execution.json")):
            record = load(record_path)
            if record["execution"] != "completed":
                continue
            dest = record_path.parent
            assert record["exit_code"] == 0 and record["turn_completed"], dest
            assert not record.get("infrastructure_errors"), dest
            assert record["invalid_trace_lines"] == 0, dest
            assert record["skill_sha256"] == packages[arm], (dest, "package provenance differs")
            if record["id"] == "routing":
                text = (dest / "final.md").read_text().strip()
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
                decisions = json.loads(text)
                assert len(decisions) == len(cases), dest
                assert {d["id"] for d in decisions} == set(cases), dest
                assert all(type(d["select"]) is bool for d in decisions), dest
                correct = sum(d["select"] == cases[d["id"]]["activate"] for d in decisions)
                assert record["command_count"] == 0, "routing actor used a terminal"
                routing.append({"arm": arm, "repeat": record["repeat"],
                                "correct": correct, "total": len(cases)})
                continue
            case = cases[record["id"]]
            names = [Path(p).name for p in case["inputs"]]
            editable = names[:1] if case["id"].startswith("edit-") else []
            for name in names:
                artifact = dest / "artifacts" / name
                actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
                assert actual == record["workspace_sha256_after"][name], artifact
                if name not in editable:
                    assert actual == baseline["input_sha256"][name], artifact
            protected = {
                "edit-preserve-meaning": ("report.md", "Compatibility note"),
                "edit-protected-conflict": ("protected-conflict.md", "Approved statement"),
            }.get(case["id"]) or (tuple(case["protected_section"]) if "protected_section" in case else None)
            if protected:
                name, heading = protected
                assert protected_section((run / "inputs" / name).read_bytes().decode(), heading) == protected_section((dest / "artifacts" / name).read_bytes().decode(), heading), dest
            assert record["skill_unchanged"], dest
            prompt = (dest / "prompt.txt").read_text()
            assert "expected.json" not in prompt and "completion" not in prompt, dest
            if arm == "no-skill":
                assert not record["skill_sha256"] and "Use the technical-document-review skill" not in prompt, dest
            records.append({"arm": arm, "repeat": record["repeat"], "id": record["id"]})

    grades_path = run / "grades.json"
    graded = 0
    if grades_path.exists():
        grades = load(grades_path)
        for arm in ("original", "no-skill", "candidate"):
            observed = {r["id"] for r in records if r["arm"] == arm and r["repeat"] == "matched"}
            expected = {c["id"] for c in cases.values() if c["activate"] and c["inputs"]}
            assert observed == expected, (arm, "missing matched trials", expected - observed)
            assert set(grades[arm]) == expected, (arm, "missing semantic grades")
            for case_id, grade in grades[arm].items():
                assert grade["status"] in ("pass", "fail"), (arm, case_id)
                assert grade["evidence"] and grade["checks"], (arm, case_id)
                assert len(grade["checks"]) == len(cases[case_id].get("checks", [cases[case_id]["completion"]])), (arm, case_id)
                if grade["status"] == "pass":
                    assert all(c["satisfied"] is True for c in grade["checks"]), (arm, case_id)
                graded += 1
    print(json.dumps({"completed_behavioral_artifact_checks": len(records),
                      "routing": routing, "matched_semantic_grades_present": graded,
                      "snapshot_integrity": "pass", "read_only_inputs": "pass",
                      "protected_sections": "pass",
                      "limit": "Artifact checks validate integrity, not the truth of author semantic judgments."}, indent=2))


if __name__ == "__main__":
    main()
