import requests
import pygame
import io


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







def text_to_speech(text, voice, api_key):
    url = "https://api.play.ht/api/v2/tts"

    headers = {
        "Authorization": "Bearer 2ce4d441c833453aaf3bcf1bcc2aca7b",
        "X-User-Id": user_id 
    }

    payload = {
        "text": text,
        "voice": voice,
        "speed": 1,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        audio_url = response.json()['url']
        return audio_url
    else:
        return "Error: " + response.text

def play_audio_from_url(url):
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Download the audio file
    response = requests.get(url)
    if response.status_code == 200:
        audio_file = io.BytesIO(response.content)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
            pygame.time.Clock().tick(10)
    else:
        print("Error downloading the audio file")


cloned_voices = get_cloned_voices("2ce4d441c833453aaf3bcf1bcc2aca7b", "ynqkzbWUjISoU9q90qWtywn2gQF2")
print(cloned_voices)


# Example usage
api_key = "2ce4d441c833453aaf3bcf1bcc2aca7b"
text = "Hello, this is a test message."
voice = "s3://voice-cloning-zero-shot/d74ee38a-63d9-46b4-bc33-fc5210be3946/goku/manifest.json"
user_id = "ynqkzbWUjISoU9q90qWtywn2gQF2"

audio_url = text_to_speech(text, voice, api_key)
if audio_url.startswith("http"):
    play_audio_from_url(audio_url)
else:
    print(audio_url)