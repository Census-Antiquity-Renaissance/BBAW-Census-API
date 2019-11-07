FROM tiangolo/uvicorn-gunicorn:python3.7

ARG APP_ENV

ENV POETRY_VERSION=0.12 \
  APP_ENV=debug

RUN pip install "poetry==${POETRY_VERSION}"


# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY . /code/

# Project initialization:
RUN poetry config settings.virtualenvs.create false \
  && poetry install --no-interaction --no-ansi