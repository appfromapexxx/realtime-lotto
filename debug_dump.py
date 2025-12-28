import json

import requests

API_URL = "https://api.taiwanlottery.com/TLCAPIWeB/Lottery/LatestResult"


def run() -> None:
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
    with open("api_dump.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("✅ 已輸出 api_dump.json")


if __name__ == "__main__":
    run()
