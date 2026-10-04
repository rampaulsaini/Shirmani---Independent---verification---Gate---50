# Deployment and operating boundary

## Desired state

The repository should expose the verification dashboard through GitHub Pages and continuously refresh its evidence-driven report.

The workflow builds a Pages artifact and invokes actions/deploy-pages@v4.

## One-time GitHub repository setting

Enable:

**Repository → Settings → Pages → Build and deployment → Source: GitHub Actions**

This is a repository administration setting. The connected GitHub tool available to this session can write repository content and workflows but does not expose the administrative mutation required to enable Pages itself.

## Verified diagnostic

On 2026-10-04 the verification job completed successfully, including:

- regression tests;
- deterministic verifier;
- report validation;
- site build;
- Pages artifact upload;
- audit artifact upload.

The separate deploy job failed with HTTP 404 when creating the Pages deployment. GitHub's own error message stated that GitHub Pages must be enabled.

Once the one-time Pages setting is enabled, the existing workflow is designed to deploy the generated dashboard automatically on its next successful run.

## Integrity rule

Do not mark deployment as successful merely because the artifact was uploaded. A deployment is operational only when the deploy job itself completes successfully and GitHub provides the Pages environment URL.
