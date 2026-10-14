# Package automation

Load for CI, release jobs, non-interactive installs, or publishing.

## Install an exact rvs version

Install the exact `rvs` release the job was written for, never whatever is newest. The CLI is pre-1.0 and can change commands between minor releases, so a version change belongs in a reviewed workflow change, after reading the [changelog](https://github.com/rvstash/ravenstash-cli/blob/main/CHANGELOG.md).

In GitHub Actions, use `rvstash/setup-ravenstash` pinned to a full commit SHA. Its `version` input is required and exact:

```yaml
- name: Set up Ravenstash CLI
  uses: rvstash/setup-ravenstash@969c51bc762cc75cbe5707e99b63aedad7bd22da # v0.1.0
  with:
    version: "0.15.1"
```

On other CI systems, use the portable installer with an exact version:

```bash
curl -fsSL https://ravenstash.com/install.sh \
  | RVS_INSTALL_METHOD=portable RVS_INSTALL_VERSION=0.15.1 bash
export PATH="$HOME/.local/bin:$PATH"
```

Keep the plain installer for interactive machines; on Debian-family systems it configures APT, which follows the newest release.

## Authentication

Inject an eligible automation token from the CI system's secret store:

```bash
export RVS_TOKEN="${TOKEN_FROM_SECRET_STORE}"
rvs auth whoami
```

Do not run device login in CI. `RVS_TOKEN` is not refreshed, and its ownership determines the available accounts and repositories.

## Make context explicit

The token acts for exactly one account, which `rvs` uses automatically. Make the target explicit for each invocation in shared runners:

```bash
rvs npm --rvs-target platform/packages ci
```

Use equivalent wrappers for pip, uv, Twine, or Maven. A job should not depend on an interactive user's selected target. `RVS_ACCOUNT_REF`, if set, must name the token's account.

## Logging and cleanup

- Do not enable shell tracing around token export or authenticated invocations.
- Review verbose native-client logs before publishing them as artifacts.
- Do not write the token to a generated package-manager configuration file.
- Remove temporary files created by the job through its normal workspace cleanup; do not delete user configuration outside the runner workspace.

`rvs ci` is absent. CI workflows install `rvs` with the steps above and use the package wrappers or documented native package-manager configuration.
