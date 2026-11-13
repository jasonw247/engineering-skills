#!/usr/bin/env python3
"""Preview or install a curated selection into a repository or host catalog."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


REGISTRY = Path("skills/bootstrap-repo/references/registry.json")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
# Lock format version 1 (references/lock-format.md). Writers use the generic
# name and replace a lock still stored under the original name.
LOCK, LEGACY_LOCK = "skills.lock.json", "skill-repo.lock.json"
MAX_LOCK_BYTES = 1024 * 1024


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def package_name(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing skill frontmatter: {path}")
    frontmatter = text.split("---", 2)[1]
    match = re.search(r"^name:\s*(['\"]?)([a-z0-9-]+)\1\s*$", frontmatter, re.M)
    if not match:
        raise ValueError(f"Missing or invalid skill name: {path}")
    return match[2]


def snapshot(root, ignore_caches=True):
    """Read packages without symlinks; exclude source caches when packaging."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"Expected a real skill directory: {root}")
    files = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        here = Path(directory)
        for name in dirs:
            if (here / name).is_symlink():
                raise ValueError(f"Symlink in skill package: {here / name}")
        dirs[:] = sorted(name for name in dirs if not ignore_caches or name != "__pycache__")
        for name in sorted(names):
            path = here / name
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"Expected a regular skill file: {path}")
            if not ignore_caches or path.suffix != ".pyc":
                files[path.relative_to(root).as_posix()] = (
                    path.read_bytes(), path.stat().st_mode & 0o777
                )
    return files


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, (data, _) in files.items()}


def select(registry, profile, requested):
    entries = registry["skills"]
    if profile and profile not in registry["profiles"]:
        raise ValueError(f"Unknown profile: {profile}")
    roots = registry["profiles"][profile]["skills"] if profile else []
    selected, visiting = [], set()

    def visit(name):
        if name not in entries or not NAME.fullmatch(name):
            raise ValueError(f"Unknown or invalid skill: {name}")
        if name in visiting:
            raise ValueError(f"Cyclic skill dependency: {name}")
        if name in selected:
            return
        visiting.add(name)
        for dependency in entries[name].get("dependencies", []):
            visit(dependency)
        visiting.remove(name)
        selected.append(name)

    for name in list(roots) + requested:
        visit(name)
    if not selected:
        raise ValueError("Choose --profile or at least one --skill")
    return selected


def catalog_conflicts(records, destination, selected):
    """Validate the prospective catalog without relabeling retained packages."""
    conflicts = []
    for name, record in records.items():
        if not NAME.fullmatch(name) or not isinstance(record, dict):
            conflicts.append(f"Invalid catalog record: {name}")
            continue
        roles, cues = record.get("roles"), record.get("cues")
        use_when = record.get("use_when")
        if not (
            isinstance(roles, list) and roles
            and all(role in ("actor", "reviewer") for role in roles)
            and isinstance(use_when, str) and use_when.strip()
            and isinstance(cues, list) and cues
            and all(isinstance(cue, str) and cue.strip() for cue in cues)
        ):
            remedy = (f"include --skill {name} in this upgrade"
                      if name not in selected else "fix the source registry entry")
            conflicts.append(f"{name}: missing or invalid selection metadata; {remedy}")
        if "upstream" in record and not isinstance(record["upstream"], dict):
            remedy = (f"include --skill {name} in this upgrade"
                      if name not in selected else "fix the source registry entry")
            conflicts.append(f"{name}: upstream must be an object; {remedy}")
        dependencies = record.get("dependencies", [])
        if not (isinstance(record.get("version"), str) and record["version"].strip()
                and isinstance(dependencies, list)
                and all(isinstance(dep, str) and NAME.fullmatch(dep) for dep in dependencies)):
            conflicts.append(f"{name}: invalid version or dependencies")
        if name not in selected:
            try:
                root = destination / name
                if package_name(root / "SKILL.md") != name:
                    raise ValueError("package name/path mismatch")
                if hashes(snapshot(root, ignore_caches=False)) != record.get("files"):
                    raise ValueError("managed copy has local edits or damage")
            except (OSError, ValueError) as error:
                conflicts.append(f"{name}: retained package is invalid: {error}")
    if not conflicts:
        try:
            select({"skills": records, "profiles": {}}, None, list(records))
        except ValueError as error:
            conflicts.append(f"Invalid catalog dependency closure: {error}")
    return conflicts


