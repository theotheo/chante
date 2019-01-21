import argparse
import logging
import re
import unicodedata
from pathlib import Path

from gtts import gTTS, lang
from pydub import AudioSegment

langs = lang.tts_langs()

# https://stackoverflow.com/a/295466/1248256
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)

    return value

def tts_in_all_languages(word):
    word = slugify(word)
    p = Path(word)
    p.mkdir(exist_ok=True)

    for code, name in langs.items():
        logging.debug(code, name)
        name = slugify(name)

        tts = gTTS(name, lang='en')
        fn = str(p.joinpath('{}___{}.mp3'.format(code, name)))
        tts.save(fn)

        tts = gTTS(word, lang=code, slow=True)
        fn = str(p.joinpath('{}_{}.mp3'.format(code, word)))
        tts.save(fn)


    playlist = AudioSegment.silent(duration=500) 
    for fname in sorted(list(p.glob('*.mp3'))):
        playlist += AudioSegment.from_mp3(str(fname))
        playlist += AudioSegment.silent(duration=200) 


    with open('{}.mp3'.format(word), 'wb') as f:
        playlist.export(f, format='mp3')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Text in all Google TTS languages')
    parser.add_argument('text', help='a text')

    args = parser.parse_args()

    tts_in_all_languages(args.text)
