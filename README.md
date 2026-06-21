# CSOT Week 3 Starter

**Fork this repo** and build a full CI/CD pipeline around it.

## What's here

```
app/main.py      Flask app — /health and /api/version already wired to VERSION file
VERSION          Version string (start at 1.0.0)
requirements.txt Runtime deps only
```

## Your task

Add everything else:

| What to add | Why |
|-------------|-----|
| `Dockerfile` | containerize the app |
| `compose.yaml` | run with nginx proxy; web must use `ports: ["0:80"]` |
| `nginx/default.conf` | reverse-proxy to the api container |
| `tests/test_*.py` | pytest tests covering your routes (≥70% coverage) |
| `requirements-dev.txt` | pytest, pytest-cov, etc. |
| `.github/workflows/ci.yml` | full CI: lint → test → secret-scan → dep-scan → build-push → deploy |

## Grader requirements

Two endpoints **must** exist in your app:

```
GET /health       → {"status": "ok"}
GET /api/version  → {"version": "<contents of VERSION file>"}
```

The `VERSION` file lives at the **repo root**.
The grader commits `VERSION=1.0.1` to trigger your CD pipeline and checks
that `/api/version` returns `1.0.1` after your deploy job runs.

## Scoring (300 pts)

**Act 1 — CI & containerize (200 pts)**

| Check | Pts |
|-------|-----|
| tests/ with test_*.py | 5 |
| CI runs pytest | 5 |
| Coverage ≥70% gate in CI | 5 |
| Submitted commit CI all green | 10 |
| AI test review (routes + schema + # tests) | 15 |
| Lint job in CI | 5 |
| Linter tool (ruff/flake8/pylint) | 5 |
| Secret scan (TruffleHog/gitleaks) | 5 |
| Dependency scan (pip-audit) | 5 |
| Dockerfile | 5 |
| compose.yaml | 5 |
| Web uses port `"0:80"` | 5 |
| SQLite volume in compose | 5 |
| docker/build-push in CI | 5 |
| VERSION file | 3 |
| GET /api/version in code | 3 |
| .github/workflows/ | 4 |
| Deploy job with SSH | 5 |

**Act 2 — Live CD deploy (100 pts)**

| Check | Pts |
|-------|-----|
| Deploy job exists in workflow | 10 |
| Live app serves version 1.0.0 (click Verify on portal) | 45 |
| Grader commits VERSION=1.0.1 → CD auto-deploys → live shows 1.0.1 | 45 |

## Secrets for the deploy job

Once you submit on the portal, a personal sandbox is provisioned for you.
Add these to your repo: Settings → Secrets and variables → Actions.

| Secret | Value (from portal) |
|--------|---------------------|
| `DEPLOY_HOST` | sandbox IP |
| `DEPLOY_SSH_PORT` | SSH port |
| `DEPLOY_USER` | `incident` |
| `DEPLOY_PASSWORD` | sandbox password |
| `DEPLOY_PATH` | deploy directory path |
| `COMPOSE_PROJECT_NAME` | compose project name |
