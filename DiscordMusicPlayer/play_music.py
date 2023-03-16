from playsound import playsound
import os
from pydub import AudioSegment

def play_music():
    path = r'music.mp3'
    dst = r'music.wav'
    sound = AudioSegment.from_mp3(path)
    sound.export(dst, format="wav")
    playsound(dst)


play_music()