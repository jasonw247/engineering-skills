"""Observable installation behavior, using isolated temporary repositories."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills/bootstrap-repo/scripts/bootstrap.py"


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / "target"
        self.target.mkdir()

    def run_bootstrap(self, *args, source=ROOT, expected=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(source),
             "--target", str(self.target), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout) if result.stdout else result.stderr

    def test_preview_does_not_write(self):
        report = self.run_bootstrap("--profile", "agent-harness")
        self.assertEqual(report["mode"], "preview")
        self.assertEqual(list(self.target.iterdir()), [])
        self.assertIn("tdd", report["optional_not_selected"])

    def test_apply_copies_complete_packages_and_preserves_repository(self):
        for name in ("AGENTS.md", "harness.yaml"):
            (self.target / name).write_text("existing content\n")
        report = self.run_bootstrap("--profile", "agent-harness", "--apply")
        self.assertTrue(report["verified"])
        installed = self.target / ".agents/skills"
        self.assertEqual(len(list(installed.iterdir())), 5)
        self.assertTrue((installed / "codebase-design/DEEPENING.md").is_file())
        self.assertTrue((installed / "writing-for-agents/LICENSE").is_file())
        for name in ("AGENTS.md", "harness.yaml"):
            self.assertEqual((self.target / name).read_text(), "existing content\n")
        lock = json.loads((self.target / ".agents/skills.lock.json").read_text())
        self.assertEqual(lock["skills"]["retro"]["upstream"]["revision"],
                         "49dd158d1076134a641b33efb035946536778336")

    def test_dependencies_and_idempotent_repeat(self):
        self.run_bootstrap("--skill", "tdd", "--apply")
        self.assertTrue((self.target / ".agents/skills/codebase-design/SKILL.md").is_file())
        report = self.run_bootstrap("--skill", "tdd", "--apply")
        self.assertTrue(all(a["action"] == "unchanged" for a in report["actions"]))

    def test_simplification_is_optional_and_installs_as_an_actor_package(self):
        report = self.run_bootstrap("--profile", "agent-harness", "--apply")
        self.assertIn("diff-simplification", report["optional_not_selected"])
        package = self.target / ".agents/skills/diff-simplification"
        self.assertFalse(package.exists())
        report = self.run_bootstrap("--skill", "diff-simplification", "--apply")
        self.assertTrue(report["verified"])
        self.assertEqual((package / "references/sources.md").read_bytes(),
                         (ROOT / "skills/diff-simplification/references/sources.md").read_bytes())
        lock = json.loads((self.target / ".agents/skills.lock.json").read_text())
        self.assertEqual(lock["skills"]["diff-simplification"]["roles"], ["actor"])
        self.assertEqual(lock["skills"]["diff-simplification"]["dependencies"], [])

    def test_host_catalog_is_locked_and_includes_selection_metadata(self):
        host = Path(self.temp.name) / "host"
        host.mkdir()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(ROOT), "--host", str(host),
             "--skill", "tdd", "--apply"], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["catalog"], "host")
        self.assertTrue((host / "skills/tdd/SKILL.md").is_file())
        self.assertFalse((host / ".agents").exists())
        lock = json.loads((host / "skills.lock.json").read_text())
        self.assertEqual(lock["skills"]["tdd"]["dependencies"], ["codebase-design"])
        self.assertEqual(lock["skills"]["tdd"]["roles"], ["actor"])
        self.assertIn("test", lock["skills"]["tdd"]["cues"])

    def test_partial_legacy_upgrade_fails_before_writes_then_explicit_upgrade_succeeds(self):
        for host in (False, True):
            with self.subTest(host=host):
                target = Path(self.temp.name) / ("host-upgrade" if host else "project-upgrade")
                target.mkdir()
                command = [sys.executable, str(SCRIPT), "--source", str(ROOT),
                           "--host" if host else "--target", str(target)]
                subprocess.run(command + ["--skill", "tdd", "--apply"], check=True,
                               capture_output=True)
                base = target if host else target / ".agents"
                lock_path = base / "skills.lock.json"
                lock = json.loads(lock_path.read_text())
                for field in ("roles", "use_when", "cues"):
                    del lock["skills"]["tdd"][field]
                lock_path.write_text(json.dumps(lock))
                before = lock_path.read_bytes()
                for mode in ([], ["--apply"]):
                    result = subprocess.run(command + ["--skill", "diff-simplification"] + mode,
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("--skill tdd", result.stdout + result.stderr)
                    self.assertEqual(lock_path.read_bytes(), before)
                    self.assertFalse((base / "skills/diff-simplification").exists())
                result = subprocess.run(command + ["--skill", "tdd", "--skill",
                                         "diff-simplification", "--apply"],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(json.loads(result.stdout)["verified"])
                upgraded = json.loads(lock_path.read_text())
                self.assertEqual(upgraded["skills"]["tdd"]["roles"], ["actor"])

    def test_invalid_retained_metadata_blocks_new_install(self):
        self.run_bootstrap("--skill", "tdd", "--apply")
        lock_path = self.target / ".agents/skills.lock.json"
        original = json.loads(lock_path.read_text())
        for field, value in (("roles", []), ("roles", ["administrator"]),
                             ("use_when", " "), ("cues", [""]),
                             ("dependencies", ["not-installed"]),
                             ("version", " "), ("upstream", "elsewhere"),
                             ("upstream", None)):
            with self.subTest(field=field, value=value):
                lock = json.loads(json.dumps(original))
                lock["skills"]["tdd"][field] = value
                lock_path.write_text(json.dumps(lock))
                before = lock_path.read_bytes()
                self.run_bootstrap("--skill", "diff-simplification", "--apply", expected=2)
                self.assertEqual(lock_path.read_bytes(), before)
                self.assertFalse((self.target / ".agents/skills/diff-simplification").exists())

    def test_damaged_retained_package_blocks_new_install(self):
        self.run_bootstrap("--skill", "tdd", "--apply")
        path = self.target / ".agents/skills/tdd/SKILL.md"
        path.write_text(path.read_text() + "\nLocal instruction.\n")
        lock_path = self.target / ".agents/skills.lock.json"
        before = lock_path.read_bytes()
        report = self.run_bootstrap("--skill", "diff-simplification", "--apply", expected=2)
        self.assertIn("tdd", str(report))
        self.assertEqual(lock_path.read_bytes(), before)
        self.assertFalse((self.target / ".agents/skills/diff-simplification").exists())

    def test_local_edit_blocks_entire_selection(self):
        self.run_bootstrap("--skill", "handoff", "--apply")
        path = self.target / ".agents/skills/handoff/SKILL.md"
        path.write_text(path.read_text() + "\nLocal instruction.\n")
        lock = (self.target / ".agents/skills.lock.json").read_bytes()
        report = self.run_bootstrap("--profile", "agent-harness", "--apply", expected=2)
        self.assertIn("local edits", report["conflicts"][0])
        self.assertFalse((self.target / ".agents/skills/retro").exists())
        self.assertTrue(path.read_text().endswith("Local instruction.\n"))
        self.assertEqual((self.target / ".agents/skills.lock.json").read_bytes(), lock)

    def test_unmanaged_conflict_is_preserved(self):
        path = self.target / ".agents/skills/handoff"
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("my existing skill\n")
        report = self.run_bootstrap("--skill", "handoff", "--apply", expected=2)
        self.assertIn("not managed", report["conflicts"][0])
        self.assertEqual((path / "SKILL.md").read_text(), "my existing skill\n")
        self.assertFalse((self.target / ".agents/skills.lock.json").exists())

    def test_symlink_destination_is_rejected(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (self.target / ".agents").symlink_to(outside, target_is_directory=True)
        error = self.run_bootstrap("--skill", "handoff", "--apply", expected=2)
        self.assertIn("symlinked", error)
        self.assertEqual(list(outside.iterdir()), [])

    def test_unknown_skill_does_not_write(self):
        self.run_bootstrap("--skill", "../../escape", "--apply", expected=2)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_update_unchanged_managed_copy_and_keep_unselected_skills(self):
        source = Path(self.temp.name) / "source"
        shutil.copytree(ROOT / "skills", source / "skills")
        self.run_bootstrap("--skill", "handoff", "--skill", "retro", "--apply", source=source)
        package = source / "skills/handoff/SKILL.md"
        package.write_text(package.read_text() + "\nUpdated curated instruction.\n")
        report = self.run_bootstrap("--skill", "handoff", "--apply", source=source)
        self.assertEqual(report["actions"][0]["action"], "update")
        self.assertEqual((self.target / ".agents/skills/handoff/SKILL.md").read_bytes(), package.read_bytes())
        self.assertTrue((self.target / ".agents/skills/retro/SKILL.md").is_file())

    def test_cyclic_dependency_does_not_write(self):
        source = Path(self.temp.name) / "source"
        shutil.copytree(ROOT / "skills", source / "skills")
        path = source / "skills/bootstrap-repo/references/registry.json"
        registry = json.loads(path.read_text())
        registry["skills"]["codebase-design"]["dependencies"] = ["tdd"]
        path.write_text(json.dumps(registry))
        error = self.run_bootstrap("--skill", "tdd", "--apply", source=source, expected=2)
        self.assertIn("Cyclic", error)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_duplicate_name_in_another_folder_does_not_write(self):
        path = self.target / ".agents/skills/custom-handoff"
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("---\nname: handoff\ndescription: custom\n---\n")
        report = self.run_bootstrap("--skill", "handoff", "--apply", expected=2)
        self.assertIn("Duplicate", report["conflicts"][0])
        self.assertFalse((self.target / ".agents/skills/handoff").exists())

    def test_unrelated_nonstandard_folder_is_preserved(self):
        path = self.target / ".agents/skills/custom"
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text("existing nonstandard instructions\n")
        self.run_bootstrap("--skill", "handoff", "--apply")
        self.assertEqual((path / "SKILL.md").read_text(), "existing nonstandard instructions\n")

    def test_source_symlink_does_not_escape_or_write(self):
        source = Path(self.temp.name) / "source"
        shutil.copytree(ROOT / "skills", source / "skills")
        (source / "skills/handoff/linked.txt").symlink_to(self.target / "missing")
        error = self.run_bootstrap("--skill", "handoff", "--apply", source=source, expected=2)
        self.assertIn("regular skill file", error)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_every_skill_folder_is_registered_and_installs_cleanly(self):
        registry = json.loads((ROOT / "skills/bootstrap-repo/references/registry.json").read_text())
        disk_skills = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
        self.assertEqual(set(registry["skills"]), disk_skills)
        args = [item for name in sorted(disk_skills) for item in ("--skill", name)]
        report = self.run_bootstrap(*args, "--apply")
        self.assertTrue(report["verified"])
        installed = {p.name for p in (self.target / ".agents/skills").iterdir() if p.is_dir()}
        self.assertEqual(installed, disk_skills)


if __name__ == "__main__":
    unittest.main()
