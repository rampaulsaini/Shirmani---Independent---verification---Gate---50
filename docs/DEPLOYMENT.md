# Deployment and operating boundary

## Desired state

The repository should expose the verification dashboard through GitHub Pages and continuously refresh its evidence-driven report.

The workflow builds a Pages artifact and invokes actions/deploy-pages@v4.

## Repository-level Pages setting

**Current state: ENABLED.**

The repository is configured to use **GitHub Actions** as the Pages deployment source.

## Verified diagnostic

On 2026-10-04, workflow run **#19** completed the complete deployment path successfully:

- regression tests;
- deterministic verifier;
- report validation;
- repository-structure validation;
- report persistence;
- site build;
- Pages artifact upload;
- audit artifact upload;
- GitHub Pages deployment.

The earlier HTTP 404 was the pre-enablement state. It is retained only as historical diagnostic context, not as the current operational status.

## Operational rule

A deployment is considered operational only when the `deploy` job itself completes successfully. Artifact upload alone is not treated as deployment success.

## Integrity rule

Do not mark deployment as successful merely because the artifact was uploaded. A deployment is operational only when the deploy job itself completes successfully and GitHub provides the Pages environment URL.
