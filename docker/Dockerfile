FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry==1.8.2 \
  && poetry install --no-interaction --no-root
COPY . .
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
CMD ["poetry", "run", "uvicorn", "backend:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
