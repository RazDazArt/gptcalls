import elevenlabs

key = open("C:/Users/mrfla/Pictures/elevenlabskey.txt", "r").read().strip('\n')
elevenlabs.set_api_key(key)

audio = elevenlabs.generate(
    text = "sukuna. what you failed to realize. was somthing that you decided to overlook in your heart. but despite your attempts to ignore it, you have to realize it sooner or later. that the truth is. the jujutsu kaisen really was. the friends. we made along the way. now come on buddy, i'll be your friend. theres still time to fix all this and set things right. dattebayo, watashi wa あなたは私の特別です、ドゥー・ドゥット・トゥ・ルーウー・ドゥン・ドゥン・ダン... ジブンを世界さえも変えてしまおうな 瞬間はいつもすぐそばに...",
    voice = "Callum" 
)

elevenlabs.play(audio)