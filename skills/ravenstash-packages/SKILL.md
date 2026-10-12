---
name: ravenstash-packages
description: Use Ravenstash private PyPI, npm, and Maven repositories and read-only private mirrors through rvs and native package tools. Use for repository or mirror discovery and creation, dependency installation, package publishing, version lifecycle operations, package tags (npm dist-tags), upstream inspection, and CI package access; do not use for Container or Helm OCI workflows.
license: MIT
metadata:
  author: Ravenstash
  version: "0.7.0"
  ravenstash-rvs-compatibility: "0.15.x"
---

# Ravenstash Packages

Use the package-release lanes of Ravenstash Artifacts without collapsing private repositories, private mirrors, acting accounts, or formats into one implicit destination.

## Preflight

Repository management lives under `rvs art repo`. The product also supports Container images and Helm charts in one OCI repository format; those operations use the separate OCI workflow.

1. Run `rvs --version` and use `rvs <group> --help` for exact syntax.
2. Inspect authentication with `rvs auth status` and, when identity matters, `rvs auth whoami`.
3. Resolve the acting account and target with `rvs art status`, an explicit `--account`, a one-shot `--target`, or wrapper `--rvs-account` and `--rvs-target`.
4. Prefer the one-shot forms when the user did not request a saved selection change. `rvs art status` only reads.
5. Resolve the format. Never publish to a mirror or use a package-release workflow against OCI content.

## Route the workflow

- For repository, package lifecycle, upstream, or mirror work, read [references/repositories-and-caches.md](references/repositories-and-caches.md).
- For Python installs or publishing, read [references/pypi.md](references/pypi.md).
- For npm installs, publishing, or package tags (npm distribution tags such as `latest` or `beta`), read [references/npm.md](references/npm.md).
- For Maven installs or deployments, read [references/maven.md](references/maven.md).
- For unattended jobs, read [references/automation.md](references/automation.md) in addition to the ecosystem reference.

Load only the references needed by the request.

## Native-wrapper boundary

Prefer the appropriate wrapper when the native client needs temporary Ravenstash authentication:

```bash
rvs pip --rvs-target platform/packages install internal-sdk
rvs uv --rvs-target platform/packages sync
rvs twine --rvs-target platform/releases upload dist/*
rvs npm --rvs-target platform/packages ci
rvs mvn --rvs-target platform/packages verify
```

Arguments after the Ravenstash wrapper options belong to the native tool. Do not assume their output follows `rvs --json`.

The wrappers must not cause a skill or agent to copy tokens into `.npmrc`, `pip.conf`, `.pypirc`, `settings.xml`, `pyproject.toml`, or `uv.toml`.

## Mutation boundary

- Listing, showing, resolving URLs, and checking current context are read-only.
- Creating repositories or mirrors, selecting saved context, configuring persistent native clients, publishing, yanking, deprecating, and deleting versions or OCI content mutate local or remote state. Deleted versions go to the repository trash and are restored only in the web app.
- Renaming or deleting a repository, changing its upstreams, changing a private mirror's age policy, deleting a mirror, and deleting a whole package are web-app-only. Route them to the Ravenstash web app; do not invent an `rvs` command or call the API directly.
- Before a mutation, report the exact acting account, namespace/repository or mirror, format, package/version when applicable, and intended change.
- Package tags exist only for npm and, unlike OCI tags, move. Setting, moving, or deleting one changes what installs resolve: listing tags never authorizes it, and it needs the exact package, tag, and version as well. A repository changes only its own tags; a tag that comes from an upstream is changed in its source. Report such a refusal instead of retrying or trying another route.
- Do not pass `--yes` to deletion commands merely to suppress the CLI's confirmation. Use it only when the user explicitly authorized that exact deletion and the target has been independently resolved.

## Completion

Verify the result with the narrowest read operation available. Report target identity and changed state without reproducing secret-bearing environment or verbose native-client logs.
