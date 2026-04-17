import requests
import time
from config import GNEWS_API_KEY, NEWS_API_KEY


def get_news(company):
    try:
        # 🔹 Better query (more reliable)
        query = f"{company} stock India"

        headlines = []

        # =========================
        # 🔹 1. Try GNews API FIRST
        # =========================
        if GNEWS_API_KEY:
            gnews_url = f"https://gnews.io/api/v4/search?q={query}&lang=en&max=5&apikey={GNEWS_API_KEY}"

            for _ in range(2):  # retry twice
                res = requests.get(gnews_url, timeout=5)
                data = res.json()

                if "articles" in data and data["articles"]:
                    headlines = [article["title"] for article in data["articles"]]
                    break

                time.sleep(1)

        # =========================
        # 🔹 2. Fallback: NewsAPI
        # =========================
        if not headlines and NEWS_API_KEY:
            newsapi_url = (
                f"https://newsapi.org/v2/everything?"
                f"q={query}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
            )

            for _ in range(2):
                res = requests.get(newsapi_url, timeout=5)
                data = res.json()

                if data.get("articles"):
                    headlines = [article["title"] for article in data["articles"]]
                    break

                time.sleep(1)

        # =========================
        # 🔹 3. Final fallback (VERY IMPORTANT)
        # =========================
        if not headlines:
            headlines = [
                f"No major news found for {company}.",
                "Market may be stable or experiencing low activity.",
                "Try again later for updated news."
            ]

        return headlines

    except Exception as e:
        print("News API Error:", e)

        # 🔹 Always return something (never empty)
        return [
            "News service temporarily unavailable.",
            "Please try again later."
        ]