from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SKILLS = {
    "engineering-workflows": {
        "grill-me",
        "domain-modeling",
        "diagnosing-bugs",
        "comment-discipline",
        "tdd",
        "codebase-design",
        "conceptual-review",
        "contract-review",
        "repository-docs",
        "maintaining-docs",
    },
    "communication-tools": {
        "english",
        "concise",
    },
    "agent-control": {"orchestrate", "superpowers"},
    "frontend-design": {"frontend-design"},
}
CLAUDE_SKILLS = {
    "engineering-workflows": PLUGIN_SKILLS["engineering-workflows"],
    "communication-tools": {"english", "concise"},
    "agent-control": {"orchestrate", "superpowers"},
    "frontend-design": {"frontend-design"},
}
ALL_SKILLS = set().union(*PLUGIN_SKILLS.values())


def directory_names(path: Path) -> set[str]:
    return {item.name for item in path.iterdir() if item.is_dir()}


class DistributionTests(unittest.TestCase):
    def test_canonical_skill_set_is_exact(self) -> None:
        self.assertEqual(ALL_SKILLS, directory_names(ROOT / "skills"))
        total_memberships = sum(len(names) for names in PLUGIN_SKILLS.values())
        self.assertEqual(len(ALL_SKILLS), total_memberships)

    def test_exact_skill_set_in_every_plugin(self) -> None:
        for plugin, names in PLUGIN_SKILLS.items():
            self.assertEqual(names, directory_names(ROOT / "plugins" / plugin / "skills"))
        for plugin, names in CLAUDE_SKILLS.items():
            self.assertEqual(
                names,
                directory_names(ROOT / "adapters" / "claude" / "plugins" / plugin / "skills"),
            )

    def test_codex_is_explicit_only(self) -> None:
        for plugin, names in PLUGIN_SKILLS.items():
            root = ROOT / "plugins" / plugin / "skills"
            for name in names:
                metadata = (root / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertIn("allow_implicit_invocation: false", metadata, name)
                self.assertIn('icon_small: "./assets/icon.png"', metadata, name)
                self.assertIn('icon_large: "./assets/icon.png"', metadata, name)

    def test_claude_is_explicit_only(self) -> None:
        for plugin, names in CLAUDE_SKILLS.items():
            root = ROOT / "adapters" / "claude" / "plugins" / plugin / "skills"
            for name in names:
                skill = (root / name / "SKILL.md").read_text(encoding="utf-8")
                frontmatter = skill.split("---", 2)[1]
                self.assertIn("disable-model-invocation: true", frontmatter, name)

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

    def test_plugin_branding_is_packaged(self) -> None:
        for plugin in PLUGIN_SKILLS:
            canonical = (ROOT / "assets" / "plugins" / plugin / "plugin-icon.png").read_bytes()
            for path in [
                ROOT / "plugins" / plugin / "assets" / "plugin-icon.png",
                ROOT / "adapters" / "claude" / "plugins" / plugin / "assets" / "plugin-icon.png",
            ]:
                self.assertEqual(canonical, path.read_bytes(), path)

    def test_marketplaces_and_manifests_agree(self) -> None:
        codex_marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        claude_marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        for marketplace in (codex_marketplace, claude_marketplace):
            names = [entry["name"] for entry in marketplace["plugins"]]
            self.assertEqual(set(PLUGIN_SKILLS), set(names))
            self.assertEqual(len(PLUGIN_SKILLS), len(names))
        for plugin in PLUGIN_SKILLS:
            codex = json.loads((ROOT / "plugins" / plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
            claude = json.loads((ROOT / "adapters/claude/plugins" / plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            codex_entry = next(e for e in codex_marketplace["plugins"] if e["name"] == plugin)
            claude_entry = next(e for e in claude_marketplace["plugins"] if e["name"] == plugin)
            self.assertEqual({"source": "local", "path": f"./plugins/{plugin}"}, codex_entry["source"])
            self.assertEqual(f"./adapters/claude/plugins/{plugin}", claude_entry["source"])
            self.assertEqual(plugin, codex["name"])
            self.assertEqual(codex["name"], claude["name"])
            self.assertEqual(codex["version"], claude["version"])
            self.assertEqual(codex["version"], claude_entry["version"])
            self.assertRegex(codex["version"], r"^\d+\.\d+\.\d+$")
            self.assertEqual(codex["license"], claude["license"])
            for field in ("composerIcon", "logo", "logoDark"):
                self.assertEqual("./assets/plugin-icon.png", codex["interface"][field])

    def test_cross_host_boundaries_are_deliberate(self) -> None:
        self.assertEqual({"english", "concise"}, CLAUDE_SKILLS["communication-tools"])
        self.assertEqual({"orchestrate", "superpowers"}, CLAUDE_SKILLS["agent-control"])
        self.assertEqual(PLUGIN_SKILLS, CLAUDE_SKILLS)

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

    def test_frontmatter_descriptions_are_compact(self) -> None:
        for name in ALL_SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            frontmatter = text.split("---", 2)[1]
            description = next(
                line.split(":", 1)[1].strip().strip('"')
                for line in frontmatter.splitlines()
                if line.startswith("description:")
            )
            self.assertLessEqual(len(description), 180, name)

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
