from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
PLUGIN_ASSETS = ROOT / "assets" / "plugins"
CODEX_PLUGINS = ROOT / "plugins"
CLAUDE_PLUGINS = ROOT / "adapters" / "claude" / "plugins"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

AUTHOR = "Statusnone"
AUTHOR_URL = "https://github.com/Statusnone420"
REPOSITORY = "https://github.com/Statusnone420/agent-skills"
PLUGIN_ICON = "./assets/plugin-icon.png"
MARKETPLACE_NAME = "statusnone-agent-skills"
MARKETPLACE_DISPLAY_NAME = "Agent Skills"
MARKETPLACE_DESCRIPTION = "One plugin of focused agent skills, maintained by Statusnone."
CLAUDE_ONLY_FRONTMATTER = "disable-model-invocation:"
YAML_RESERVED_STARTS = tuple("[{&*!|>%@`#")


def write_text_lf(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_lf(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


@dataclass(frozen=True)
class SkillMetadata:
    display_name: str
    short_description: str
    default_prompt: str | None = None
    implicit: bool = True


@dataclass(frozen=True)
class PluginDefinition:
    skills: tuple[str, ...]
    version: str
    description: str
    display_name: str
    short_description: str
    long_description: str
    category: str
    capabilities: tuple[str, ...]
    keywords: tuple[str, ...]
    brand_color: str
    default_prompts: tuple[str, ...]
    license: str = "MIT"


SKILLS = {
    "codebase-design": SkillMetadata(
        "Codebase Design",
        "Design deep modules and real seams",
        "Review this module's interface and propose a deeper design with fewer, clearer seams.",
    ),
    "conceptual-review": SkillMetadata(
        "Conceptual Review",
        "Check reasoning or a spec before building",
        "Check whether this plan or implementation spec holds up before we build it.",
    ),
    "concise": SkillMetadata(
        "Concise",
        "Shortest complete answer, nothing lost",
        "Give me the shortest complete answer, keeping every fact, caveat, and next step.",
    ),
    "diagnosing-bugs": SkillMetadata(
        "Diagnosing Bugs",
        "Root-cause hard bugs with a tight loop",
        "Find the root cause of this bug with a fast, repeatable reproduction.",
    ),
    "english": SkillMetadata(
        "English",
        "Plain-English explanation, no action",
        "Explain the selected text or current situation in plain English without taking action.",
        implicit=False,
    ),
    "frontend-design": SkillMetadata(
        "Frontend Design",
        "Distinctive, accessible interface design",
        "Give this interface a distinctive visual direction that meets the accessibility floor.",
    ),
    "maintaining-docs": SkillMetadata(
        "Maintaining Docs",
        "Update docs from verified evidence",
        "Update this repository's documentation to match the verified change.",
    ),
    "orchestrate": SkillMetadata(
        "Orchestrate",
        "Coordinate focused subagents",
        "Delegate the independent parts of this task to focused subagents and integrate the results.",
        implicit=False,
    ),
    "repository-docs": SkillMetadata(
        "Repository Docs",
        "Find the guidance a task needs",
        "Find and load the repository guidance I need for this task.",
    ),
}

HOST_VARIANTS = {
    "orchestrate": frozenset({"claude"}),
}


PLUGINS = {
    "agent-skills": PluginDefinition(
        skills=tuple(SKILLS),
        version="1.1.0",
        description=(
            "Focused peer skills for codebase design, debugging, reviews, docs, plain English, "
            "frontend design, and subagents."
        ),
        display_name="Agent Skills",
        short_description="Focused skills for everyday agent work",
        long_description=(
            "Nine peer skills: codebase design, conceptual and spec review, concise answers, bug "
            "diagnosis, plain-English explanations, frontend design, documentation lookup and "
            "upkeep, and subagent orchestration."
        ),
        category="Developer Tools",
        capabilities=("Interactive", "Read", "Write"),
        keywords=(
            "skills",
            "debugging",
            "design",
            "documentation",
            "review",
            "frontend",
            "communication",
            "orchestration",
        ),
        brand_color="#6D4AFF",
        default_prompts=(
            "Find the root cause of this flaky test.",
            "Check whether this plan holds up before we build it.",
            "Give this page a distinctive visual direction.",
        ),
        license="MIT AND Apache-2.0",
    ),
}


def add_claude_manual_only(skill_md: Path) -> None:
    text = skill_md.read_text(encoding="utf-8")
    closing = text.find("\n---", 4)
    if closing == -1:
        raise ValueError(f"Missing closing frontmatter marker: {skill_md}")
    text = text[:closing] + "\ndisable-model-invocation: true" + text[closing:]
    write_text_lf(skill_md, text)


def add_codex_metadata(skill_dir: Path, name: str) -> None:
    metadata = SKILLS[name]
    agents = skill_dir / "agents"
    agents.mkdir(exist_ok=True)
    lines = [
        "interface:",
        f'  display_name: "{metadata.display_name}"',
        f'  short_description: "{metadata.short_description}"',
    ]
    if metadata.default_prompt:
        lines.append(f'  default_prompt: "{metadata.default_prompt}"')
    lines.extend(
        [
            '  icon_small: "./assets/icon.png"',
            '  icon_large: "./assets/icon.png"',
            "policy:",
            f"  allow_implicit_invocation: {'true' if metadata.implicit else 'false'}",
        ]
    )
    write_text_lf(agents / "openai.yaml", "\n".join(lines) + "\n")


def variant_file_name(host: str) -> str:
    # A plain "claude.md" would load as CLAUDE.md on case-insensitive file systems.
    return f"{host}.SKILL.md"


def apply_host_variant(skill_dir: Path, name: str, host: str) -> None:
    variants = skill_dir / "variants"
    expected_hosts = HOST_VARIANTS.get(name)
    if expected_hosts is None:
        if variants.exists():
            raise ValueError(f"Unexpected host variants: {variants}")
        return

    if not variants.is_dir():
        raise ValueError(f"Missing host variants: {variants}")
    expected_files = {variant_file_name(expected_host) for expected_host in expected_hosts}
    actual_files = {path.name for path in variants.iterdir()}
    if actual_files != expected_files:
        raise ValueError(
            f"Host variant mismatch for {name}: expected {sorted(expected_files)}, "
            f"found {sorted(actual_files)}"
        )
    if host != "codex":
        shutil.copyfile(variants / variant_file_name(host), skill_dir / "SKILL.md")
    shutil.rmtree(variants)


def copy_skills(names: tuple[str, ...], destination: Path, host: str) -> None:
    destination.mkdir(parents=True)
    for name in names:
        skill_dir = destination / name
        shutil.copytree(SOURCE / name, skill_dir)
        apply_host_variant(skill_dir, name, host)
        if host == "codex":
            add_codex_metadata(skill_dir, name)
        elif host == "claude":
            if not SKILLS[name].implicit:
                add_claude_manual_only(skill_dir / "SKILL.md")
        else:
            raise ValueError(f"Unsupported host: {host}")


def repository_path(path: Path) -> str:
    return "./" + path.relative_to(ROOT).as_posix()


def codex_manifest(name: str, plugin: PluginDefinition) -> dict:
    return {
        "name": name,
        "version": plugin.version,
        "description": plugin.description,
        "author": {"name": AUTHOR, "url": AUTHOR_URL},
        "repository": REPOSITORY,
        "license": plugin.license,
        "keywords": list(plugin.keywords),
        "skills": "./skills/",
        "interface": {
            "displayName": plugin.display_name,
            "shortDescription": plugin.short_description,
            "longDescription": plugin.long_description,
            "composerIcon": PLUGIN_ICON,
            "logo": PLUGIN_ICON,
            "logoDark": PLUGIN_ICON,
            "brandColor": plugin.brand_color,
            "developerName": AUTHOR,
            "category": plugin.category,
            "capabilities": list(plugin.capabilities),
            "websiteURL": REPOSITORY,
            "defaultPrompt": list(plugin.default_prompts),
        },
    }


def claude_manifest(name: str, plugin: PluginDefinition) -> dict:
    return {
        "name": name,
        "version": plugin.version,
        "description": plugin.description,
        "author": {"name": AUTHOR},
        "homepage": REPOSITORY,
        "repository": REPOSITORY,
        "license": plugin.license,
        "keywords": list(plugin.keywords),
    }


def codex_marketplace() -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "interface": {"displayName": MARKETPLACE_DISPLAY_NAME},
        "plugins": [
            {
                "name": name,
                "source": {"source": "local", "path": repository_path(CODEX_PLUGINS / name)},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": plugin.category,
            }
            for name, plugin in PLUGINS.items()
        ],
    }


def claude_marketplace() -> dict:
    return {
        "name": MARKETPLACE_NAME,
        "owner": {"name": AUTHOR},
        "description": MARKETPLACE_DESCRIPTION,
        "plugins": [
            {
                "name": name,
                "source": repository_path(CLAUDE_PLUGINS / name),
                "description": plugin.description,
                "version": plugin.version,
                "author": {"name": AUTHOR},
            }
            for name, plugin in PLUGINS.items()
        ],
    }


def build_plugin(destination: Path, name: str, plugin: PluginDefinition, host: str) -> None:
    copy_skills(plugin.skills, destination / "skills", host)
    shutil.copytree(PLUGIN_ASSETS / name, destination / "assets")
    if host == "codex":
        write_json(destination / ".codex-plugin" / "plugin.json", codex_manifest(name, plugin))
    else:
        write_json(destination / ".claude-plugin" / "plugin.json", claude_manifest(name, plugin))


def build_expected(root: Path) -> dict[Path, Path]:
    codex_root = root / "codex"
    claude_root = root / "claude"
    for name, plugin in PLUGINS.items():
        build_plugin(codex_root / name, name, plugin, "codex")
        build_plugin(claude_root / name, name, plugin, "claude")
    write_json(root / "codex-marketplace.json", codex_marketplace())
    write_json(root / "claude-marketplace.json", claude_marketplace())
    return {
        codex_root: CODEX_PLUGINS,
        claude_root: CLAUDE_PLUGINS,
        root / "codex-marketplace.json": CODEX_MARKETPLACE,
        root / "claude-marketplace.json": CLAUDE_MARKETPLACE,
    }


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def files_under(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def compare(expected: Path, actual: Path) -> list[str]:
    if expected.is_file():
        if not actual.is_file():
            return [f"missing: {display(actual)}"]
        if expected.read_bytes() != actual.read_bytes():
            return [f"changed: {display(actual)}"]
        return []
    if not actual.is_dir():
        return [f"missing: {display(actual)}"]
    expected_files = files_under(expected)
    actual_files = files_under(actual)
    problems = [f"missing: {display(actual / path)}" for path in sorted(expected_files - actual_files)]
    problems += [
        f"unexpected: {display(actual / path)}" for path in sorted(actual_files - expected_files)
    ]
    problems += [
        f"changed: {display(actual / path)}"
        for path in sorted(expected_files & actual_files)
        if (expected / path).read_bytes() != (actual / path).read_bytes()
    ]
    return problems


def find_drift() -> list[str]:
    with tempfile.TemporaryDirectory(prefix="agent-skills-build-") as temp:
        expected = build_expected(Path(temp))
        return [
            problem
            for expected_path, actual_path in expected.items()
            for problem in compare(expected_path, actual_path)
        ]


def replace(source: Path, destination: Path) -> None:
    if destination.is_dir():
        shutil.rmtree(destination)
    elif destination.exists():
        destination.unlink()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copyfile(source, destination)


def frontmatter_problems(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return ["missing opening frontmatter marker"]
    closing = text.find("\n---", 4)
    if closing == -1:
        return ["missing closing frontmatter marker"]
    problems = []
    for line in text[4:closing].splitlines():
        key, separator, value = line.partition(":")
        value = value.strip()
        if not separator or not value or value[0] in "'\"":
            continue
        if ": " in value or " #" in value or value.endswith(":") or value.startswith(YAML_RESERVED_STARTS):
            problems.append(f"quote the {key.strip()} value; plain YAML cannot hold it")
    return problems


def validate_configuration() -> None:
    names = {path.name for path in SOURCE.iterdir() if path.is_dir()}
    if names != set(SKILLS):
        raise SystemExit(f"Canonical skill set mismatch: {sorted(names)}")

    memberships = [name for plugin in PLUGINS.values() for name in plugin.skills]
    if len(memberships) != len(set(memberships)) or set(memberships) != set(SKILLS):
        raise SystemExit("Every canonical skill must belong to exactly one plugin.")

    artwork = {path.name for path in PLUGIN_ASSETS.iterdir() if path.is_dir()}
    if artwork != set(PLUGINS):
        raise SystemExit(f"Plugin artwork mismatch: {sorted(artwork)}")
    for plugin_name in PLUGINS:
        if not (PLUGIN_ASSETS / plugin_name / "plugin-icon.png").is_file():
            raise SystemExit(f"Missing canonical plugin icon: {plugin_name}")

    for name in SKILLS:
        if not (SOURCE / name / "assets" / "icon.png").is_file():
            raise SystemExit(f"Missing canonical skill icon: {name}")

    for path in SOURCE.rglob("*.md"):
        if CLAUDE_ONLY_FRONTMATTER in path.read_text(encoding="utf-8"):
            raise SystemExit(f"Claude-only frontmatter leaked into canonical source: {path}")

    for path in [*SOURCE.glob("*/SKILL.md"), *SOURCE.glob("*/variants/*.md")]:
        for problem in frontmatter_problems(path.read_text(encoding="utf-8")):
            raise SystemExit(f"Invalid frontmatter in {path}: {problem}")

    variant_names = {
        path.parent.name for path in SOURCE.glob("*/variants") if path.is_dir()
    }
    if variant_names != set(HOST_VARIANTS):
        raise SystemExit(
            f"Host variant skill mismatch: expected {sorted(HOST_VARIANTS)}, "
            f"found {sorted(variant_names)}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build Codex and Claude Code adapters and marketplaces from skills/ and the catalog."
    )
    parser.add_argument("--check", action="store_true", help="Verify generated files without writing.")
    args = parser.parse_args()
    validate_configuration()

    if args.check:
        problems = find_drift()
        if problems:
            print("Adapter drift detected:")
            for problem in problems:
                print(f"- {problem}")
            return 1
        print("Codex and Claude Code adapters and marketplaces match the catalog and canonical skills.")
        return 0

    with tempfile.TemporaryDirectory(prefix="agent-skills-build-") as temp:
        for expected_path, actual_path in build_expected(Path(temp)).items():
            replace(expected_path, actual_path)

    print("Built Codex and Claude Code adapters and marketplaces from the catalog and canonical skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
