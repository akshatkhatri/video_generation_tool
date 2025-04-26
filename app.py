from flask import Flask, render_template, redirect, url_for
from news_scraping import fetch_latest_news
from generate_script import generate_script_for_article
from generate_catchy_lines import generate_catchy_lines_for_an_article
from convert_text_to_speech import text_to_speech
from video_generation import generate_video
from categorize_videos import categorize_videos
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('NEWS_API_KEY')
speech_key_1 = os.getenv('AZURE_API_SPEECH_KEY_1')
speech_key_2 = os.getenv('AZURE_API_SPEECH_KEY_2')
service_region = os.getenv('AZURE_API_SERVICE_REGION')


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate")
def generate():
    
    found_articles = fetch_latest_news(api_key)
    article = found_articles[0]
    headline = article['title']
    description = article['description']

    
    script = generate_script_for_article(headline, description)
    catchy_lines = generate_catchy_lines_for_an_article(headline, description)


    audio_path = "output_audio.mp3"
    text_to_speech(script, audio_path, speech_key_1, service_region)

    
    video_path = "static/videos/final_video_with_generated_text_overlay.mp4"
    video_category = categorize_videos(headline,description)
    generate_video(video_path, audio_path, catchy_lines, headline, description,video_category)

    return redirect(url_for("view_video"))

@app.route("/video")
def view_video():
    return render_template("video.html", video_file="videos/final_video_with_generated_text_overlay.mp4", timestamp=datetime.now().timestamp())

if __name__ == "__main__":
    app.run(debug=True)
