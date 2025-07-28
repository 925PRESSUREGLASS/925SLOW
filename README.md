# 925\u00a0Stack\u00a0AI \u2013 Foundation\u00a01.0

This commit bootstraps the backend skeleton so we can begin iterative, spec\u2011driven development.

## Quick\u00a0start

```bash
# 1\u00a0\u2013 install tooling
poetry install

# 2\u00a0\u2013 run tests (should be 1 passing)
poetry run pytest -q

# 3\u00a0\u2013 start the API locally
poetry run uvicorn backend:create_app --factory --reload

# 4\u00a0\u2013 health check
curl http://localhost:8000/health
# => {"status":"ok"}

# 5\u00a0\u2013 stub CLI example
poetry run python -m backend.cli --prompt "Clean 12 windows in Palmyra"
```

Next PRs will flesh out agents, vector memory, SpecGuard, integrations, and the React frontend following the project blueprint.
