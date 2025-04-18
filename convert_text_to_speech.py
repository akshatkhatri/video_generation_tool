from news_scraping import api_key

from dotenv import load_dotenv
import os

load_dotenv()

import azure.cognitiveservices.speech as speechsdk

def text_to_speech(text, filename, key, region):
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    # You can choose different voices here
    speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"  # Indian male voice

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech saved to {filename}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation.error_details}")

# Example usage
speech_key_1 = os.getenv('AZURE_API_SPEECH_KEY_1')
speech_key_2 = os.getenv('AZURE_API_SPEECH_KEY_2')
service_region = os.getenv('AZURE_API_SERVICE_REGION')
# your_key = speech_key_1
# your_region = service_region

# news_article = fetch_latest_news(api_key)
# article = news_article[0]
# headline = article['title']
# description = article['description']
# script_text = generate_script_for_article(headline,description)
# # script_text = "Telangana has clinched investments worth 29,000 crore rupees in clean energy. This could be a game-changer for India’s renewable energy future."

# text_to_speech(script_text, "output_audio.mp3", your_key, your_region)

