# Helm OCI workflows

Use the selected repository for Helm chart work with short chart paths. The repository must enable OCI; the manifest determines whether a path contains a Helm chart or container image.

## Read and render

```bash
rvs art select platform/deployment-charts
rvs helm show chart charts/api --version 1.2.3
rvs helm pull charts/api --version 1.2.3
rvs helm template preview charts/api --version 1.2.3
```

Selection changes saved metadata; use `--rvs-target` for an authorized one-shot target without changing selection. Short paths are private, including names matching local directories or public aliases such as `bitnami/nginx`. Use explicit local paths (`./api`) for local charts and plain Helm for configured public aliases. Full OCI/HTTP URLs and explicit `--repo` keep their native meaning. No private miss falls back publicly.

## Publish or deploy

Within the user's authorized publication scope:

```bash
rvs helm push api-1.2.3.tgz
rvs helm push api-1.2.3.tgz team/backend
```

The first destination is the selected repository root; the second adds a subdirectory. Helm appends the chart metadata name and version. Do not include them in the push destination. Verify the resulting reference and digest.

Install and upgrade also accept short chart operands. Release names remain unchanged; deploying a release is a separate user action from reading or publishing a chart. Preserve the intended Kubernetes context and namespace.

Keep full repository URLs in `Chart.yaml`. One invocation authorizes one private Ravenstash repository, while public dependencies keep their own URLs and existing credentials. Remote caches are not supported for OCI repositories.
