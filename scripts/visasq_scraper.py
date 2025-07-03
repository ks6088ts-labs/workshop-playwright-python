import asyncio
import csv
import datetime
import os

from playwright.async_api import Page, async_playwright


async def dump_csv(entries, filepath="assets/visasq_entries.csv"):
    """CSV ファイルにエントリを保存するヘルパー関数"""
    # assets ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

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


async def retrieve_visasq_entries(page: Page, url: str):
    entries = []
    await page.goto(url)
    await page.wait_for_load_state("networkidle")

    # href の url パターンが /issue/12345/ のような形式である要素
    for entry in await page.query_selector_all("a[href^='/issue/']"):
        url = await entry.get_attribute("href")

        # h3 タグの中にある要素を取得
        h3_element = await entry.query_selector("h3")

        # p class=description-regular-14 の中にある要素を取得
        p_element = await entry.query_selector("p.description-regular-14")

        # h3_element と p_element が両方存在する場合のみ処理を続ける
        if not h3_element or not p_element:
            continue

        # entries リストに辞書形式で追加
        entries.append(
            {
                "id": url.split("/")[-2],  # URL から ID を抽出
                "url": url,
                "title": await h3_element.inner_text() if h3_element else "",
                "description": await p_element.inner_text() if p_element else "",
            }
        )
    return entries


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        BASE_URL = "https://expert.visasq.com"
        all_entries = []
        max_page = 15

        try:
            for page_number in range(1, max_page + 1):
                print(f"Retrieving entries from page {page_number}...")
                entries = await retrieve_visasq_entries(
                    page=page,
                    url=f"{BASE_URL}/issue/?keyword=&is_started_only=true&page={page_number}",
                )

                # entries の url を絶対 URL に変換
                for entry in entries:
                    entry["url"] = f"{BASE_URL}{entry['url']}"

                all_entries.extend(entries)
                print(f"Found {len(entries)} entries on page {page_number}")
                if len(entries) == 0:
                    print("No more entries found, stopping the scrape.")
                    break
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

        # 現在の日時をファイル名に含める
        now = datetime.datetime.now()
        filepath = "assets/visasq_entries_" + now.strftime("%Y%m%d_%H%M%S") + ".csv"

        await dump_csv(
            entries=all_entries,
            filepath=filepath,
        )

        print(f"Scraping completed. Total entries: {len(all_entries)}")
        print(f"Results saved to: {filepath}")


if __name__ == "__main__":
    asyncio.run(main())
