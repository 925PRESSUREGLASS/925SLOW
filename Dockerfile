FROM nvidia/cuda:12.3.0-base-ubuntu22.04

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y software-properties-common tzdata && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-venv python3.11-distutils curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11 && \
    pip install poetry && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

ENV PIP_DEFAULT_TIMEOUT=1800
ENV POETRY_HTTP_BASIC_PYPI_URL=https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

CMD ["poetry", "run", "uvicorn", "backend.api.root:app", "--host", "0.0.0.0", "--port", "8000"]

