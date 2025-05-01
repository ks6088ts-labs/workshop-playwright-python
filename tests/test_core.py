import logging
import re

from playwright.sync_api import Page, expect
from workshop_playwright_python.core import hello_world


def test_hello_world_verbose(caplog):
    with caplog.at_level(logging.DEBUG):
        hello_world(verbose=True)
    assert "Hello World" in caplog.text


def test_hello_world_non_verbose(caplog):
    with caplog.at_level(logging.DEBUG):
        hello_world(verbose=False)
    assert "Hello, world!" not in caplog.text


def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))


def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
