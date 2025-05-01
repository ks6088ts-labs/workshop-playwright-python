import json

from playwright.sync_api import Playwright, StorageState, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8888/")
    page.get_by_role("textbox", name="Email Address / Username").fill("admin@example.com")
    page.get_by_role("textbox", name="Password").fill("very-strong-password")
    page.get_by_role("button", name="Login").click()

    storage: StorageState = context.storage_state(path="playwright/.auth/storage.json")
    print(json.dumps(storage, indent=2))

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
