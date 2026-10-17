# Ravenstash Agent Skills

Official Agent Skills for Ravenstash products and the `rvs` developer CLI. This repository contains the portable workflows and their behavioral evals.

The 0.9 skill source targets the `rvs` 0.16.x compatibility channel declared in each skill's `ravenstash-rvs-compatibility` metadata. Installed CLI help remains the execution authority.

The skills follow the [Agent Skills specification](https://agentskills.io/) and are designed for Codex, GitHub Copilot, Claude Code, Cursor, and other compatible agents. They teach product-specific decisions and safety boundaries; current facts and complete command references remain in the [Ravenstash documentation](https://docs.ravenstash.com/).

## Skills

| Skill | Purpose |
| --- | --- |
| `ravenstash` | Product vocabulary, availability boundaries, source priority, and workflow routing |
| `ravenstash-cli` | Installation, updates, local profiles, acting accounts, targets, structured output, runtimes, and troubleshooting |
| `ravenstash-packages` | PyPI, npm, and Maven repositories, private mirrors, lifecycle operations, publishing, installs, and automation |
| `ravenstash-oci` | Container images and Helm charts in one OCI repository format through Docker, Helm, ORAS, and `rvs` wrappers |

Install all four. Each workflow skill is self-contained, while `ravenstash` provides the common router for broad requests.

## Install

Using the cross-agent skills installer:

```bash
npx skills add rvstash/ravenstash-skills --all
```

If the installed GitHub CLI release includes `gh skill`, install each skill for the intended agent and scope:

```bash
gh skill install rvstash/ravenstash-skills ravenstash --agent codex --scope user
gh skill install rvstash/ravenstash-skills ravenstash-cli --agent codex --scope user
gh skill install rvstash/ravenstash-skills ravenstash-packages --agent codex --scope user
gh skill install rvstash/ravenstash-skills ravenstash-oci --agent codex --scope user
```

Change `--agent codex` or `--scope user` for another supported client or a project-local installation. Preview a skill before installing it:

```bash
gh skill preview rvstash/ravenstash-skills ravenstash-packages
```

## Trust model

- Skills use the installed `rvs` CLI and its live help as the operational contract. They do not construct direct Ravenstash API calls.
- Skills never contain credentials. Interactive authentication remains in the browser-backed device flow; automation injects `RVS_TOKEN` from a secret manager.
- A skill does not grant permission for a remote or destructive change. Exact account, target, repository format or OCI content type, and affected object must still be resolved.
- Public documentation remains authoritative for volatile product policy and availability.

## Validate

```bash
python3 scripts/validate.py
git diff --check
```

The validator checks Agent Skills metadata, local reference links, Codex UI metadata, unfinished scaffolding, and the behavioral eval catalog.

## License

MIT
