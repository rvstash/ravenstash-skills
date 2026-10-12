# npm workflows

Load for npm, Node.js, JavaScript, TypeScript, scoped-package, install, or publish work.

## Install

```bash
rvs npm --rvs-target platform/packages install @acme/design-system
rvs npm --rvs-target platform/packages ci
rvs npm --rvs-target mirror:npmjs install lodash
```

Private mirrors support reads only. Keep Ravenstash wrapper options before the native npm arguments. A one-shot target must not change saved selection.

## Publish

Publishing requires a private npm repository:

```bash
rvs npm --rvs-target platform/releases publish
```

The wrapper invokes native `npm publish`, including its packlist and lifecycle hooks. Treat those hooks as project code that may execute locally; inspect the package and obtain any execution approval required by the environment before publishing.

## Unpublish

```bash
rvs npm --rvs-target platform/packages unpublish @acme/widgets@1.2.3
```

`npm unpublish PACKAGE@VERSION` moves that version to the repository trash; the wrapper requests the delete authority it needs. npm sends a whole-package unpublish both for `npm unpublish PACKAGE --force` and for a package's last version; it succeeds only while exactly one version is left, which it trashes. With more versions it fails with `E405`: use `rvs art package delete-version` for a single version and route whole-package deletion to the web app. Unpublishing is a deletion: confirm the exact package, version, and repository first, and pass `--force` only when that whole-package unpublish is authorized.

## Package tags

Package tags are npm's distribution tags: movable names such as `latest`, `next`, or `beta` that each point at one version. `npm install PACKAGE` installs the version `latest` points at, and `npm install PACKAGE@beta` the one `beta` points at. Only npm packages have tags; the tag commands refuse PyPI and Maven, so do not emulate tags there. They are not OCI tags, which name one manifest and never move.

If the installed release lacks `rvs art package tag`, report the version instead of substituting another command.

### Read tags

```bash
rvs art package tag list @acme/widgets --target platform/packages --format npm
rvs art package show @acme/widgets --target platform/packages --format npm
rvs npm --rvs-target platform/packages dist-tag ls @acme/widgets
```

`tag list` shows the tags as installs in that repository resolve them, `latest` first, with each tag's version, state, stored version, and revision. It also shows where each tag comes from (`Source`) and whether it is `Read-only`, and it lists the tags of a package an upstream supplies. `package show` prints a `Tags` line and marks the versions that carry a tag. `rvs npm dist-tag ls` reads from the repository's install address with read access and shows only what installs resolve.

A tag resolves only to a version that can be installed from the repository. While the version it is set to cannot (it is in the trash, held for checking, quarantined, or blocked), the stored tag is kept but not served:

- `latest` is a `fallback`: it resolves to the best installable version, not the stored one.
- Any other tag is `hidden`: installs by that tag find nothing.

Both apply again as soon as the stored version is installable, for example after it is restored from the trash or released from a hold. Report a fallback or hidden tag with its stored version; do not move the tag to "repair" it unless the user asks for that change. Callers without publish access see only the tags that resolve, without stored versions or revisions, so a tag missing from their view is not proof that it does not exist.

Reading tags never authorizes changing them.

### Change tags

```bash
rvs art package tag set @acme/widgets beta 2.0.0-beta.1 \
  --target platform/packages --format npm
rvs art package tag set @acme/widgets latest 1.9.0 \
  --target platform/packages --format npm --expect-revision 3
rvs art package tag delete @acme/widgets beta \
  --target platform/packages --format npm --expect-revision 1
```

`tag set` creates the tag or moves it to the version; `tag delete` removes the tag at once (tags do not go to the trash) and leaves the version unchanged. Both need publish access and change what installs get:

- Resolve and state the exact account, repository, format, package, tag, and version first, and the version the tag points at now. Never choose the package, tag, or version on the user's behalf.
- Take the tag's revision from `tag list` and pass `--expect-revision N`, so the change applies only if nobody changed the tag since it was read.
- Moving `latest` and deleting any tag ask for confirmation. Pass `--yes` only when the user authorized exactly that change; with root `--json` the command stops without the change unless `--yes` is passed.
- A new tag name must not look like a version or version range (`2.0.0`, `v2`, `^1`) or equal one of the package's versions. Use names such as `next`, `beta`, `canary`, or `v1-lts`.
- Verify afterwards with `tag list`.

### Refusals

`rvs` explains a refusal in words and may not print the reason name. Do not retry a refused change unchanged, and do not reach for another route.

| Reason | Meaning | What to do |
| --- | --- | --- |
| `target_unavailable` | The version is not installable in this repository: in the trash, held, quarantined, or blocked. | Report it. The user restores the version in the web app, waits for the check, or names another version. Do not pick one. |
| `latest_required` | `latest` cannot be deleted while the package still has versions, unless an upstream also serves versions of it under a version-level resolution rule (installs then take the upstream's `latest`). | Move it with `tag set` to a version the user names. Do not delete versions to get around it. |
| `revision_mismatch` | The tag changed since it was read. | Run `tag list` again, show the user the current state, and continue only if the change is still wanted. Never drop `--expect-revision` to force it. |
| `tag_limit` | The package has the maximum number of tags. | Ask which tag to delete; do not choose one. |

Other refusals: a format other than npm (tags are not supported there), an invalid tag name, missing publish access, and a package, tag, or version that does not exist in the repository.

### Tags from an upstream

A repository manages only its own tags, and a tag in it can point only at a version the repository itself holds. When an upstream (an attached repository or a remote cache) supplies the package or the version, its tags are read-only in the consuming repository and are changed in their source: in the attached repository, with that repository as the explicit target and publish access there, or in the remote registry behind a remote cache, which Ravenstash does not change.

Changing such a tag or tagging such a version is refused as a conflict that names the upstream. `tag list` marks these tags `Read-only`. In both cases stop: do not retry, do not try `rvs npm dist-tag`, the web app, or an API call instead, and do not publish a copy of the version to make it taggable. Use `rvs art repo upstream list platform/packages npm` to see the repository's sources and tell the user where the tag is managed.

### Native npm

```bash
rvs npm --rvs-target platform/packages dist-tag ls @acme/widgets
rvs npm --rvs-target platform/packages dist-tag add @acme/widgets@2.0.0-beta.1 beta
rvs npm --rvs-target platform/packages dist-tag rm @acme/widgets beta
rvs npm --rvs-target platform/releases publish --tag next
```

- The wrapper sends `dist-tag ls` to the install address with read access and `dist-tag add` and `rm` to the publish address with publish access. Do not pass `--registry`.
- Always give `dist-tag add` both the version and the tag. Without a tag npm means `latest`, and without a version it sends `*`.
- `dist-tag add` that points `latest` at a version and every `dist-tag rm` ask for confirmation. A run that cannot answer, such as CI, stops without the change unless `--rvs-yes` is placed before the npm arguments; add it only for an authorized change.
- The same rules and refusals apply as for `rvs art package tag`. npm has no revision precondition, so prefer `rvs art package tag set` or `delete` with `--expect-revision` when a concurrent change would matter.
- `publish --tag NAME` gives the published version that tag instead of moving `latest`; use it for prereleases. A package that has no `latest` yet still gets `latest` on that version. Check the result with `tag list`.

## Configuration

`rvs art endpoint --format npm` prints routing; `rvs art native config npm` prints setup instructions without minting credentials or writing files. Persistent configuration changes require explicit intent. Do not place an access token in a tracked `.npmrc`, command argument, or output.
