import csv
import datetime

import pytest

from playwright.sync_api import Page
from tests import flags


def dump_csv(entries, filepath="assets/visasq_entries.csv"):
    """CSV ファイルにエントリを保存するヘルパー関数"""
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "id",
            "url",
            "title",
            "description",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)


def retrieve_visasq_entries(page: Page, url: str):
    entries = []
    page.goto(url)
    page.wait_for_load_state("networkidle")

    # href の url パターンが /issue/12345/ のような形式である要素
    for entry in page.query_selector_all("a[href^='/issue/']"):
        url = entry.get_attribute("href")

        # h3 タグの中にある要素を取得
        h3_element = entry.query_selector("h3")

        # p class=description-regular-14 の中にある要素を取得
        p_element = entry.query_selector("p.description-regular-14")

        # h3_element と p_element が両方存在する場合のみ処理を続ける
        if not h3_element or not p_element:
            continue

        # entries リストに辞書形式で追加
        entries.append(
            {
                "id": url.split("/")[-2],  # URL から ID を抽出
                "url": url,
                "title": h3_element.inner_text() if h3_element else "",
                "description": p_element.inner_text() if p_element else "",
            }
        )
    return entries


@pytest.mark.skipif(flags.SKIP, reason="This test is just a sample scraper and is skipped by default.")
def test_visasq_entries(page: Page):
    BASE_URL = "https://expert.visasq.com"
    all_entries = []
    max_page = 15
    try:
        for page_number in range(1, max_page + 1):
            print(f"Retrieving entries from page {page_number}...")
            entries = retrieve_visasq_entries(
                page=page,
                url=f"{BASE_URL}/issue/?keyword=&is_started_only=true&page={page_number}",
            )
            # entries の url を絶対 URL に変換
            for entry in entries:
                entry["url"] = f"{BASE_URL}{entry['url']}"

            # print(
            #     json.dumps(
            #         entries,
            #         indent=2,
            #         ensure_ascii=False,
            #     )
            # )

            all_entries.extend(entries)
    except Exception as e:
        print(f"An error occurred at page {page_number}: {e}")

    now = datetime.datetime.now()
    filepath = "assets/visasq_entries_" + now.strftime("%Y%m%d_%H%M%S") + ".csv"
    dump_csv(
        entries=all_entries,
        filepath=filepath,
    )
