# Use a specific version of pypy to ensure reproducibility
FROM python:3.11.1-slim AS python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Add poetry and venv to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder stage to install dependencies
FROM python-base AS builder-base

# Install dependencies for building Python packages
RUN apt-get update && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        python3-dev \
        libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

# Copy only pyproject.toml for dependency installation
COPY pyproject.toml ./
RUN poetry install --only=main --no-interaction --no-ansi --no-root

# Set working directory
WORKDIR /app

# Copy the application code
COPY . /app/