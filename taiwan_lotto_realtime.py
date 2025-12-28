import asyncio
from datetime import datetime
from urllib.parse import urlparse

import requests
from playwright.async_api import async_playwright

API_URL = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery/LatestResult"
PAGE_URL = "https://www.taiwanlottery.com/lotto/lotto_lastest_result"


def format_date(date_str: str | None) -> str:
    if not date_str:
        return "未知日期"
    try:
        date_value = datetime.fromisoformat(date_str)
    except ValueError:
        return date_str
    roc_year = date_value.year - 1911
    return f"{roc_year}/{date_value.month:02d}/{date_value.day:02d}"


def fetch_lotto_result_from_api() -> dict | None:
    """呼叫官方 API 取得最新威力彩結果"""
    print("🌐 正在抓取最新開獎結果 (API)...")
    try:
        response = requests.get(
            API_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        print(f"❌ API 連線失敗: {exc}")
        return None
    except ValueError as exc:
        print(f"❌ API 回傳不是 JSON: {exc}")
        return None

    if payload.get("rtCode") != 0:
        print(f"❌ API 回應錯誤: {payload.get('rtMsg')}")
        return None

    return (payload.get("content") or {}).get("superLotto638Result")


async def fetch_lotto_result_with_playwright() -> dict | None:
    """使用 Playwright 備援取得最新威力彩結果"""
    print("🌐 正在抓取最新開獎結果 (Playwright 備援)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        allowed_hosts = {"www.taiwanlottery.com", "taiwanlottery.com", "api.taiwanlottery.com"}

        async def route_handler(route):
            host = urlparse(route.request.url).hostname
            # Block third-party trackers to reduce privacy exposure.
            if host and host not in allowed_hosts:
                await route.abort()
                return
            await route.continue_()

        await page.route("**/*", route_handler)
        try:
            response_future = page.wait_for_response(
                lambda response: response.url.startswith(API_URL)
                and response.request.method == "GET",
                timeout=15000,
            )
            await page.goto(PAGE_URL, wait_until="domcontentloaded", timeout=60000)
            response = await response_future
            payload = await response.json()
        except Exception as exc:
            print(f"❌ Playwright 取得開獎結果失敗: {exc}")
            return None
        finally:
            await browser.close()

    if payload.get("rtCode") != 0:
        print(f"❌ API 回應錯誤: {payload.get('rtMsg')}")
        return None

    return (payload.get("content") or {}).get("superLotto638Result")


def fetch_lotto_result() -> dict | None:
    result = fetch_lotto_result_from_api()
    if result:
        return result

    print("⚠️  API 失敗，改用 Playwright 備援...")
    try:
        return asyncio.run(fetch_lotto_result_with_playwright())
    except RuntimeError as exc:
        print(f"❌ 無法啟動 Playwright: {exc}")
        return None

def main():
    result = fetch_lotto_result()
    if not result:
        return

    period = result.get("period")
    lottery_date = format_date(result.get("lotteryDate"))
    draw_order = result.get("drawNumberAppear") or []
    size_order = result.get("drawNumberSize") or []

    if len(draw_order) < 7 or len(size_order) < 7:
        print("⚠️  開獎號碼資料不足，請稍後再試。")
        return

    title = f"威力彩 第{period}期 ({lottery_date})"
    special_ball = draw_order[6]

    print("\n" + "═" * 40)
    print(f"  🎰  {title}")
    print("═" * 40)
    print("📌 開出順序：", end="")
    print("  ".join(f"{n:>2}" for n in draw_order[:6]))
    print("🔢 大小順序：", end="")
    print("  ".join(f"{n:>2}" for n in size_order[:6]))
    print(f"🔴 第二區：  {special_ball:>2}")
    print("═" * 40 + "\n")

if __name__ == "__main__":
    main()
