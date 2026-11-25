# Authentication and context

Load this reference for interactive login, automation authentication, multiple local profiles, acting-account selection, per-format artifact-target selection, the default personal mirror, or status output.

Keep four layers distinct:

- the authenticated **user** is the audit actor;
- a **local profile** is named CLI configuration and a credential slot;
- the **acting account** is the personal or organization authorization and metering boundary; and
- the **artifact target** is a repository or private mirror inside that account.

## Interactive login

```bash
rvs auth login
rvs auth login --profile work
rvs auth login --duration 30d
rvs auth status
rvs auth whoami
```

Device login requires the user to review and approve the browser request. Do not automate that approval. `--duration` accepts 12 hours through 180 days; the server may reduce a requested duration to its current policy.

Inspect and manage local profiles without exposing credentials:

```bash
rvs profile list
rvs profile current
rvs profile use work
rvs profile rename old-name new-name
rvs profile delete old-name
rvs auth logout
```

Profile selection updates the persisted default. Use `--profile` or wrapper `--rvs-profile` for a one-shot operation instead. `rvs profile current` reports the selection source.

## Automation

An unattended process receives its token through the environment:

```bash
export RVS_TOKEN="${TOKEN_FROM_SECRET_STORE}"
rvs auth whoami
```

The value must originate in the user's secret manager. Never put it in a skill, repository, command transcript, shell profile, or `~/.rvs/config.toml`.

A PAT or organization automation token acts for exactly one account, so commands use that account and ignore the saved or shell selection. `RVS_ACCOUNT_REF`, if set, must name the same account, or the command stops. `rvs status` shows the token's account with the source `access token (RVS_TOKEN)`. A command authenticated with `RVS_TOKEN` never uses the default mirror described below, so automation names its target explicitly.

## Acting account

```bash
rvs account list
rvs account switch user:avery
rvs account switch org:acmehq
rvs status
```

Use the Ravenstash username for a personal account or the public handle for an organization. Account selection is persisted in the selected local profile. For one operation, use the command's `--account` option or a wrapper's `--rvs-account` option. `rvs status` verifies the user and shows the effective profile, account, target, and API. It names a person as `user:HANDLE (Name)`, never by email, and an organization automation token without repeating its organization. A selection made by an environment variable, shell session, or command option is shown next to its value; `rvs --json status` always includes `selected_by`. If `RVS_TOKEN` cannot act for the selected account, `rvs status` warns and names the token's account.

## Artifact target

```bash
rvs art status
rvs art select platform/backend
rvs art select platform/backend --format pypi
rvs art clear --format npm
rvs art clear
```

Target forms are `namespace/repository`, `in/ar_...`, `mirror:source`, and `custom-mirror:name`. `rvs art status` shows a repository as `repo:namespace/repository`, which is accepted as the same target. Prefer one-shot `--target` or wrapper `--rvs-target` when the user did not ask to change saved selection.

### One selection per format

The selection is kept separately for each format: pypi, npm, maven, and oci.

- `rvs art select TARGET` selects the target for every format it has. `--format`, repeated or comma-separated, selects it only for the named formats, each of which must be enabled on the target. There is no `all` keyword.
- Formats the target lacks, or that were not named, keep their current selection: selecting `mirror:npmjs` leaves the PyPI selection unchanged.
- The formats are recorded when selecting. After a repository gains a format, it must be selected again to be used for that format.
- `rvs art mirror select` and `rvs art mirror create --select` select a mirror for its one format.
- `rvs art clear` clears every format; `rvs art clear --format FORMAT` clears only the named formats.
- Running a wrapper never changes a selection.

Each wrapper uses the selection of its format: pypi for `rvs pip`, `rvs uv`, `rvs twine`, and `rvs python`; npm for `rvs npm` and `rvs pnpm`; maven for `rvs mvn`; and oci for `rvs docker`, `rvs helm`, and `rvs oras`.

Resolution precedence is:

1. Explicit one-shot target.
2. Target selected for the command's format in the effective local profile and acting account.
3. For pypi, npm, and maven reads only: the default mirror of a personal account signed in with `rvs auth login`, without `RVS_TOKEN` (see below).

With none of these, the command stops and asks for `--target` or `rvs art select`. `rvs art package` commands use the repository selected for `--format` when it is passed; without it, the pypi, npm, and maven formats selected with a repository must all use the same repository. They need `--format` only when that repository has more than one of PyPI, npm, and Maven, and they reject a mirror.

An explicit account is resolved before the target. A failed authorization or missing immutable target must not trigger a retry against another account, a same-named repository, or the default mirror.

### Default mirror

Ravenstash gives every personal account a private mirror of each Ravenstash-provided source. In an interactive session of a personal account, signed in with `rvs auth login` and without `RVS_TOKEN`, when nothing is selected for pypi, npm, or maven, installs and other reads through `rvs pip`, `rvs uv`, `rvs python -m build`, `rvs npm`, `rvs pnpm`, and `rvs mvn` use the account's default mirror of that format. `rvs` names that mirror in a note on standard error and saves nothing.

The default mirror never applies to:

- publishing or deletion, which need a selected or explicit private repository;
- organization accounts;
- commands authenticated with `RVS_TOKEN`, including a personal access token, so automation never gets it;
- OCI content: `rvs docker`, `rvs helm`, and `rvs oras` stop without an oci selection and ask for a private repository with the oci format, because there is no container mirror; or
- `rvs art endpoint`, `rvs art native config`, and `rvs art token mint`, which always need a selected or explicit target.

A mirror the user deleted is not recreated. `rvs art mirror create --format FORMAT --select` adds it again; run it only when the user asks. `rvs art mirror create` reports an existing mirror of the same source instead of failing, and its age options apply only to a newly created mirror.

Agent rules for the default mirror:

- If the user named a repository or mirror, pass it as a one-shot target. Do not rely on the default mirror, or on any saved selection, to reach it.
- Report the mirror named in the standard-error note as the source that was used. A default-mirror read never reached a private repository, so it is not evidence about the user's private packages.
- Do not create, select, or re-add a mirror merely to make a read succeed; report the missing selection instead.

### Status

`rvs art status` and `rvs status` only read. They show one line per format: its selected target, the default mirror marked as automatic, or `not selected`. With root `--json`, `rvs art status` adds a `formats` object and `rvs status` adds `targets.artifacts_by_format`; each has one entry per format with `target`, `type`, and `source` (`selected`, `default_mirror`, or `none`). The earlier single-target fields remain but are filled only when one target is selected for every selected format, so read the per-format entries.

### Configuration upgrade

The first command of an `rvs` 0.17 release upgrades `~/.rvs/config.toml` to schema 2 and keeps the original as `config.toml.schema-1.bak`. A repository selected without a format before the upgrade stays selected for every format until it is selected again. Earlier releases refuse the upgraded file. Do not edit the configuration or restore the backup unless the user asks to return to an earlier release.
