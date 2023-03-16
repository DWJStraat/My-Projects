from pytube import YouTube
from pathlib import Path
import os


def download(url, path = os.path.dirname(os.path.realpath(__file__))):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=path)
    base, ext = os.path.splitext(out_file)
    new_file = Path(f'music.mp3')
    os.rename(out_file, new_file)
    if new_file.exists():
        print(f'{yt.title} has been downloaded to {new_file}')
        return new_file
    else:
        print(f'{yt.title} has not been downloaded')
        return None

download('https://www.youtube.com/watch?v=9bZkp7q19f0')

