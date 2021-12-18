FROM python:3.9-slim-buster as base


ARG APP_ENV

ENV APP_ENV=${APP_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.5 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin"

# System dependencies
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    curl \
    # Define build-time-only dependencies
    $BUILD_ONLY_PACKAGES \
  && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - \
  && poetry --version \
  # Remove build-time-only dependencies
  && apt-get remove -y $BUILD_ONLY_PACKAGES \
  # Clean cache
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
WORKDIR /app

 
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi \
  && rm -rf "$POETRY_CACHE_DIR"
 
COPY . .
 
FROM base as final

 
 
ENTRYPOINT ["poetry", "run", "python", "./api.py"]