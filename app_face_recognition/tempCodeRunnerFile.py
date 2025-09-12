from pydub import AudioSegment

# convert success.mp3 → success.wav
sound = AudioSegment.from_mp3("./resources/sound/success.mp3")
sound.export("./resources/sound/success.wav", format="wav")

# convert fail.mp3 → fail.wav
sound = AudioSegment.from_mp3("./resources/sound/fail.mp3")
sound.export("./resources/sound/fail.wav", format="wav")