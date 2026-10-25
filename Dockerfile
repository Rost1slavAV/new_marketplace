
FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir poetry


WORKDIR /app


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false \
    && poetry install --no-root


COPY . .


EXPOSE 8000


CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]