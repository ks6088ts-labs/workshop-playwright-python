import time

from playwright.sync_api import sync_playwright

base_url = "https://maps.google.com"
search_query = "蕎麦屋 京都駅"

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
context = browser.new_context(
    java_script_enabled=True,
    locale="ja-JP",
)
page = context.new_page()
page.goto(base_url, wait_until="load")

# find the search box
input_box = page.locator('//input[@name="q"]')
input_box.fill(search_query)
input_box.press("Enter")

xpath_search_result_element = '//div[@role="feed"]'
page.wait_for_selector(xpath_search_result_element)
results_container = page.query_selector(xpath_search_result_element)
results_container.scroll_into_view_if_needed()

keep_scrolling = True
while keep_scrolling:
    results_container.press("Space")
    time.sleep(2.5)

    # "リストの最後に到達しました。" という文字列を含む要素があるか確認
    if results_container.query_selector('//span[contains(text(), "リストの最後に到達しました。")]'):
        results_container.press("Space")
        keep_scrolling = False

    with open("maps.html", "w", encoding="utf-8") as f:
        f.write(results_container.inner_html())

context.close()
browser.close()
playwright.stop()
