import sys
from pathlib import Path

from botok import WordTokenizer

wt = WordTokenizer()


def is_sanskrit(word):
    tokens = wt.tokenize(word)
    for token in tokens:
        if token.skrt:
            return True
    return False


def save_counter(counter, output_fn):
    with open(output_fn, "w") as f:
        for ngram, count in counter.items():
            f.write(f"{ngram} {count}\n")


def get_ngrams_counts(fn):
    with open(fn) as f:
        for line in f:
            ngram, count = line.split()
            yield (ngram, int(count))


def clean(fn):
    ngrams_counts = {}
    for ngram, count in get_ngrams_counts(fn):
        if is_sanskrit(ngram):
            continue
        ngrams_counts[ngram] = count

    save_counter(ngrams_counts, fn)


if __name__ == "__main__":
    fn = Path(sys.argv[1])
    clean(fn)
