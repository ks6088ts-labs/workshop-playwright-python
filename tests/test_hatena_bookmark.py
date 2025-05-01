import json

from playwright.sync_api import Page


def test_hatena_bookmark(page: Page):
    page.goto("https://b.hatena.ne.jp/hotentry/all")

    entries = []
    for entry in page.query_selector_all(".entrylist-contents-main"):
        title_element = entry.query_selector(".entrylist-contents-title a")
        bookmark_element = entry.query_selector(".entrylist-contents-users span")

        if title_element and bookmark_element:
            title = title_element.inner_text()
            url = title_element.get_attribute("href")
            bookmarks = bookmark_element.inner_text().replace("users", "").strip()

            entries.append({"title": title, "url": url, "bookmarks": int(bookmarks) if bookmarks.isdigit() else 0})

    print(json.dumps(entries, indent=2, ensure_ascii=False))
