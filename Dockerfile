FROM python:3.11.8-slim-bookworm AS requirements-stage

WORKDIR /tmp

RUN pip install --no-cache-dir uv==0.5.12

COPY ./pyproject.toml ./uv.lock /tmp/

RUN uv export --format requirements-txt --no-dev --no-hashes --output-file requirements.txt

FROM python:3.11.8-slim-bookworm

ARG GIT_REVISION="0000000"
ARG GIT_TAG="x.x.x"

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt && \
    playwright install --with-deps


CMD ["python", "workshop_playwright_python/core.py"]
