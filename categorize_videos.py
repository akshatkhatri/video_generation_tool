import requests
import re
from news_scraping import fetch_latest_news,api_key

'''
1. buisness
2. crime
3. energy
4. enviornment
5. health
6. politics
7. social
8. technology
9. world
'''


def categorize_videos(headline, description): 
    prompt = (
        f"Given the following news headline and description, classify the news into one of these exact categories:\n"
        f"1. business\n2. crime\n3. energy\n4. environment\n5. health\n6. politics\n7. social\n8. technology\n9. world\n\n"
        f"Headline: {headline}\n"
        f"Description: {description}\n\n"
        f"Respond with only the **single** most appropriate category name (e.g., 'technology'). "
        f"Do not include any commentary, explanation, or punctuation. Just return the category name."
    )

    urls = [
        "https://cd8d-122-173-31-73.ngrok-free.app/v1/chat/completions",  # ngrok URL
        "http://127.0.0.1:1234/v1/chat/completions"                        # fallback to localhost
    ]

    headers = {"Content-Type": "application/json"}

    data = {
        "model": "deepseek-chat", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            script = response.json()["choices"][0]["message"]["content"]
            cleaned_script = re.sub(r"<think>.*?</think>", "", script, flags=re.DOTALL).strip()
            return cleaned_script

        except Exception as e:
            print(f"❌ Failed to connect to {url}: {e}")

    return None

if __name__ == "__main__":
    fetched_articles = fetch_latest_news(api_key)
    article = fetched_articles[0]
    headline = article['title']
    description = article['description']
    category = categorize_videos(headline,description)
    print(category)