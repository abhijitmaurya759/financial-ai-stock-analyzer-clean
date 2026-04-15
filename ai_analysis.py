from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_news(news_list):

    if not news_list:
        return "No news available for analysis."

    news_text = "\n".join(news_list)

    prompt = f"""
Analyze the sentiment of these financial news headlines
and summarize the market outlook:

{news_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content