# Ravenstash product model

Load this reference only when the request depends on Ravenstash terminology, target selection, registry support, or availability.

## Ownership and content

- A user is one person with a Ravenstash login.
- A local profile is named CLI configuration and credential association; it is not the authenticated user.
- An acting account is the personal account or organization authorizing the operation and receiving its usage attribution.
- A namespace is an account-owned cross-product naming and organization-member permission boundary.
- A repository is a private logical content namespace that can enable one or more formats.
- A repository lane is one format inside a repository: PyPI, npm, Maven, or OCI. Container images and Helm charts share the OCI lane and are classified by their manifests.
- A private mirror is an account-scoped, read-only PyPI, npm, or Maven access surface backed by an official or custom remote cache. It is not a private repository and cannot accept publishing.
- Every personal account has a private mirror of each Ravenstash-provided source, created by Ravenstash. A mirror the user deleted is not recreated automatically.

## Target forms

| Form | Meaning | Capabilities |
| --- | --- | --- |
| `namespace/repository` | Private repository | Read and publish for enabled lanes |
| `in/ar_...` | ID-based private-repository target | Same repository across name changes |
| `mirror:source` | Ravenstash-curated official private mirror | Read only |
| `custom-mirror:name` | Account-defined custom private mirror | Read only |

An explicit target is one-shot and must not change saved selection. A saved selection remains scoped to its local profile and immutable acting-account identity, and holds one target per format: pypi, npm, maven, and oci. Selecting a target changes only the formats it has, or the formats named with `--format`; the other formats keep their selection.

When nothing is selected for pypi, npm, or maven, reads by a personal account signed in interactively use that account's default mirror of the format, and `rvs` names it on standard error. That default never applies to publishing or deletion, organization accounts, `RVS_TOKEN` automation, OCI content, or address, setup, and token commands. It is a convenience for interactive reads, not a substitute for a target the user named.

## Registry boundaries

- PyPI, npm, and Maven support private repositories and private mirrors.
- Container images and Helm charts share one private-only OCI format and the `oci.rvsta.sh` host. There is no container mirror, so OCI work always needs a private repository with the oci format.
- ORAS uses the selected OCI repository without a separate Ravenstash format flag; content type comes from the manifest.
- A mirror's backing remote cache can be connected behind a compatible private repository in the web app; `rvs art repo upstream list` shows the result. The attachment copies its age setting when created and is then managed independently from the mirror default.

## Availability floor for these skills

These sources target the `rvs` 0.17.x line and were verified against `v0.17.0`. `rvs art repo` manages repositories for packages, container images, and Helm charts. Top-level `rvs repo`, `rvs artifacts`, and `rvs ci` are absent. Repository rename and deletion, upstream changes, mirror age changes and deletion, and whole-package deletion are web-app-only. Check current public documentation before making broader product-availability claims.
