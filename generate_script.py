from news_scraping import fetch_latest_news
from news_scraping import api_key
import requests

# Fetch news
news_articles = fetch_latest_news(api_key)
article = news_articles[2]

def generate_script_for_article(headline, description):
    prompt = (
        f"Write a short, engaging, and professional video script for the news headline: '{headline}'. "
        f"Include the description: '{description}'. "
        "The script should be suitable for a 30-45 second voiceover. "
        "Start with a hook, explain the context briefly, and end with a punchy closing line."
        "Also remember that the script will most likely be used in movie.py for text overlay"
        "and text to speech only "
    )

    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "deepseek-chat",  # Change if your model has a different name
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        script = response.json()["choices"][0]["message"]["content"]
        return script.strip()

    except Exception as e:
        print("Error generating script:", e)
        return None

# Example usage
if __name__ == "__main__":
    headline = article["title"]
    description = article["description"]
    script = generate_script_for_article(headline, description)

    print("\nGenerated Script:\n")
    print(script)
