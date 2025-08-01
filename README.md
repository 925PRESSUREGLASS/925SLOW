# 925 0Stack a0AI  e2 80 93 Foundation a01.0

This commit bootstraps the backend skeleton so we can begin iterative, spec11driven development.

## Quick a0start

```bash
# 1 a013 install tooling
poetry install

# 2 a013 run tests (should be 1 passing)
poetry run pytest -q

# 3 a013 start the API locally
poetry run uvicorn backend:create_app --factory --reload

# 4 a013 health check
curl http://localhost:8000/health
# => {"status":"ok"}

# 5 a013 stub CLI example
poetry run python -m backend.cli --prompt "Clean 12 windows in Palmyra"
```

Next PRs will flesh out agents, vector memory, SpecGuard, integrations, and the React frontend following the project blueprint.
