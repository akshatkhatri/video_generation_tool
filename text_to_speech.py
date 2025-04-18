from news_scraping import fetch_latest_news
from news_scraping import api_key

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
speech_key_1 = "GDNrHswpuz5XeQ6lgWuljcBX1dRF8VhTgsk9N4joAlekSexZa9G9JQQJ99BDACqBBLyXJ3w3AAAYACOG9vTX"
speech_key_2 = "1i9N63QXOI3o2CEZDhp4M7sJbUtYrqFtRFRSAq9tQ380mi1FdO1JJQQJ99BDACqBBLyXJ3w3AAAYACOGlOs2"
service_region = "southeastasia"
your_key = speech_key_1
your_region = service_region

news_article = fetch_latest_news(api_key)
article = news_article[1]
script_text = article['description']
# script_text = "Telangana has clinched investments worth 29,000 crore rupees in clean energy. This could be a game-changer for India’s renewable energy future."

text_to_speech(script_text, "output_audio.mp3", your_key, your_region)

