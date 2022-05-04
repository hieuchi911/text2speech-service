import re
import unicodedata
from argparse import ArgumentParser
from pathlib import Path
import time

import soundfile as sf

from .hifigan.mel2wave import mel2wave
from .nat.config import FLAGS
from .nat.text2mel import text2mel

def nat_normalize_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.lower().strip()
    sp = FLAGS.special_phonemes[FLAGS.sp_index]
    text = re.sub(r"[\n.,:]+", f" {sp} ", text)
    text = text.replace('"', " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[.,:;?!]+", f" {sp} ", text)
    text = re.sub("[ ]+", " ", text)
    text = re.sub(f"( {sp}+)+ ", f" {sp} ", text)
    return text.strip()

if __name__=='__main__':
    parser = ArgumentParser()
    parser.add_argument("--text", type=str)
    parser.add_argument("--output", default="clip.wav", type=Path)
    parser.add_argument("--sample-rate", default=16000, type=int)
    parser.add_argument("--silence-duration", default=-1, type=float)
    parser.add_argument("--lexicon-file", default=None)
    args = parser.parse_args()

    text = nat_normalize_text(args.text)
    print("Normalized text input:", text)
    start = time.time()
    mel = text2mel(text, args.lexicon_file, args.silence_duration)
    end = time.time()
    print("\ntext2mel took: ", end - start)

    start = time.time()
    wave = mel2wave(mel)
    end = time.time()
    print("\nmel2wave took: ", end - start)

    print("writing output to file", args.output)
    sf.write(str(args.output), wave, samplerate=args.sample_rate)
