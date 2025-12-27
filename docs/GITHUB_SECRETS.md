# GitHub Secrets Configuration

This document explains what GitHub Secrets are needed for the CI/CD workflows.

## Automatic Secrets (No Configuration Needed)

### `GITHUB_TOKEN`
- **Automatically provided** by GitHub Actions
- **Used by**: Docker Build, Terraform workflows
- **Purpose**: Authenticate with GitHub Container Registry (GHCR), post comments on PRs
- **Status**: ✅ Ready to use, no setup needed

## Optional Secrets (For Enhanced Functionality)

### `OPENWEATHER_API_KEY` ✅ CONFIGURED
- **Used by**: pipeline-tests.yml
- **Purpose**: Real weather data ingestion in integration tests
- **Status**: ✅ Configured in "prod" environment
- **Environment**: prod
- **Available to**: pipeline-tests.yml when using `environment: prod`

### `CODECOV_TOKEN`
- **Used by**: tests.yml
- **Purpose**: Upload coverage reports to Codecov.io
- **Status**: ❌ Optional (workflow continues even if upload fails)
- **To Add**:
  1. Register at https://codecov.io
  2. Connect your GitHub repository
  3. Copy the token from Codecov dashboard
  4. Add to GitHub Secrets with name `CODECOV_TOKEN`

## Summary

| Secret | Required | Auto | Status | Environment |
|--------|----------|------|--------|-------------|
| GITHUB_TOKEN | ✅ Yes | ✅ Yes | Ready | N/A |
| OPENWEATHER_API_KEY | ❌ No | ❌ No | ✅ Configured | prod |
| CODECOV_TOKEN | ❌ No | ❌ No | Optional | N/A |

## Current Workflow Status

- ✅ Tests: Work without secrets
- ✅ Docker builds: Work with automatic GITHUB_TOKEN
- ✅ Terraform: Works with automatic GITHUB_TOKEN
- ✅ Pipeline tests: **Now use REAL API data** from prod environment secret

**All workflows will run successfully without any manual configuration.**

### To Add Secrets Later

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Enter name and value
5. Secrets are available to all workflows

---

**Note**: Secrets are never logged or exposed in workflow outputs.
