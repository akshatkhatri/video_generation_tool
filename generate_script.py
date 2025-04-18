from news_scraping import fetch_latest_news
from news_scraping import api_key
import requests
import re

# Fetch news
news_articles = fetch_latest_news(api_key)
article = news_articles[0]

def generate_script_for_article(headline, description):
    prompt = (
    f"You are a professional news video scriptwriter.\n\n"
    f"Your task is to generate ONLY a short and engaging voiceover script for a news video.\n"
    f"Input:\nHeadline: '{headline}'\nDescription: '{description}'\n\n"
    f"Instructions:\n"
    f"- Write ONE single, continuous paragraph (no bullet points).\n"
    f"- The script must be professional, clear, and engaging.\n"
    f"- Begin with a strong hook, explain the story briefly, and end with a punchy closing line.\n"
    f"- DO NOT repeat the headline directly.\n"
    f"- The script must sound natural when read aloud and be suitable for video overlay.\n"
    f"- The length should match a 20–25 second narration.\n"
    f"- STRICTLY return ONLY the final script. Do NOT include any titles, summaries, comments, notes, or introductions like 'Here is your summary'.\n"
    f"- The response must be JUST the paragraph, nothing else.\n"
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
            script = response.json()["choices"][0]["message"]["content"]
            cleaned_script = re.sub(r"<think>.*?</think>", "", script, flags=re.DOTALL).strip()
            return cleaned_script

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
