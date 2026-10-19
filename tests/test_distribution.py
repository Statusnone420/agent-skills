from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_adapters

ALL_SKILLS = set(build_adapters.SKILLS)
PLUGINS = build_adapters.PLUGINS
MAX_SKILL_FILE_BYTES = 16 * 1024


def directory_names(path: Path) -> set[str]:
    return {item.name for item in path.iterdir() if item.is_dir()}


def frontmatter(path: Path) -> dict[str, str]:
    block = path.read_text(encoding="utf-8").split("---", 2)[1]
    fields = (line.split(":", 1) for line in block.splitlines() if ":" in line)
    return {key.strip(): value.strip().strip('"') for key, value in fields}


class DistributionTests(unittest.TestCase):
    def test_generated_files_match_catalog_and_canonical_skills(self) -> None:
        build_adapters.validate_configuration()
        self.assertEqual([], build_adapters.find_drift())

    def test_drift_check_compares_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            expected = Path(temp) / "expected"
            actual = Path(temp) / "actual"
            for root in (expected, actual):
                (root / "skill").mkdir(parents=True)
            (expected / "skill" / "SKILL.md").write_bytes(b"same size\n")
            (actual / "skill" / "SKILL.md").write_bytes(b"same SIZE\n")
            shutil.copystat(expected / "skill" / "SKILL.md", actual / "skill" / "SKILL.md")
            (expected / "skill" / "notes.md").write_bytes(b"kept\n")
            (actual / "skill" / "stale.md").write_bytes(b"left over\n")
            (expected / "marketplace.json").write_bytes(b"{}\n")
            (actual / "marketplace.json").write_bytes(b"[]\n")
            shutil.copystat(expected / "marketplace.json", actual / "marketplace.json")

            tree = build_adapters.compare(expected / "skill", actual / "skill")
            single = build_adapters.compare(expected / "marketplace.json", actual / "marketplace.json")

        kinds = sorted(problem.split(":")[0] + " " + problem.rsplit("/", 1)[-1] for problem in tree)
        self.assertEqual(["changed SKILL.md", "missing notes.md", "unexpected stale.md"], kinds)
        self.assertEqual(1, len(single))
        self.assertTrue(single[0].startswith("changed: "), single)

    def test_skill_files_stay_under_16_kb(self) -> None:
        for root in (ROOT / "skills", ROOT / "plugins", ROOT / "adapters"):
            for path in root.rglob("*"):
                if path.is_file() and path.suffix != ".png":
                    self.assertLess(path.stat().st_size, MAX_SKILL_FILE_BYTES, path)

    def test_canonical_skill_set_is_exact(self) -> None:
        self.assertEqual(ALL_SKILLS, directory_names(ROOT / "skills"))
        memberships = [name for plugin in PLUGINS.values() for name in plugin.skills]
        self.assertEqual(sorted(ALL_SKILLS), sorted(memberships))

    def test_codex_is_explicit_only(self) -> None:
        for plugin, definition in PLUGINS.items():
            root = ROOT / "plugins" / plugin / "skills"
            for name in definition.skills:
                metadata = (root / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn("allow_implicit_invocation: false", metadata, name)
                self.assertIn('icon_small: "./assets/icon.png"', metadata, name)
                self.assertIn('icon_large: "./assets/icon.png"', metadata, name)

    def test_claude_is_explicit_only(self) -> None:
        for plugin, definition in PLUGINS.items():
            root = ROOT / "adapters" / "claude" / "plugins" / plugin / "skills"
            for name in definition.skills:
                skill = (root / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("disable-model-invocation: true", skill.split("---", 2)[1], name)

    def test_every_canonical_skill_has_a_unique_icon(self) -> None:
        digests = {
            hashlib.sha256((ROOT / "skills" / name / "assets" / "icon.png").read_bytes()).hexdigest()
            for name in ALL_SKILLS
        }
        self.assertEqual(len(ALL_SKILLS), len(digests))

    def test_retired_skill_artwork_is_preserved(self) -> None:
        artwork = ROOT / "assets" / "retired-skills"
        self.assertEqual(
            {
                "grilling.png",
                "grill-with-docs.png",
                "prompting-opus-5.png",
                "prompting-fable-5.png",
                "luna-subagents.png",
                "ask-pro.png",
                "claude-handoff.png",
            },
            {path.name for path in artwork.glob("*.png")},
        )

    def test_marketplace_entries_resolve_to_matching_manifests(self) -> None:
        codex_marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        claude_marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(list(PLUGINS), [entry["name"] for entry in codex_marketplace["plugins"]])
        self.assertEqual(list(PLUGINS), [entry["name"] for entry in claude_marketplace["plugins"]])
        for entry in codex_marketplace["plugins"]:
            plugin_root = ROOT / entry["source"]["path"]
            manifest = json.loads((plugin_root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(entry["name"], manifest["name"])
            self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
            self.assertTrue((plugin_root / manifest["skills"]).is_dir(), entry["name"])
            for field in ("composerIcon", "logo", "logoDark"):
                self.assertTrue((plugin_root / manifest["interface"][field]).is_file(), field)
        for entry in claude_marketplace["plugins"]:
            plugin_root = ROOT / entry["source"]
            manifest = json.loads((plugin_root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(entry["name"], manifest["name"])
            self.assertEqual(entry["version"], manifest["version"])
            self.assertTrue((plugin_root / "skills").is_dir(), entry["name"])

    def test_consolidated_skills_keep_specialist_routes(self) -> None:
        grill_me = (ROOT / "skills" / "grill-me" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("$domain-modeling", grill_me)

    def test_orchestrate_uses_host_native_variants(self) -> None:
        source = ROOT / "skills/orchestrate"
        codex = ROOT / "plugins/agent-control/skills/orchestrate"
        claude = ROOT / "adapters/claude/plugins/agent-control/skills/orchestrate"
        self.assertEqual((source / "SKILL.md").read_bytes(), (codex / "SKILL.md").read_bytes())
        native = (source / "variants/claude.md").read_text(encoding="utf-8")
        generated = (claude / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(native, generated.replace("disable-model-invocation: true\n", "", 1))
        self.assertNotEqual(native, (source / "SKILL.md").read_text(encoding="utf-8"))
        for token in ("Luna", "Terra", "Sol", "Astra", "gpt-"):
            self.assertNotIn(token, native)
        for folder in (codex, claude):
            self.assertFalse((folder / "variants").exists())
        self.assertEqual({"claude.md"}, {p.name for p in (source / "variants").iterdir()})

    def test_retired_hosts_are_absent_from_active_distribution(self) -> None:
        self.assertEqual({"claude"}, directory_names(ROOT / "adapters"))
        self.assertFalse((ROOT / ".cursor-plugin").exists())
        self.assertFalse((ROOT / "marketplace.json").exists())

    def test_retired_host_artwork_is_preserved(self) -> None:
        archive = ROOT / "assets/retired-hosts"
        manifest = json.loads((archive / "manifest.json").read_text(encoding="utf-8"))
        # The retirement snapshot is fixed even when the active catalog grows.
        self.assertEqual(38, len(manifest))
        actual = {
            p.relative_to(archive).as_posix()
            for host in ("cursor", "zcode")
            for p in (archive / host).rglob("*")
            if p.is_file()
        }
        self.assertEqual(set(manifest), actual)
        for relative, digest in manifest.items():
            path = Path(relative)
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertIn(path.parts[0], {"cursor", "zcode"})
            self.assertEqual(".png", path.suffix)
            self.assertEqual(
                digest, hashlib.sha256((archive / path).read_bytes()).hexdigest(), relative
            )

    def test_comment_discipline_rejects_comment_backed_shortcuts(self) -> None:
        skill = (ROOT / "skills" / "comment-discipline" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Comments are not implementation", skill)
        self.assertIn("fix the root cause", skill)
        self.assertIn("Treat comment-shaped directives as executable code", skill)
        self.assertIn("Never measure success by deletion count", skill)

    def test_frontmatter_names_match_folders_and_descriptions_are_compact(self) -> None:
        for name in ALL_SKILLS:
            fields = frontmatter(ROOT / "skills" / name / "SKILL.md")
            self.assertEqual(name, fields.get("name"), name)
            self.assertLessEqual(len(fields["description"]), 180, name)

    def test_skill_references_resolve_and_stale_syntax_is_absent(self) -> None:
        skill_reference = re.compile(r"\$([a-z][a-z0-9-]+)")
        slash_reference = re.compile(r"`/[a-z][a-z0-9-]+`")
        for path in (ROOT / "skills").rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertEqual([], slash_reference.findall(text), path)
            self.assertNotIn("fork_context", text, path)
            for name in skill_reference.findall(text):
                self.assertIn(name, ALL_SKILLS, f"{path}: ${name}")

    def test_attribution_and_subdirectory_license_are_present(self) -> None:
        origin = (ROOT / "ORIGIN.md").read_text(encoding="utf-8")
        self.assertIn("anthropics/skills", origin)
        self.assertIn("obra/superpowers", origin)
        apache = (ROOT / "skills" / "frontend-design" / "LICENSE.txt").read_text(encoding="utf-8")
        self.assertIn("Apache License", apache)

    def test_distribution_contains_no_workflow_hooks(self) -> None:
        roots = [ROOT / "skills", ROOT / "plugins", ROOT / "adapters"]
        matches = [
            path
            for root in roots
            for path in root.rglob("*")
            if "hook" in path.name.lower() or "pre-commit" in path.name.lower()
        ]
        self.assertEqual([], matches)


if __name__ == "__main__":
    unittest.main()
