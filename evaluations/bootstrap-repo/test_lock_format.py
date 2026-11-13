"""The version 1 catalog lock format: the published example and installer output conform."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/bootstrap-repo/scripts/bootstrap.py"
EXAMPLE = Path(__file__).resolve().parent / "fixtures/catalog-v1"
LOCK, LEGACY_LOCK = "skills.lock.json", "skill-repo.lock.json"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def check_catalog(base):
    """Apply the reader rules of references/lock-format.md; return the problems found."""
    present = [base / name for name in (LOCK, LEGACY_LOCK)
               if (base / name).exists() or (base / name).is_symlink()]
    if len(present) != 1:
        return [f"expected exactly one of {LOCK} or {LEGACY_LOCK}"]
    path = present[0]
    if path.is_symlink() or path.stat().st_size > 1024 * 1024:
        return ["lock is a symlink or exceeds 1 MiB"]
    lock = json.loads(path.read_text(encoding="utf-8"))
    if lock.get("schema_version") != 1 or not isinstance(lock.get("skills"), dict):
        return ["unsupported schema_version or skills"]
    skills, problems = lock["skills"], []

    def strings(value, allow_empty=False):
        return isinstance(value, list) and (allow_empty or value) and all(
            isinstance(item, str) and item.strip() for item in value)

    for name, record in skills.items():
        if not NAME.fullmatch(name) or not isinstance(record, dict):
            problems.append(f"{name}: invalid name or record")
            continue
        version, files = record.get("version"), record.get("files")
        if not (isinstance(version, str) and version.strip()):
            problems.append(f"{name}: invalid version")
        dependencies = record.get("dependencies", [])
        if not (strings(dependencies, allow_empty=True)
                and all(NAME.fullmatch(dep) and dep in skills for dep in dependencies)):
            problems.append(f"{name}: invalid or missing dependency")
        roles = record.get("roles")
        if not (strings(roles) and set(roles) <= {"actor", "reviewer"}):
            problems.append(f"{name}: invalid roles")
        if not (isinstance(record.get("use_when"), str) and record["use_when"].strip()
                and strings(record.get("cues"))):
            problems.append(f"{name}: missing selection metadata")
        if "upstream" in record and not isinstance(record["upstream"], dict):
            problems.append(f"{name}: invalid upstream")
        if not (isinstance(files, dict) and "SKILL.md" in files
                and all(SHA256.fullmatch(str(value)) for value in files.values())):
            problems.append(f"{name}: invalid files")
            continue
        root = base / "skills" / name
        if root.is_symlink() or not root.is_dir():
            problems.append(f"{name}: missing package directory")
            continue
        actual = {}
        for item in sorted(root.rglob("*")):
            if item.is_symlink():
                problems.append(f"{name}: symlink {item.relative_to(root).as_posix()}")
            elif item.is_file():
                actual[item.relative_to(root).as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
        if actual != files:
            problems.append(f"{name}: package files do not match the lock")

    visiting, done = set(), set()

    def visit(name):
        if name in done or name not in skills or not isinstance(skills[name], dict):
            return
        if name in visiting:
            problems.append(f"{name}: dependency cycle")
            return
        visiting.add(name)
        for dependency in skills[name].get("dependencies") or []:
            visit(dependency)
        visiting.discard(name)
        done.add(name)

    for name in skills:
        visit(name)
    return problems


def load_installer():
    spec = importlib.util.spec_from_file_location("bootstrap_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edit_lock(base, edit):
    path = base / LOCK
    lock = json.loads(path.read_text(encoding="utf-8"))
    edit(lock)
    path.write_text(json.dumps(lock), encoding="utf-8")


class LockFormatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / "target"
        self.target.mkdir()

    def bootstrap(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(ROOT), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout) if result.stdout else result.stderr

    def copy_example(self):
        base = Path(self.temp.name) / "example"
        shutil.copytree(EXAMPLE, base)
        return base

    def test_published_example_conforms(self):
        self.assertEqual(check_catalog(EXAMPLE), [])
        # Optional fields may be absent.
        base = self.copy_example()
        edit_lock(base, lambda lock: lock["skills"]["example-design"].pop("dependencies"))
        self.assertEqual(check_catalog(base), [])

    def test_installer_output_conforms_and_uses_the_generic_name(self):
        self.bootstrap("--target", str(self.target), "--profile", "agent-harness", "--apply")
        agents = self.target / ".agents"
        self.assertTrue((agents / LOCK).is_file())
        self.assertFalse((agents / LEGACY_LOCK).exists())
        self.assertEqual(check_catalog(agents), [])
        host = Path(self.temp.name) / "host"
        host.mkdir()
        self.bootstrap("--host", str(host), "--skill", "tdd", "--apply")
        self.assertEqual(check_catalog(host), [])

    def test_checker_rejects_catalogs_that_break_the_format(self):
        def drop(field):
            return lambda base: edit_lock(base, lambda lock: lock["skills"]["example-review"].pop(field))

        def set_field(field, value):
            def apply(base):
                edit_lock(base, lambda lock: lock["skills"]["example-review"].__setitem__(field, value))
            return apply

        def rename(base):
            def apply(lock):
                lock["skills"]["Example_Review"] = lock["skills"].pop("example-review")
            edit_lock(base, apply)

        def cycle(base):
            edit_lock(base, lambda lock: lock["skills"]["example-design"].__setitem__(
                "dependencies", ["example-review"]))

        cases = [
            ("unsupported schema_version", lambda base: edit_lock(
                base, lambda lock: lock.__setitem__("schema_version", 2))),
            ("missing selection metadata", drop("cues")),
            ("invalid roles", set_field("roles", ["critic"])),
            ("invalid version", set_field("version", "")),
            ("invalid or missing dependency", set_field("dependencies", ["absent"])),
            ("invalid upstream", set_field("upstream", "elsewhere")),
            ("invalid upstream", set_field("upstream", None)),
            ("invalid name", rename),
            ("dependency cycle", cycle),
            ("package files do not match", lambda base: (
                base / "skills/example-review/references/checklist.md").write_text("changed")),
            ("package files do not match", lambda base: (
                base / "skills/example-design/notes.md").write_text("unlisted")),
            ("expected exactly one", lambda base: shutil.copy(base / LOCK, base / LEGACY_LOCK)),
        ]
        for expected, break_catalog in cases:
            with self.subTest(expected):
                base = self.copy_example()
                break_catalog(base)
                problems = check_catalog(base)
                self.assertTrue(any(expected in problem for problem in problems), problems)
                shutil.rmtree(base)

    def test_original_lock_name_is_replaced_on_apply(self):
        self.bootstrap("--target", str(self.target), "--skill", "code-review", "--apply")
        agents = self.target / ".agents"
        (agents / LOCK).rename(agents / LEGACY_LOCK)
        preview = self.bootstrap("--target", str(self.target), "--skill", "code-review")
        self.assertEqual(Path(preview["replaces_lock"]), (agents / LEGACY_LOCK).resolve())
        self.assertTrue((agents / LEGACY_LOCK).exists())
        self.bootstrap("--target", str(self.target), "--skill", "code-review", "--apply")
        self.assertTrue((agents / LOCK).is_file())
        self.assertFalse((agents / LEGACY_LOCK).exists())
        self.assertEqual(check_catalog(agents), [])

    def test_failed_migration_leaves_one_readable_lock(self):
        self.bootstrap("--target", str(self.target), "--skill", "code-review", "--apply")
        agents = self.target / ".agents"
        (agents / LOCK).rename(agents / LEGACY_LOCK)
        before = (agents / LEGACY_LOCK).read_bytes()
        # Publishing a new package into a read-only skills folder fails after migration.
        (agents / "skills").chmod(0o555)
        try:
            self.bootstrap("--target", str(self.target), "--skill", "tdd", "--apply", expected=2)
        finally:
            (agents / "skills").chmod(0o755)
        self.assertFalse((agents / LEGACY_LOCK).exists())
        self.assertEqual((agents / LOCK).read_bytes(), before)
        self.assertFalse((agents / "skills/tdd").exists())
        self.assertEqual(check_catalog(agents), [])

    def test_migration_never_exposes_two_lock_names(self):
        self.bootstrap("--target", str(self.target), "--skill", "code-review", "--apply")
        agents = self.target / ".agents"
        (agents / LOCK).rename(agents / LEGACY_LOCK)
        installer = load_installer()
        states, real_replace = [], installer.os.replace

        def observed_replace(source, destination):
            real_replace(source, destination)
            states.append(((agents / LOCK).exists(), (agents / LEGACY_LOCK).exists()))

        # Deleting any file fails, as when the original lock cannot be removed.
        with mock.patch.object(installer.os, "replace", observed_replace), \
                mock.patch.object(Path, "unlink", side_effect=OSError("simulated deletion failure")), \
                contextlib.redirect_stdout(io.StringIO()):
            registry = installer.read_json(ROOT / installer.REGISTRY)
            selected = installer.select(registry, None, ["tdd"])
            installer.install(ROOT, self.target.resolve(), registry, selected, None, True)
        self.assertTrue(states)
        self.assertNotIn((True, True), states)
        self.assertEqual(((agents / LOCK).exists(), (agents / LEGACY_LOCK).exists()), (True, False))
        self.assertEqual(check_catalog(agents), [])

    def test_oversized_lock_is_refused(self):
        self.bootstrap("--target", str(self.target), "--skill", "code-review", "--apply")
        lock_path = self.target / ".agents" / LOCK
        edit_lock(lock_path.parent, lambda lock: lock.__setitem__("padding", "x" * (1024 * 1024)))
        before = lock_path.read_bytes()
        error = self.bootstrap("--target", str(self.target), "--skill", "tdd", "--apply", expected=2)
        self.assertIn("exceeds 1 MiB", error)
        self.assertEqual(lock_path.read_bytes(), before)

    def test_both_lock_names_block_installation(self):
        self.bootstrap("--target", str(self.target), "--skill", "code-review", "--apply")
        agents = self.target / ".agents"
        shutil.copy(agents / LOCK, agents / LEGACY_LOCK)
        before = (agents / LOCK).read_bytes()
        error = self.bootstrap("--target", str(self.target), "--skill", "tdd", "--apply", expected=2)
        self.assertIn("remove the stale one", error)
        self.assertEqual((agents / LOCK).read_bytes(), before)
        self.assertFalse((agents / "skills/tdd").exists())


if __name__ == "__main__":
    unittest.main()
