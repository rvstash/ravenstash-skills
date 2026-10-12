# Container workflows

Load for Docker image operations against a private Ravenstash repository with OCI enabled.

## Short image names

Select the exact repository and use the image path supplied by the user:

```bash
rvs art select platform/runtime-images
rvs docker pull team/api:1.2
```

Use `--rvs-target platform/runtime-images` instead when the task should not change saved selection. Pull retains the full reference printed by the CLI; it does not create a local `team/api:1.2` alias. Never assume a later local run uses that image unless it names the full reference. An internal miss never falls back publicly.

A push creates remote state. Verify the local source, destination path/tag, acting account, and OCI target before publishing. Shorthand push creates its qualified local tag automatically. A conflicting destination tag is rejected; do not replace it merely to make a retry succeed without authorization for that replacement. Tag shorthand expands only the destination and keeps its source local. `push --all-tags` requires a full reference.

## Full references and builds

Resolve a reference for Dockerfiles, Buildx output tags, ORAS, or a CLI version without Docker shorthand:

```bash
rvs art reference \
  --format oci \
  --target platform/runtime-images \
  team/api:1.2
```

Use the returned reference; do not invent stable identifiers or registry hosts. Dockerfile references are never rewritten. A wrapped build may combine public images and private images from the one selected Ravenstash repository. Credentials for that repository are exchanged per invocation; selection alone does not mint credentials. Multi-repository private build authorization is not supported.

Nested paths are valid, but Docker interprets hostname-like first components (e.g. `team.v2/api`) as explicit registries. Use the full internal reference for such paths. Keep Docker context/config options before the Docker subcommand.

Remote caches are not supported for OCI repositories.
