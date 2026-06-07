# Skuld Website

Static landing page for Skuld — secure control plane for AI coding/security agents.

Hosted on [GitHub Pages](https://pages.github.com/).

## Live site

**https://skuldkore.github.io/**

## Local preview

Open `index.html` in a browser, or serve the folder locally:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Deployment

Pushes to `main` trigger the [Deploy GitHub Pages](.github/workflows/deploy-pages.yml) workflow, which publishes the site automatically.

### First-time GitHub setup (required)

The deploy workflow will fail until GitHub Pages is enabled once for this repository.

**This repository is currently private.** On GitHub Free, Pages only works with public repositories. If Settings → Pages says *"Upgrade or make this repository public to enable Pages"*, choose one of these options first:

1. **Make the repository public** (free) — recommended for a marketing landing page
2. **Upgrade your GitHub plan** — required if you want Pages on a private repository

Then complete setup:

1. Open [Settings → Pages](https://github.com/skuldkore/skuldkore.github.io/settings/pages).
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Re-run the failed **Deploy GitHub Pages** workflow from the Actions tab.
4. Open the live URL above once the run succeeds.

#### Optional automatic enablement

To let the workflow enable Pages for you, create a repository secret named `PAGES_ENABLEMENT_TOKEN` containing a Personal Access Token with `repo` scope or Pages write permission.

## Project structure

```text
.
├── index.html
└── .github/workflows/
    └── deploy-pages.yml
```
