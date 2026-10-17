# PyPI workflows

Load for pip, uv, Twine, Python dependency, wheel, or source-distribution work.

## Install

Use a private repository once:

```bash
rvs pip --rvs-target platform/packages install internal-sdk
rvs uv --rvs-target platform/packages sync
```

Use an official private mirror once:

```bash
rvs pip --rvs-target mirror:pypiorg install requests
```

Ravenstash must be the primary index for a selected Ravenstash resolution workflow. Do not recommend pip `--extra-index-url`; dependency-confusion rules can allow the unintended index to win. Use a repository upstream attachment (configured in the Ravenstash web app) or an explicit mirror target instead.

## Publish

Publishing requires a private PyPI repository, never a mirror:

```bash
rvs twine --rvs-target platform/releases upload dist/*
rvs uv --rvs-target platform/releases publish
```

To build with pypa/build, `rvs python --rvs-target platform/packages -m build` installs the build requirements from that repository with read access. `rvs python` runs only `python -m build`; it refuses any other Python invocation, so do not route scripts or `pip` through it.

Inspect the distribution files and exact repository before publishing. A publish creates durable remote state and is not a preparatory step that may be invented to satisfy another request.

## Persistent configuration

`rvs art endpoint --format pypi --access read|publish` prints an address. `rvs art native config pip` and `rvs art native config twine` print instructions without minting credentials or changing files. Pip has fixed read intent and Twine fixed publish intent; neither accepts `--access`. Executing the printed setup or editing native configuration requires the user's corresponding intent.
