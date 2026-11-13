#!/usr/bin/env python3
"""Run local synthetic tasks in fresh Codex sessions; never grade inside the actor.

Requires an authenticated Codex CLI. This runner makes model calls, writes only
the selected run directory and temporary workspaces, and never installs skills.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


EVAL = Path(__file__).resolve().parent


def hashes(root):
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*")) if p.is_file()
    }


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def protected_section(text, heading):
    start = text.index("## " + heading + "\n")
    end = text.find("\n## ", start + 3)
    return text[start:] if end == -1 else text[start:end + 1]


def run_one(args, case, routing=False):
    label = "routing" if routing else case["id"]
    dest = args.run / args.arm / args.repeat / label
    dest.mkdir(parents=True, exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix="document-trial-") as temp:
        base = Path(temp)
        work = base / "work"
        work.mkdir()
        codex_home = base / "codex-home"
        codex_home.mkdir()
        auth = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "auth.json"
        if auth.is_file():
            shutil.copyfile(auth, codex_home / "auth.json")
            (codex_home / "auth.json").chmod(0o600)

        if routing:
            entry = (args.skill_package / "SKILL.md").read_text()
            metadata = entry.split("---", 2)[1].strip()
            rows = [{"id": c["id"], "request": c["request"]} for c in args.cases]
            prompt = (
                "Decide whether the following skill should be selected for each request, "
                "using only its name and description. Do not perform the tasks, read files, "
                "or use tools. Return a JSON array with id, select (boolean), and a short reason.\n\n"
                + metadata + "\n\nRequests:\n" + json.dumps(rows, indent=2)
            )
            raw_names = []
        else:
            raw_names = [Path(p).name for p in case["inputs"]]
            for name in raw_names:
                shutil.copyfile(args.run / "inputs" / name, work / name)
            if args.skill_package:
                shutil.copytree(args.skill_package, work / "skill")
            prompt = (
                "Complete the user request below. The available task inputs are "
                + ", ".join(raw_names) + ".\n"
                "Resource boundary: use only these synthetic local inputs, your ordinary "
                "tools, and any supplied skill package. Do not access the network, read "
                "outside this workspace, delegate, commit, publish, or use external services. "
                "You may create the requested deliverables and temporary local checks here.\n"
            )
            if args.skill_package:
                prompt += "Use the technical-document-review skill at skill/SKILL.md.\n"
            prompt += "\nUser request:\n" + case["request"]

        before = hashes(work)
        (dest / "prompt.txt").write_text(prompt)
        cmd = [
            "codex", "exec", "--json", "--ephemeral", "--ignore-user-config",
            "--skip-git-repo-check", "--enable", "skip_host_skill_discovery",
            "--disable", "apps", "--disable", "multi_agent", "--disable", "shell_snapshot",
            "-c", 'web_search="disabled"', "-m", args.model,
            "-c", 'model_reasoning_effort="high"', "-s", "workspace-write",
            "-C", str(work), "-o", str(dest / "final.md"), "-",
        ]
        write_json(dest / "command.json", cmd)
        env = os.environ.copy()
        # Do not inherit the enclosing Codex session's host/tool negotiation.
        for key in list(env):
            if key.startswith("CODEX_"):
                del env[key]
        env["CODEX_HOME"] = str(codex_home)
        helper = Path(shutil.which("codex")).resolve().with_name("codex-code-mode-host")
        if helper.is_file():
            env["CODEX_CODE_MODE_HOST_PATH"] = str(helper)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        tick = time.monotonic()
        execution = "completed"
        with (dest / "trace.jsonl").open("w") as out, (dest / "stderr.txt").open("w") as err:
            try:
                result = subprocess.run(cmd, input=prompt, text=True, stdout=out,
                                        stderr=err, env=env, timeout=args.timeout)
                exit_code = result.returncode
            except subprocess.TimeoutExpired:
                execution, exit_code = "timeout", None
        elapsed = time.monotonic() - tick
        after = hashes(work)
        unchanged = {name: before[name] == after.get(name) for name in raw_names}
        allowed_edits = raw_names[:1] if not routing and case["id"].startswith("edit-") else []
        integrity = all(ok for name, ok in unchanged.items() if name not in allowed_edits)
        protected = None
        protection = {
            "edit-preserve-meaning": ("report.md", "Compatibility note"),
            "edit-protected-conflict": ("protected-conflict.md", "Approved statement"),
        }.get(label) or (tuple(case["protected_section"]) if not routing and "protected_section" in case else None)
        if protection:
            name, heading = protection
            try:
                protected = (
                    protected_section((args.run / "inputs" / name).read_bytes().decode(), heading)
                    == protected_section((work / name).read_bytes().decode(), heading)
                )
            except (ValueError, FileNotFoundError):
                protected = False
        for item in work.iterdir():
            if item.name == "skill":
                continue
            target = dest / "artifacts" / item.name
            target.parent.mkdir(parents=True, exist_ok=True)
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copyfile(item, target)

        events, invalid = [], 0
        for line in (dest / "trace.jsonl").read_text().splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                invalid += 1
        turns = [e for e in events if e.get("type") == "turn.completed"]
        stderr = (dest / "stderr.txt").read_text()
        infrastructure_errors = [line for line in stderr.splitlines()
                                 if "negotiating with the code-mode host" in line
                                 or "code-mode host is disabled" in line]
        commands = [e["item"] for e in events if e.get("type") == "item.completed"
                    and e.get("item", {}).get("type") == "command_execution"]
        record = {
            "id": label, "arm": args.arm, "repeat": args.repeat,
            "started_at": started, "execution": execution, "exit_code": exit_code,
            "elapsed_seconds": round(elapsed, 3), "model_requested": args.model,
            "reasoning_effort": "high", "timeout_seconds": args.timeout,
            "code_mode_host_path": str(helper) if helper.is_file() else None,
            "inherited_codex_environment_removed": True,
            "infrastructure_errors": infrastructure_errors,
            "skill_sha256": hashes(args.skill_package) if args.skill_package else {},
            "workspace_sha256_before": before, "workspace_sha256_after": after,
            "inputs_unchanged": unchanged, "read_only_inputs_preserved": integrity,
            "protected_section_unchanged": protected,
            "skill_unchanged": all(before[k] == after.get(k) for k in before if k.startswith("skill/")),
            "turn_completed": bool(turns), "invalid_trace_lines": invalid,
            "usage": [e.get("usage", {}) for e in turns], "command_count": len(commands),
            "grading": "pending; execution completion is not semantic acceptance",
        }
        write_json(dest / "execution.json", record)
    print(json.dumps({"arm": args.arm, "case": label, "repeat": args.repeat,
                      "execution": execution, "exit_code": exit_code,
                      "seconds": record["elapsed_seconds"], "integrity": integrity,
                      "protected": protected}), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--arm", required=True)
    parser.add_argument("--skill-package", type=Path)
    parser.add_argument("--model", default="gpt-6.1-sol")
    parser.add_argument("--repeat", default="initial")
    parser.add_argument("--case", action="append")
    parser.add_argument("--routing", action="store_true")
    parser.add_argument("--jobs", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()
    args.run = args.run.resolve()
    args.skill_package = args.skill_package.resolve() if args.skill_package else None
    args.cases = json.loads((args.run / "expected.json").read_text())["cases"]
    if args.routing:
        if not args.skill_package:
            parser.error("routing requires metadata from --skill-package")
        run_one(args, None, routing=True)
        return
    selected = [c for c in args.cases if c["inputs"] and c["activate"]
                and (not args.case or c["id"] in args.case)]
    if not selected or (args.case and set(args.case) - {c["id"] for c in selected}):
        parser.error("unknown or non-behavioral case")
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for start in range(0, len(selected), args.jobs):
            pending = [pool.submit(run_one, args, case)
                       for case in selected[start:start + args.jobs]]
            results = [future.result() for future in as_completed(pending)]
            if any(r["infrastructure_errors"] or r["exit_code"] != 0 for r in results):
                raise SystemExit("Infrastructure failure: stopping before dispatching more tasks")


if __name__ == "__main__":
    main()
