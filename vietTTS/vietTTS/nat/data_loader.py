from pathlib import Path

from .config import FLAGS, AcousticInput, DurationInput


def load_phonemes_set_from_lexicon_file(fn: Path):
    S = set()
    for line in open(fn, "r").readlines():
        word, phonemes = line.strip().lower().split("\t")
        phonemes = phonemes.split()
        S.update(phonemes)

    S = FLAGS.special_phonemes + sorted(list(S))
    return S