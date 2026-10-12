# ORAS workflows

Load when the user explicitly wants ORAS or an OCI-native discover, manifest, tag, pull, or push operation.

ORAS uses the selected repository’s OCI format:

```bash
rvs oras \
  --rvs-target platform/runtime-images \
  discover oci.rvsta.sh/platform/runtime-images/api:latest
```

Do not pass `--rvs-format`. Content type comes from the manifest, not the host or a credential permission. Use `rvs art oci` for path, tag, digest, manifest, and referrer management.

For a push, inspect the local artifact set and annotations, resolve the stable reference with `rvs art reference`, and confirm the exact remote reference before executing. Do not use ORAS to work around a missing repository lane or to target a private mirror.

## Deletion

Deleting a manifest, with `rvs art oci manifest delete PATH@sha256:DIGEST` or `rvs oras manifest delete`, moves it and its referrers to the repository trash. Its tags stop resolving, it can be restored in the web app until it is permanently deleted, and the same digest cannot be pushed to that path until then. A manifest that an image index in the path references is refused; the index must be deleted instead. `rvs art oci tag delete PATH:TAG` removes only the tag, at once. Confirm the exact path and digest or tag before deleting, and do not add `--yes` or ORAS `--force` unless that deletion is authorized.
