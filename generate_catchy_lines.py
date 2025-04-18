import requests
import re
from news_scraping import fetch_latest_news
from news_scraping import api_key


news_articles = fetch_latest_news(api_key)
article = news_articles[0]

def generate_catchy_lines_for_an_article(headline, description):
    prompt = (
        f"You are a creative and professional news scriptwriter.\n"
        f"Given the following news headline and description, generate 3 short, catchy, and impactful lines that "
        f"can be used as text overlays in a short-form video.\n\n"
        f"⚠️ Strict output format:\n"
        f"Return ONLY the lines in this format:\n"
        f"- Line 1\n"
        f"- Line 2\n"
        f"- Line 3\n\n"
        f"Each line should:\n"
        f"- Be under 20 words\n"
        f"- Be bold, punchy, and informative\n"
        f"- Not include quotes or extra commentary\n"
        f"- Be directly usable as a text overlay\n\n"
        f"Headline: '{headline}'\n"
        f"Description: '{description}'\n\n"
        f"Remember: Only output the 3 lines in bullet point format. No additional thoughts, commentary, or explanation."
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
            raw_output = response.json()["choices"][0]["message"]["content"].strip()

            # Step 1: Remove the <think>...</think> block (if any)
            cleaned_script = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL).strip()

            # Step 2: Extract the bullet points as a list
            bullet_lines = [line.strip("- ").strip() for line in cleaned_script.splitlines() if line.strip().startswith("-")]
            
            return bullet_lines

        except Exception as e:
            print(f"❌ Failed to connect to {url}: {e}")

    return None

if __name__ == "__main__":
    headline = article["title"]
    description = article["description"]
    catchy_lines = generate_catchy_lines_for_an_article(headline, description)

    print("\nGenerated Script:\n")
    print(catchy_lines)
