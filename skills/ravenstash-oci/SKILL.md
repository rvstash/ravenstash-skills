---
name: ravenstash-oci
description: Use Ravenstash private OCI repositories for container images and Helm charts through rvs, Docker, Helm, and ORAS with exact target selection and ephemeral credentials. Use for OCI references, image push or pull, Helm chart publish or install, and ORAS discovery; do not use for PyPI, npm, Maven, or private-mirror workflows.
license: MIT
metadata:
  author: Ravenstash
  version: "0.8.0"
  ravenstash-rvs-compatibility: "0.15.x"
---

# Ravenstash OCI

Container images and Helm charts share the `oci` format and `oci.rvsta.sh` host. Content type is determined from the manifest. A path has one primary content type; use separate paths such as `images/api` and `charts/api` when needed.

## Preflight

1. Run `rvs --version` and discover current syntax with `rvs <group> --help`.
2. Check `rvs auth status` and use `rvs auth whoami` when identity matters.
3. Resolve the acting account and exact `namespace/repository` target.
4. Confirm that the repository enables `oci`. Use `rvs art oci list` to inspect paths; `--content-type container_image|helm_chart` filters their classification.
5. Confirm that the requested native tool is installed.

Read [references/container.md](references/container.md) for Docker image work, [references/helm.md](references/helm.md) for Helm charts, or [references/oras.md](references/oras.md) for ORAS. Load only the relevant file.

## Stable reference construction

Docker push/pull/tag can use short image paths with the selected repository. Helm push can omit its destination, and chart read/render/release commands accept short paths; see the Helm reference for local-path and alias collisions. For commands requiring a full reference, use `rvs art reference` rather than inventing namespace or repository refs:

```bash
rvs art reference \
  --format oci \
  --target platform/runtime-images \
  api:latest
```

Use the returned reference unchanged. Never reconstruct stable identifiers from display names.

## Credential boundary

`rvs art native config docker|helm|oras` prints setup instructions without minting, writing, or running tools. ORAS instructions for both content types use one token and one host login. Default native credential stores can be shared, so logout may affect another client; the printed recipes use isolated temporary files.

- Use the `rvs docker`, `rvs helm`, or `rvs oras` wrapper for temporary scoped authentication.
- Do not extract a token for `docker login`, put it in argv, or write it to the user's Docker or Helm configuration.
- The wrapper uses a temporary native configuration while preserving unrelated registry credentials. Do not replace the user's complete native config.
- Inspect verbose native logs before sharing them.

## Target boundary

- OCI targets are exact private repositories. `mirror:` and `custom-mirror:` targets are invalid.
- A one-shot `--rvs-target` must not change saved selection.
- Pull, inspect, show, and discover operations are normally reads. Push and publish operations create remote state and require the exact destination to be confirmed.
- Deleting a manifest moves it to the repository trash, where only the web app restores it; deleting a tag is immediate. See the ORAS reference.
- An OCI tag names one manifest and is never moved to another. npm distribution tags are movable package tags and belong to the package workflow, not here.
- Do not invent a tag, chart version, digest, or OCI path that the user did not supply or that cannot be read from the project.

## Completion

Report OCI content type, target, stable OCI reference, native tool, and observable result. For a push or publish, include the resulting tag or digest when the native tool reports it, without exposing credentials.
