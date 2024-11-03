from gtts import gTTS
import os
import uuid

def generate_audio(text):
    audio = gTTS(text=text, lang='en', slow=False)
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join('uploads', filename)
    audio.save(filepath)
    return filename