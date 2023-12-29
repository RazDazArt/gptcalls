import elevenlabs

key = open("C:/Users/mrfla/Pictures/elevenlabskey.txt", "r").read().strip('\n')
elevenlabs.set_api_key(key)

audio = elevenlabs.generate(
    text = "hallo",
    voice = "Callum"
)

elevenlabs.play(audio)