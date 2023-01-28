import whisper
import os

model = whisper.load_model("base")

yt = "https://www.youtube.com/watch?v=pT7vRUGeEtA"

# os.system("youtube-dl --extract-audio --audio-format mp3 {} --output temp.mp3".format(yt))

result = model.transcribe('temp.mp3')
print(result["text"].strip())