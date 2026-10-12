# AGENTS.md

This file is the complete operating guide for automated contributors to the Ravenstash Agent Skills repository; it relies on nothing outside this repository.

## Agent workflow

- Reviews and investigations are read-only. For implementation, complete the authorized local change and run the smallest relevant verification.
- Do not commit, push, release, or publish unless the user explicitly requests it. Report changed files and verification results.

## Repository role

- This is the canonical source for portable `SKILL.md` workflows that teach AI agents how to use released Ravenstash products and the `rvs` CLI.
- It is not the public product documentation, a copy of the CLI command reference, an MCP server, or an authorization layer.
- Skills live under `skills/<name>/SKILL.md`. Conditional detail belongs in that skill's `references/` directory.

## Sources of truth

Before changing product or command claims, verify them against:

1. The released `rvs` binary and its `--help` output.
2. <https://docs.ravenstash.com/> and its `llms.txt` entrypoint.
3. The public [Ravenstash CLI repository](https://github.com/rvstash/ravenstash-cli) and its release notes.

Do not copy private architecture, internal service routes, environment hosts, customer data, or unreleased credentials into this repository. Examples use public hosts, documentation-safe names, and obvious placeholders.

## Skill authoring

- Follow the Agent Skills specification: lowercase hyphenated directory/name, concise discriminating description, and progressive disclosure.
- Keep each workflow skill self-contained. It may recommend another installed skill, but it must not fail merely because a sibling directory was not installed.
- Encode Ravenstash-specific decisions, safety invariants, failure boundaries, and success checks. Link to public docs instead of copying an exhaustive manual.
- Preserve user scope. A skill never turns a read request into a create, publish, switch, configure, yank, or delete operation.
- Require the exact local profile, acting account, target, repository format or OCI content type, and object identity where ambiguity could affect another resource.
- Never include token values or instructions to persist credentials.
- Verify the supported CLI compatibility channel and command surface from the skill metadata, pinned released binary, and its `--help` output. Do not encode a release-specific command inventory in this instruction file or invent commands and products that the supported release does not expose.
- Do not add skills for roadmap products until a released customer workflow gives the skill something concrete to operate or interpret.

## Versioning

- Skill releases use independent semantic versioning.
- Keep `metadata.version` consistent across all files changed for one release.
- State the supported `rvs` compatibility channel in operational skill frontmatter.
- A CLI command-surface change requires coordinated skill review before the affected release is considered supported.

## Verification

Run from this repository:

```bash
python3 scripts/validate.py
git diff --check
```

Also exercise changed command examples against the pinned compatible `rvs` binary. Model evals must judge behavior and side effects, not merely wording.
