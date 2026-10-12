#!/usr/bin/env python3
"""Validate Ravenstash Agent Skill packages with no third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
WEB_APP_ONLY = "the operation is managed in the Ravenstash web app"
REMOVED_COMMANDS = {
    "rvs account use": "use `rvs account switch` with supported rvs releases",
    "rvs art repo set-default": "use `rvs art select` or a one-shot `--target`",
    "rvs art repo rename": WEB_APP_ONLY,
    "rvs art repo delete": WEB_APP_ONLY,
    "rvs art repo upstream add": WEB_APP_ONLY,
    "rvs art repo upstream update": WEB_APP_ONLY,
    "rvs art repo upstream remove": WEB_APP_ONLY,
    "rvs art mirror set-age": WEB_APP_ONLY,
    "rvs art mirror delete": WEB_APP_ONLY,
    "rvs art package delete": WEB_APP_ONLY,
}


def scalar(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", frontmatter)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value


def frontmatter(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("must begin with YAML frontmatter")
    closing = content.find("\n---\n", 4)
    if closing == -1:
        raise ValueError("frontmatter is not closed")
    return content[4:closing]


def validate_links(path: Path, errors: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK_RE.findall(content):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = target.split("#", 1)[0]
        if clean_target and not (path.parent / clean_target).resolve().exists():
            errors.append(f"{path.relative_to(ROOT)}: missing link target {target}")


def validate_released_commands(path: Path, errors: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    for command, guidance in REMOVED_COMMANDS.items():
        # A hyphenated continuation is a different command (`delete-version`).
        if re.search(rf"{re.escape(command)}(?![\w-])", content):
            errors.append(f"{path.relative_to(ROOT)}: removed command `{command}`; {guidance}")


def validate_openai_yaml(skill_dir: Path, name: str, errors: list[str]) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8")
    prompt = re.search(r'(?m)^\s+default_prompt:\s*"([^"]+)"\s*$', content)
    if not prompt or f"${name}" not in prompt.group(1):
        errors.append(f"{path.relative_to(ROOT)}: default_prompt must mention ${name}")
    short = re.search(r'(?m)^\s+short_description:\s*"([^"]+)"\s*$', content)
    if not short or not 25 <= len(short.group(1)) <= 64:
        errors.append(
            f"{path.relative_to(ROOT)}: short_description must be 25-64 characters"
        )


def validate_skills(errors: list[str]) -> set[str]:
    names: set[str] = set()
    versions: dict[str, str] = {}
    compatibilities: dict[str, str] = {}
    for skill_dir in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        path = skill_dir / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
            continue
        content = path.read_text(encoding="utf-8")
        if "[TODO" in content:
            errors.append(f"{path.relative_to(ROOT)}: unfinished scaffold marker")
        try:
            metadata = frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        name = scalar(metadata, "name")
        description = scalar(metadata, "description")
        license_name = scalar(metadata, "license")
        version = scalar(metadata, "version")
        compatibility = scalar(metadata, "ravenstash-rvs-compatibility")
        if not name or not NAME_RE.fullmatch(name) or not 1 <= len(name) <= 64:
            errors.append(f"{path.relative_to(ROOT)}: invalid name")
            continue
        if name != skill_dir.name:
            errors.append(f"{path.relative_to(ROOT)}: name must match parent directory")
        if name in names:
            errors.append(f"{path.relative_to(ROOT)}: duplicate skill name {name}")
        names.add(name)
        if not description or not 1 <= len(description) <= 1024:
            errors.append(f"{path.relative_to(ROOT)}: invalid description length")
        if license_name != "MIT":
            errors.append(f"{path.relative_to(ROOT)}: license must be MIT")
        if not version or not SEMVER_RE.fullmatch(version):
            errors.append(f"{path.relative_to(ROOT)}: metadata.version must be semantic")
        else:
            versions[name] = version
        if not compatibility:
            errors.append(
                f"{path.relative_to(ROOT)}: missing ravenstash-rvs-compatibility"
            )
        else:
            compatibilities[name] = compatibility
        validate_links(path, errors)
        validate_released_commands(path, errors)
        validate_openai_yaml(skill_dir, name, errors)
        for reference in sorted((skill_dir / "references").glob("*.md")):
            validate_links(reference, errors)
            validate_released_commands(reference, errors)
    if len(set(versions.values())) > 1:
        errors.append(f"skills: inconsistent metadata.version values: {versions}")
    if len(set(compatibilities.values())) > 1:
        errors.append(
            "skills: inconsistent ravenstash-rvs-compatibility values: "
            f"{compatibilities}"
        )
    return names


def validate_evals(skill_names: set[str], errors: list[str]) -> None:
    path = ROOT / "evals" / "cases.json"
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"evals/cases.json: {exc}")
        return
    if not isinstance(cases, list) or not cases:
        errors.append("evals/cases.json: expected a non-empty array")
        return
    ids: set[str] = set()
    for index, case in enumerate(cases):
        label = f"evals/cases.json[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: expected object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not NAME_RE.fullmatch(case_id):
            errors.append(f"{label}: invalid id")
        elif case_id in ids:
            errors.append(f"{label}: duplicate id {case_id}")
        else:
            ids.add(case_id)
        if case.get("expected_skill") not in skill_names:
            errors.append(f"{label}: unknown expected_skill")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label}: prompt is required")
        for field in ("expected_behaviors", "prohibited_behaviors"):
            value = case.get(field)
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                errors.append(f"{label}: {field} must be a non-empty string array")


def main() -> int:
    errors: list[str] = []
    skill_names = validate_skills(errors)
    validate_evals(skill_names, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(skill_names)} skills and the behavioral eval catalog.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
