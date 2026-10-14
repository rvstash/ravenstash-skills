---
name: ravenstash
description: Route Ravenstash product requests to the correct supported surface and apply Ravenstash product vocabulary, availability boundaries, and safe operating rules. Use when a user asks about Ravenstash, Ravenstash Artifacts, repositories, private mirrors, rvs, PyPI, npm, Maven, Container, Helm, or which Ravenstash workflow to use.
license: MIT
metadata:
  author: Ravenstash
  version: "0.8.0"
  ravenstash-rvs-compatibility: "0.15.x"
---

# Ravenstash

Use this skill to orient the request, then use the most specific Ravenstash workflow available. Do not use it as a substitute for current public documentation or installed CLI help.

## Choose the surface

- Use `ravenstash-cli` for installation, updates, authentication, local profiles, acting-account selection, artifact-target context, local runtimes, or CLI troubleshooting.
- Use `ravenstash-packages` for private PyPI, npm, or Maven repositories, private mirrors, package publishing, installs, package lifecycle operations, and package automation.
- Use `ravenstash-oci` for container images or Helm charts in OCI-enabled repositories and for Docker, Helm, or ORAS workflows.
- Use the Ravenstash web application for account security settings, organization membership, passkeys, automation-token creation, custom-mirror creation, and workflows not exposed by `rvs`: renaming or deleting a repository, changing its upstreams, changing a private mirror's age policy, deleting a mirror, and deleting a whole package.

Read [references/product-model.md](references/product-model.md) when the request depends on repository formats, target types, terminology, or current product availability.

## Source priority

1. Treat installed `rvs` help as authoritative for the commands that binary supports: run `rvs --version` and `rvs <group> --help` before inventing a command or option.
2. Use <https://docs.ravenstash.com/> for current product procedures and availability. The machine-readable entrypoint is
   <https://docs.ravenstash.com/llms.txt>.
3. Use <https://ravenstash.com/llms-full.txt> for current high-level product facts and boundaries.
4. If these sources disagree, report the version or documentation mismatch and do not guess.

## Operating boundaries

- Use `rvs` or the documented browser workflow for Ravenstash operations. Do not construct direct Ravenstash API calls.
- A skill provides procedure, not authorization. Preserve the user's requested scope and stop before an unrequested create, update, publish, yank, delete, target switch, or persistent configuration change.
- Never request, print, copy, or persist a Ravenstash access token. Interactive login uses the browser-backed device flow; automation receives `RVS_TOKEN` from the user's secret store.
- Resolve the local profile, acting account, target, repository format, and OCI content type when relevant before any operation that could affect remote state. Never substitute a same-named object from another account or namespace.
- Do not imply that a roadmap product or placeholder CLI group is usable. The coordinated command surface uses `rvs art repo`; top-level `rvs repo`, `rvs artifacts`, and `rvs ci` are absent.
- Do not invent billing, quota, retention, anonymous access, or package-security behavior. Refer volatile policy questions to current public documentation.

## Completion

Report the surface used, the resolved account and target when relevant, the observable result, and any state intentionally changed. Do not expose tokens or secret-bearing output.
