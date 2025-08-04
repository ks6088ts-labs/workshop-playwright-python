from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.microsoft.com/ja-jp/")
    page.get_by_role("button", name="Microsoft.com を検索").click()
    page.get_by_role("combobox", name="検索が展開されています").fill("xbox controller")
    page.get_by_role("button", name="Microsoft.com を検索").click()

    # wait for 5 seconds to let the search results load
    page.wait_for_timeout(5000)

    context.close()
    browser.close()
