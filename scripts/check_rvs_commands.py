#!/usr/bin/env python3
"""Check documented rvs commands and options against the installed rvs."""

import os
import re
import shlex
import subprocess
import sys
from functools import cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# rvs passes everything except its own --rvs-* options to these native tools.
NATIVE_TOOLS = {"docker", "helm", "mvn", "npm", "oras", "pip", "pnpm", "python", "twine", "uv"}
SHELL_FENCES = {"", "bash", "console", "sh", "shell", "yaml", "yml"}
TEXT_SUFFIXES = {".md", ".yml", ".yaml"}
FENCE = re.compile(r"^\s*(```|~~~)\s*([\w-]*)")
CI_KEYS = re.compile(r"^\s*-?\s*(run|script|before_script|after_script):", re.MULTILINE)
YAML_NAME = re.compile(r"^\s*-?\s*name:")
INVOCATION = re.compile(r"(?:^|[\s(|;&`])rvs\s+([^|;&`)#\n]+)")
HELP_ENVIRONMENT = {**os.environ, "COLUMNS": "200", "NO_COLOR": "1", "TERM": "dumb"}


def command_lines(path: Path) -> list[tuple[int, str]]:
    """Return shell and YAML lines, joining backslash continuations."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    selected: list[tuple[int, str]] = []
    if path.suffix != ".md" and not CI_KEYS.search(text):
        # Only CI definitions run commands; other YAML is metadata or prose.
        return []
    if path.suffix == ".md":
        language = None
        for number, line in enumerate(lines, 1):
            fence = FENCE.match(line)
            if fence:
                language = None if language is not None else fence.group(2).lower()
                continue
            if language in SHELL_FENCES:
                selected.append((number, line))
    else:
        selected = [
            (number, line) for number, line in enumerate(lines, 1) if not YAML_NAME.match(line)
        ]

    joined: list[tuple[int, str]] = []
    pending = ""
    start = 0
    for number, line in selected:
        if not pending:
            start = number
        stripped = line.rstrip()
        if stripped.endswith("\\"):
            pending += stripped[:-1] + " "
            continue
        joined.append((start, pending + line))
        pending = ""
    if pending:
        joined.append((start, pending))
    return [(number, line) for number, line in joined if not line.lstrip().startswith("#")]


@cache
def help_text(arguments: tuple[str, ...]) -> str | None:
    result = subprocess.run(
        ["rvs", *arguments, "--help"],
        capture_output=True,
        env=HELP_ENVIRONMENT,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def check_invocation(arguments: list[str]) -> list[str]:
    global_options = []
    while arguments and arguments[0].startswith("-"):
        global_options.append(arguments.pop(0))
    errors = [
        f"`rvs` has no {option} global option"
        for option in global_options
        if not re.search(rf"(?<![\w-]){re.escape(option)}(?![\w-])", help_text(()) or "")
    ]
    if not arguments:
        return errors
    command = arguments[0]
    if command in NATIVE_TOOLS:
        options = [argument for argument in arguments if argument.startswith("--rvs-")]
        help_path = (command,)
    else:
        positional = []
        for argument in arguments:
            if argument.startswith("-"):
                break
            positional.append(argument)
        options = [argument for argument in arguments if argument.startswith("--")]
        help_path = tuple(positional)

    command_help = help_text(help_path)
    if command_help is None:
        return [f"`rvs {' '.join(help_path)}` is not an rvs command"]
    known = command_help + (help_text(()) or "")
    for option in options:
        name = option.split("=", 1)[0]
        if not re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", known):
            errors.append(f"`rvs {' '.join(help_path)}` has no {name} option")
    return errors


def main() -> int:
    if help_text(()) is None:
        print("rvs is not installed or does not run", file=sys.stderr)
        return 2
    errors: list[str] = []
    checked = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix not in TEXT_SUFFIXES:
            continue
        for number, line in command_lines(path):
            for match in INVOCATION.finditer(line):
                try:
                    arguments = shlex.split(match.group(1))
                except ValueError:
                    arguments = match.group(1).split()
                if not arguments:
                    continue
                checked += 1
                for error in check_invocation(arguments):
                    errors.append(f"{path.relative_to(ROOT)}:{number}: {error}")
    if errors:
        print("\n".join(errors))
        return 1
    version = subprocess.run(["rvs", "--version"], capture_output=True, text=True, check=False)
    print(f"Checked {checked} rvs invocations against {version.stdout.strip()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
