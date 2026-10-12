# Authentication and context

Load this reference for interactive login, automation authentication, multiple local profiles, acting-account selection, or artifact-target resolution.

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

A PAT or organization automation token acts for exactly one account, so commands use that account and ignore the saved or shell selection. `RVS_ACCOUNT_REF`, if set, must name the same account, or the command stops. `rvs status` shows the token's account with the source `access token (RVS_TOKEN)`.

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
rvs art clear
```

Target forms are `namespace/repository`, `in/ar_...`, `mirror:source`, and `custom-mirror:name`. `rvs art status` shows a repository as `repo:namespace/repository`, which is accepted as the same target. Prefer one-shot `--target` or wrapper `--rvs-target` when the user did not ask to change saved selection.

Resolution precedence is:

1. Explicit one-shot target.
2. Selected target for the effective local profile and acting account.

With neither, the command stops and asks for `--target` or `rvs art select`; there is no per-format default or automatic mirror fallback. `rvs art package` commands follow the same rule and need `--format` only when the repository has more than one of PyPI, npm, and Maven.

A selection stores a format only when `--format` was passed or the target has one format. Otherwise `rvs art status` leaves the format empty and each wrapper uses its own format; running a wrapper never changes the selection.

An explicit account is resolved before the target. A failed authorization or missing immutable target must not trigger a retry against another account or a same-named repository.
