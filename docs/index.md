# workshop-playwright-python

## Installation

To set up the environment, details are provided in [Playwright for Python > Installation](https://playwright.dev/python/docs/intro).
In this workshop, we provide a script to install the necessary dependencies.

```bash
git clone https://github.com/ks6088ts-labs/workshop-playwright-python.git
cd workshop-playwright-python

# Install the dependencies
make install-deps-dev
```

- [[BUG] Host system is missing dependencies to run browsers (WSL2) #19100](https://github.com/microsoft/playwright/issues/19100)

## Fundamentals

To run some demos, please follow the instructions below.

```bash
# Run tests in verbose mode
make test-verbose

# Show traces
make show-trace

# Generate code
make codegen
```

## Guides

### Authentication

0. Run an application server

```shell
docker compose up
```

1. Run code generator and log in to the app manually.

```shell
make codegen
```

2. Update the generated codes for storing state via `context.storage_state()` method

3. Run the updated script named as `save_context.py`

```shell
uv run scripts/save_context.py
```

4. Run the following command to access to the app without logging in.

```shell
uv run scripts/load_context.py
```

## [Microsoft Playwright Testing](https://learn.microsoft.com/ja-jp/azure/playwright-testing/)

- [Get Started Sample](https://github.com/microsoft/playwright-testing-service/tree/main/samples/get-started)

## [Playwright MCP server](https://github.com/microsoft/playwright-mcp)

## [Locust](https://github.com/locustio/locust)

- [Your first test](https://docs.locust.io/en/stable/quickstart.html)

## Custom apps

### Credentials

Run the following command to set up the credentials for the application.

```shell
# Run the application
uv run streamlit run workshop_playwright_python/apps/streamlit_authentication.py
```

To login, type your credentials described in [.streamlit/config.yaml](../.streamlit/config.yaml) and click the "Login" button. (e.g. `jsmith:abc`, `rbriggs:def`)

### OpenID Connect

To run a frontend application with authentication, you can refer to the following links.

- [User authentication and information](https://docs.streamlit.io/develop/concepts/connections/authentication)
- [Use Microsoft Entra to authenticate users](https://docs.streamlit.io/develop/tutorials/authentication/microsoft)

For example, you can use the following file [.streamlit/secrets.toml](../.streamlit/secrets.toml.example) to set up authentication with Microsoft Entra ID.

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "xxx"

[auth.microsoft]
client_id = "your-client-id"
client_secret = "your-client-secret"
server_metadata_url = "https://login.microsoftonline.com/consumers/v2.0/.well-known/openid-configuration"
```

Then, run the application using the following command:

```shell
# Run the application
uv run streamlit run workshop_playwright_python/apps/authentication.py
```
