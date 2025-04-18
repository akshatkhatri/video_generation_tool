import requests
from news_scraping import fetch_latest_news
from news_scraping import api_key


news_articles = fetch_latest_news(api_key)
article = news_articles[0]

def generate_catchy_lines_for_an_article(headline, description):
    prompt = (
        f"You are a creative and professional news scriptwriter.\n"
        f"Given the following news headline and description, generate 3 short, catchy, and impactful lines that "
        f"can be used as text overlays in a short-form video.\n"
        f"Each line should be under 20 words, engaging, and should highlight a key point from the news.\n"
        f"These lines will appear as bold on-screen text every 10 seconds.\n\n"
        f"Headline: '{headline}'\n"
        f"Description: '{description}'\n\n"
        "Only return the lines as a bullet list, without any explanations or extra commentary."
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
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"❌ Failed to connect to {url}: {e}")

    return None

if __name__ == "__main__":
    headline = article["title"]
    description = article["description"]
    script = generate_catchy_lines_for_an_article(headline,description)

    print("\nGenerated Script:\n")
    print(script)