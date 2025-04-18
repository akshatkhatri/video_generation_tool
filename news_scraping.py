import requests

def fetch_latest_news(api_key):
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "q": "India",  # Focus on India-related news
        # "domains": "indiatoday.in,ndtv.com,thehindu.com,timesofindia.indiatimes.com",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 30,
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Optional post-filtering step (in case more precision is needed)
    filtered_articles = [
        article for article in data.get("articles", [])
        if "India" in article.get("title", "") or "India" in article.get("description", "")
    ]

    return filtered_articles


api_key = "af7e877631704fa9a2ba13d1469cd58c"
news_articles = fetch_latest_news(api_key)
# print(news_articles)

if __name__ == "__main__":
    for i, article in enumerate(news_articles, 1):
        print(f"{i}. {article['title']}")
        print(article['description'])
        # print(article['content'])
        print(article['url'])
        print()