def install(source, target, registry, selected, profile, apply, host=False):
    agents = target if host else target / ".agents"
    destination = agents / "skills"
    lock_path, legacy_path = agents / LOCK, agents / LEGACY_LOCK
    for path in (agents, destination, lock_path, legacy_path):
        if path.is_symlink():
            raise ValueError(f"Refusing symlinked installation path: {path}")
    for path in (agents, destination):
        if path.exists() and not path.is_dir():
            raise ValueError(f"Expected a directory: {path}")
    if lock_path.exists() and legacy_path.exists():
        raise ValueError(f"Both {LOCK} and {LEGACY_LOCK} exist in {agents}; remove the stale one")
    current = lock_path if lock_path.exists() else legacy_path if legacy_path.exists() else None
    if current and current.stat().st_size > MAX_LOCK_BYTES:
        raise ValueError(f"Installation lock exceeds 1 MiB: {current}")
    lock = read_json(current) if current else {"schema_version": 1, "skills": {}}
    if lock.get("schema_version") != 1 or not isinstance(lock.get("skills"), dict):
        raise ValueError(f"Unsupported or invalid installation lock: {current}")

    actions, conflicts, packages, records = [], [], {}, dict(lock["skills"])
    for name in selected:
        root = source / "skills" / name
        if root.parent.is_symlink() or package_name(root / "SKILL.md") != name:
            raise ValueError(f"Package name/path mismatch: {root}")
        packages[name] = snapshot(root)
        current_hashes = hashes(packages[name])
        dest = destination / name
        action = "install"
        if dest.exists() or dest.is_symlink():
            installed_hashes = hashes(snapshot(dest, ignore_caches=False))
            prior = lock["skills"].get(name)
            if prior is not None and installed_hashes != prior.get("files"):
                conflicts.append(f"{name}: managed copy has local edits")
            elif prior is None and installed_hashes != current_hashes:
                conflicts.append(f"{name}: existing folder is not managed by engineering-skills")
            action = "unchanged" if installed_hashes == current_hashes else "update"
            if prior is None and installed_hashes == current_hashes:
                action = "adopt-identical"
        entry = registry["skills"][name]
        record = {
            "version": entry["version"], "files": current_hashes,
            "dependencies": entry.get("dependencies", []),
            "roles": entry.get("roles", []),
            "use_when": entry.get("use_when", ""),
            "cues": entry.get("cues", []),
        }
        if "source" in entry:
            record["upstream"] = dict(registry["sources"][entry["source"]])
            record["upstream"]["path"] = entry["upstream_path"]
        records[name] = record
        actions.append({"skill": name, "action": action, "path": str(dest), "files": len(current_hashes)})

    conflicts.extend(catalog_conflicts(records, destination, selected))

    # A differently named directory may already expose one of the selected skill names.
    if destination.exists():
        for folder in destination.iterdir():
            if folder.name in selected or folder.is_symlink() or not folder.is_dir():
                continue
            skill = folder / "SKILL.md"
            if skill.is_file() and not skill.is_symlink():
                try:
                    duplicate = package_name(skill) in selected
                except ValueError:
                    duplicate = False  # Preserve unrelated, nonstandard skill folders.
                if duplicate:
                    conflicts.append(f"Duplicate selected skill in existing folder: {folder}")

    profile_entry = registry["profiles"].get(profile, {})
    report = {
        "mode": "apply" if apply else "preview", "target": str(target),
        "catalog": "host" if host else "project",
        "profile": profile, "actions": actions, "conflicts": conflicts,
        "optional_not_selected": [s for s in profile_entry.get("optional", []) if s not in selected],
        "note": profile_entry.get("note", "Custom selection; existing repository policy remains in charge."),
    }
    if current == legacy_path:
        report["replaces_lock"] = str(legacy_path)
    if conflicts:
        print(json.dumps(report, indent=2))
        return 2
    if apply:
        destination.mkdir(parents=True, exist_ok=True)
        new_lock = {"schema_version": 1, "skills": records}
        lock_text = json.dumps(new_lock, indent=2, sort_keys=True) + "\n"
        if len(lock_text.encode("utf-8")) > MAX_LOCK_BYTES:
            raise ValueError("The catalog lock would exceed 1 MiB")
        if current == legacy_path:
            # Migrate by an atomic rename before any other write, so the catalog
            # always has exactly one valid lock and a later failure leaves it readable.
            os.replace(legacy_path, lock_path)
        changed = [a for a in actions if a["action"] in ("install", "update")]
        # Stage on the target filesystem. Restore moved folders if publishing fails.
        with tempfile.TemporaryDirectory(prefix=".engineering-skills-stage-", dir=agents) as tmp:
            stage = Path(tmp)
            for action in changed:
                name = action["skill"]
                for relative, (data, mode) in packages[name].items():
                    path = stage / "new" / name / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                    path.chmod(mode)
            staged_lock = stage / "lock.json"
            staged_lock.write_text(lock_text, encoding="utf-8")
            moved, published = [], []
            try:
                for action in changed:
                    name = action["skill"]
                    dest = destination / name
                    if dest.exists():
                        backup = stage / "old" / name
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        dest.rename(backup)
                        moved.append((backup, dest))
                    (stage / "new" / name).rename(dest)
                    published.append(dest)
                for name in records:
                    if hashes(snapshot(destination / name, ignore_caches=False)) != records[name]["files"]:
                        raise ValueError(f"Installed hashes do not match: {name}")
                os.replace(staged_lock, lock_path)
            except Exception:
                for path in reversed(published):
                    shutil.rmtree(path)
                for backup, dest in reversed(moved):
                    backup.rename(dest)
                raise
        report["verified"] = True
        report["lock"] = str(lock_path)
    print(json.dumps(report, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[3], help="engineering-skills checkout")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--target", type=Path, help="existing target repository")
    destination.add_argument("--host", type=Path, help="existing host catalog directory")
    parser.add_argument("--profile", help="registry profile")
    parser.add_argument("--skill", action="append", default=[], help="select a skill; repeat to add more")
    parser.add_argument("--apply", action="store_true", help="apply the previewed selection")
    parser.add_argument("--list", action="store_true", help="list packages and profiles without writes")
    args = parser.parse_args()
    try:
        source = args.source.expanduser().resolve()
        registry = read_json(source / REGISTRY)
        if registry.get("schema_version") != 1:
            raise ValueError("Unsupported registry schema")
        if args.list:
            print(json.dumps(registry, indent=2))
            return 0
        if args.target is None and args.host is None:
            raise ValueError("--target or --host is required")
        target = (args.host or args.target).expanduser().resolve()
        if not target.is_dir() or target == source:
            raise ValueError("Destination must be an existing directory distinct from engineering-skills")
        selected = select(registry, args.profile, args.skill)
        return install(source, target, registry, selected, args.profile, args.apply, args.host is not None)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"bootstrap: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
