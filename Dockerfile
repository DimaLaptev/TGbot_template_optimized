FROM python:3.10 as base
# set work directory
WORKDIR /app/

FROM base as docker-entrypoint

FROM docker-entrypoint as non-root
RUN useradd -ms /bin/bash app
USER app

FROM base as requirements-builder

WORKDIR /build/

RUN pip --no-cache-dir install poetry

COPY pyproject.toml /build/

RUN poetry self add poetry-plugin-export
RUN poetry install --only=main --no-root
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM non-root as app

COPY --from=requirements-builder /build/requirements.txt /app/requirements.txt

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN pip install --no-cache-dir -r requirements.txt

# Дополнительные зависимости для новой архитектуры
RUN pip install --no-cache-dir pydantic-settings

# copy new project structure
COPY src ./src/

# Настройка PYTHONPATH для модулей src
ENV PYTHONPATH=/app/src

# run new architecture app
WORKDIR /app/src
ENTRYPOINT ["python"]
CMD ["main_with_pydantic.py"]

FROM app