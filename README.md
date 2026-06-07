# Skuld Website

Static landing page for Skuld — secure control plane for AI coding/security agents.

Hosted on [GitHub Pages](https://pages.github.com/).

## Live site

**https://skuldkore.github.io/website-/**

## Local preview

Open `index.html` in a browser, or serve the folder locally:

```bash
python3 -m http.server 8000
```

Then visit http://localhost:8000.

## Deployment

Pushes to `main` trigger the [Deploy GitHub Pages](.github/workflows/deploy-pages.yml) workflow, which publishes the site automatically.

### First-time GitHub setup

1. In the repository on GitHub, open **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Wait for the workflow run to finish, then open the live URL above.

## Project structure

```text
.
├── index.html
└── .github/workflows/
    └── deploy-pages.yml
```
