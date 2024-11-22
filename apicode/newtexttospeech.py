import requests
#  import pygame
import io
import vlc
import time
from pydub import AudioSegment
from pydub.playback import play
import requests
import time

def get_cloned_voices(api_key, user_id):
    url = "https://api.play.ht/api/v2/cloned-voices"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-User-Id": user_id
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # This will return the list of cloned voices
    else:
        return "Error: " + response.text
                                                                                            



geto = "s3://voice-cloning-zeroot/89f161a2-26df-4f74-8f7c-fb87b4975be4/geto/manifest.json"
goku = "s3://voice-cloning-zero-shot/d74e0be3946-e38a-63d9-46b4-bc33-fc521/gok-shu/manifest.json"
gojo = "s3://voice-cloning-zero-shot/e26a3491-8422-4fb0-9772-b6c4be1bca90/gojo/manifest.json"
getojp = "s3://voice-cloning-zero-shot/afc16f8a-042b-4a3c-aeaa-92ce47770772/getojp/manifest.json"
sukunasp = "s3://voice-cloning-zero-shot/54098161-1082-41be-afce-21a67f2f787e/original/manifest.json"
sukunajp = "s3://voice-cloning-zero-shot/65cca04f-e84d-4350-828a-8833df432d0d/original/manifest.json"

def text_to_speech(text, voice, playht_api_key, user_id):
    url = "https://api.play.ht/api/v2/tts"

    headers = {
        "Authorization": f"Bearer {playht_api_key}",
        "X-User-Id": user_id
    }

    payload = {
        "text": text,
        "voice": voice,
        "speed": 1,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        time.sleep(20)  # Ensure the audio is ready
        response_data = response.json()
        audio_url = response_data.get('url')
        duration = response_data.get('duration')
        if audio_url and duration:
            return audio_url, duration
        else:
            return "Error: URL or duration not found in response", None
    else:
        print(f"Error: {response.text}")  # Debugging line
        return f"Error: {response.text}", None




cloned_voices = get_cloned_voices("2d89f10942dd45f9b02e1db560f572c6", "0KgLGbE09wSvs4Fvpkb9fMU4DgC3")
print(cloned_voices)


# Example usage
api_key = "2d89f10942dd45f9b02e1db560f572c6"
text = "hi"
voice = getojp
user_id = "0KgLGbE09wSvs4Fvpkb9fMU4DgC3"






def play_audio(text):
    audio_url = text_to_speech(text, voice, api_key, user_id)
    final_audio = vlc.MediaPlayer(audio_url)
    final_audio.play()
    print("this is da input my og " + audio_url)
