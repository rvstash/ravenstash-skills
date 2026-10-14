# Installation, updates, runtimes, and shell integration

Load only for installation, upgrades, runtime management, or shell changes.

## Install and update

The shell installer selects the released native build on supported Linux and macOS systems:

```bash
curl -fsSL https://ravenstash.com/install.sh | bash
```

Windows 11 uses PowerShell:

```powershell
irm https://ravenstash.com/install.ps1 | iex
```

The supported release targets Linux glibc and musl, macOS, and Windows on amd64 and arm64, plus versioned Nix flakes and matching Linux paths for WSL2. The installer executes downloaded code. Show the applicable command and installer URL for review; run it only when the user has authorized the host-level installation. CI jobs install an exact version instead; see the packages skill's automation reference or the [setup-ravenstash action](https://github.com/rvstash/setup-ravenstash).

Check for compatible updates without applying one:

```bash
rvs update
```

Applying an update changes the installed system package:

```bash
rvs update --apply
```

Before 1.0, all releases share the rolling `v0` channel, so a plain update can move to a newer minor release; review the release notes first. To take the latest patch of one minor line for a single update, without pinning later updates to it:

```bash
rvs update --to 0.MINOR
rvs update --to 0.MINOR --apply
```

The first command only previews; only `--apply` installs. `--yes` requires `--apply`. A configuration written by a pre-release `rvs` is refused and left unchanged; resetting it with `rvs profile delete --all` removes every local profile, so run it only when the user asks.

APT installations delegate to APT. Portable Linux, Alpine, macOS, and Windows installations authenticate, stage, health-check, and activate the matching bundle. Nix installations delegate replacement to Nix. Do not replace the binary manually or bypass the signed update path.

Signed release candidates can be previewed and installed explicitly:

```bash
rvs update --candidate X.Y.ZrcN
rvs update --candidate X.Y.ZrcN --apply
```

## Managed runtimes

Runtime management is optional and supports local Python, Node.js, and Java:

```bash
rvs runtime install python 3.14
rvs runtime install node 22
rvs runtime install java 21
rvs runtime list
rvs runtime doctor
```

Installation downloads content and changes `~/.rvs/runtimes`. `--force` removes and replaces an existing matching runtime; do not use it unless requested.

Project selection writes a conventional local file:

```bash
rvs runtime use python 3.14
rvs runtime use node 22
rvs runtime use java 21
```

Report `.python-version`, `.node-version`, or `.java-version` as a changed file and do not assume it should be committed.

## Shell changes

- `rvs runtime setup-shell` installs runtime shims. `rvs` has no other shell-integration command.

Runtime shim setup can edit a shell startup file. Inspect or report the change and do not apply it merely because a single command needs environment variables.
