from news_scraping import fetch_latest_news
from news_scraping import api_key
import requests
from news_scraping import fetch_latest_news

# Fetch news
news_articles = fetch_latest_news(api_key)
article = news_articles[0]

def generate_script_for_article(headline, description):
    prompt = (
        f"Write a short, engaging, and professional video script for the news headline: '{headline}'. "
        f"Include the description: '{description}'. "
        "The script should be suitable for a 30-45 second voiceover. "
        "Start with a hook, explain the context briefly, and end with a punchy closing line. "
        "Also remember that the script will most likely be used in movie.py for text overlay "
        "and text to speech only."
    )

    urls = [
        "https://cd8d-122-173-31-73.ngrok-free.app/v1/chat/completions",  # ngrok URL
        "http://127.0.0.1:1234/v1/chat/completions"                        # fallback to localhost
    ]

    headers = {"Content-Type": "application/json"}

    data = {
        "model": "deepseek-chat", 
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            script = response.json()["choices"][0]["message"]["content"]
            return script.strip()

        except Exception as e:
            print(f"❌ Failed to connect to {url}: {e}")

    return None

# Example usage
if __name__ == "__main__":
    headline = article["title"]
    description = article["description"]
    script = generate_script_for_article(headline, description)

    print("\nGenerated Script:\n")
    print(script)
