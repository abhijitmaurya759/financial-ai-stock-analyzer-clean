import requests
from config import NEWS_API_KEY

def get_news(company):

    query = f'"{company}"'

    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"

    r = requests.get(url)
    data = r.json()

    articles = data.get("articles", [])

    headlines = []

    for a in articles:
        headlines.append(a["title"])

    return headlines