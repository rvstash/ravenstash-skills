# Repositories and private mirrors

Load for repository discovery or creation, package lifecycle work, private-mirror discovery or creation, or questions about upstream attachment.

## Private repositories

Inspect before changing:

```bash
rvs art repo list
rvs art repo list --format pypi
rvs art repo show platform/packages
rvs art repo upstream list platform/packages pypi
```

Creation requires an explicit name and one or more formats:

```bash
rvs art repo create platform/packages --format pypi,npm
rvs art repo create platform/packages --format pypi --format npm
```

A bare name creates the repository in the acting account's default namespace. A logical repository can contain several formats. Confirm all intended formats rather than creating another same-named repository to compensate for a missing lane.

## Web-app-only operations

`rvs` does not rename or delete repositories, add, change, or remove upstreams, change a private mirror's package-age policy, delete a private mirror, or delete a whole package. Restoring deleted content from the repository trash is also web-app-only. Route these requests to the Ravenstash web app after resolving the exact account and repository or mirror; do not invent an `rvs` command or a direct API call. Do not state a trash retention period or other recovery guarantees; point to current public documentation.

## Private mirrors

Private mirrors are read-only and support only PyPI, npm, and Maven. Each is backed by an official or customer-defined remote cache, and their targets remain distinct:

```bash
rvs art mirror list
rvs art mirror show rc_...
rvs art mirror create pypiorg --select
rvs art mirror select pypiorg
rvs art mirror select --custom company-python
```

Use a mirror once without changing the saved target:

```bash
rvs pip --rvs-target mirror:pypiorg install requests
rvs pip --rvs-target custom-mirror:company-python install internal-sdk
```

Create custom mirrors in the web app. The CLI can list, show, and select existing custom mirrors; it cannot create, change, or delete them.

## Upstream attachment

A repository can use a mirror's backing remote cache as an upstream. Inspect the configured sources with `rvs art repo upstream list`; attach, reorder, or detach them in the web app. The repository's own packages are checked first, and configured upstream positions are `1` through `4`. An attachment copies the cache's age setting at creation and is then managed independently. A later mirror age change must not be described as automatically changing existing attachments.

An upstream supplies packages for installs; it does not hand over their management. A repository changes only its own package tags: the tags of a package or version that an upstream supplies are read-only in the consuming repository and are changed in their source. See [npm.md](npm.md).

## Package lifecycle

Package commands act on the private repository chosen with `rvs art select` unless `--target` is passed; a selected mirror is rejected. `--format` is required only when that repository has more than one of PyPI, npm, and Maven; passing it for a single-format repository is harmless and keeps the intended format explicit:

```bash
rvs art package list --target platform/packages --format pypi
rvs art package show requests --target platform/packages --format pypi
rvs art package show requests --target platform/packages --format pypi --version 2.32.3
rvs art package yank requests 2.32.3 --target platform/packages --reason "broken wheel"
rvs art package deprecate left-pad 1.0.0 --target platform/packages --message "Use 1.0.1"
rvs art package delete-version requests 2.32.3 --target platform/packages --format pypi
```

`package show` prints the summary and the newest 50 versions; use `--limit N` (1-100), `--all-versions`, or `--version VERSION` for one version with its files and digests. With root `--json` it prints one document with `package`, `versions`, and `versions_next_cursor`.

Yank and unyank always apply to PyPI; deprecate and undeprecate always apply to npm. These commands take no `--format`. Maven has no corresponding lifecycle operation.

Package tags (npm distribution tags) are read and changed with `rvs art package tag list|set|delete`, and `package show` prints them. Only npm packages have tags. Load [npm.md](npm.md) before reading or changing one.

Yank, deprecate, and delete-version change remote package state. Confirm exact package, version, repository, format, and account before invoking them. Do not add `--yes` unless the exact deletion is already authorized.

`delete-version` moves the version to the repository trash: it stops being installable, disappears from listings, and can be restored in the web app until it is permanently deleted at the end of the trash retention period. Until then the same version cannot be published again; other versions can. A publish of trashed content fails with a message saying it is in the trash until its permanent-deletion date. Report that outcome instead of retrying, choosing a new version, or restoring on the user's behalf. Deleting needs delete authority, which publish authority does not include.
