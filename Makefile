# Git
GIT_REVISION ?= $(shell git rev-parse --short HEAD)
GIT_TAG ?= $(shell git describe --tags --abbrev=0 --always | sed -e s/v//g)

# Project
SKIP_TEST ?= true

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

.PHONY: info
info: ## show information
	@echo "GIT_REVISION: $(GIT_REVISION)"
	@echo "GIT_TAG: $(GIT_TAG)"

.PHONY: install-deps-dev
install-deps-dev: ## install dependencies for development
	uv sync --all-extras
	uv run pre-commit install
	uv run playwright install

.PHONY: install-deps
install-deps: ## install dependencies for production
	uv sync --no-dev

.PHONY: format-check
format-check: ## format check
	uv run ruff format --check --verbose

.PHONY: format
format: ## format code
	uv run ruff format --verbose

.PHONY: fix
fix: format ## apply auto-fixes
	uv run ruff check --fix

.PHONY: lint
lint: ## lint
	uv run ruff check .

.PHONY: test
test: ## run tests
	SKIP_TEST=$(SKIP_TEST) uv run pytest --capture=no -vv

.PHONY: ci-test
ci-test: install-deps-dev format-check lint test ## run CI tests

.PHONY: update
update: ## update packages
	uv lock --upgrade

# ---
# Docker
# ---
DOCKER_REPO_NAME ?= ks6088ts
DOCKER_IMAGE_NAME ?= workshop-playwright-python
DOCKER_COMMAND ?= python scripts/visasq.py scrape --help

# Tools
TOOLS_DIR ?= /usr/local/bin
TRIVY_VERSION ?= 0.58.1

.PHONY: docker-build
docker-build: ## build Docker image
	docker build \
		-t $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG) \
		--build-arg GIT_REVISION=$(GIT_REVISION) \
		--build-arg GIT_TAG=$(GIT_TAG) \
		.

.PHONY: docker-run
docker-run: ## run Docker container
	docker run --rm $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG) $(DOCKER_COMMAND)

.PHONY: docker-lint
docker-lint: ## lint Dockerfile
	docker run --rm -i hadolint/hadolint < Dockerfile

.PHONY: docker-scan
docker-scan: ## scan Docker image
	@# https://aquasecurity.github.io/trivy/v0.18.3/installation/#install-script
	@which trivy || curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b $(TOOLS_DIR) v$(TRIVY_VERSION)
	trivy image $(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG)

.PHONY: ci-test-docker
ci-test-docker: docker-lint docker-build docker-scan docker-run ## run CI test for Docker

.PHONY: docker-visasq-scrape
docker-visasq-scrape: ## scrape visasq entries using Docker
	docker run --rm \
		-v $(PWD)/assets:/app/assets \
		$(DOCKER_REPO_NAME)/$(DOCKER_IMAGE_NAME):$(GIT_TAG) \
		python scripts/visasq.py scrape --max-page 20

# ---
# Docs
# ---

.PHONY: docs
docs: ## build documentation
	uv run mkdocs build

.PHONY: docs-serve
docs-serve: ## serve documentation
	uv run mkdocs serve

.PHONY: ci-test-docs
ci-test-docs: docs ## run CI test for documentation

# ---
# Project
# ---

.PHONY: test-verbose
test-verbose: ## run tests with verbose
	uv run pytest \
		--capture=no \
		--verbose \
		--headed \
		--tracing on \
		--video on \
		--screenshot on \
		--output generated

TRACE_ZIP ?= generated/tests-test-core-py-test-get-started-link-chromium/trace.zip
.PHONY: show-trace
show-trace: ## show trace
	uv run playwright show-trace $(TRACE_ZIP)

.PHONY: codegen
codegen: ## generate test code
	uv run playwright codegen \
		--target python-pytest \
		--output tests/test_codegen.py

.PHONY: locust
locust: ## run locust server running on localhost:8089
	uv run locust \
		--locustfile scripts/locustfile.py \
		--host http://localhost:8888 \
		--web-port 8089
