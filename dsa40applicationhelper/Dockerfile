##### (static) svelte(-kit) frontend #####
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build   # outputs to ../backend/static via svelte.config.js

##### fastapi frontend #####
FROM python:3.11-slim AS backend
WORKDIR /app/backend

## Setup uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev

## Copy stuff
COPY backend/ ./
COPY --from=frontend-builder /app/backend/static ./static
RUN mkdir -p data uploads

## Start
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
