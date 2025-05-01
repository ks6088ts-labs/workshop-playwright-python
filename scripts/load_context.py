from playwright.sync_api import Playwright, expect, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        storage_state="playwright/.auth/storage.json",
    )
    page = context.new_page()
    page.goto("http://localhost:8888/")

    expect(page.get_by_role("heading", name="Feature rich | Maximises")).to_be_visible()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
