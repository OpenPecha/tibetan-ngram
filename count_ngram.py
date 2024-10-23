import sys
from collections import Counter

from nltk.util import everygrams

import config
import dataset

n = 3


def get_wordlist(fn):
    with open(fn, "r") as f:
        for word in f.read().splitlines():
            yield word.strip()


def save_counter(counter, path):
    with open(path, "w") as f:
        for word, count in counter.items():
            f.write(f"{word} {count}\n")
    print("Counter saved to", path)


def start_counting(counter_path, n_samples=None):
    counter = Counter()
    wordlist = set(get_wordlist(wordlist_path))
    for sent in dataset.get_syls_sentences(n_samples):
        for ngram in everygrams(sent, max_len=n):
            word = "".join(ngram)
            if not word.endswith("་"):
                word += "་"
            if word not in wordlist:
                continue
            counter[word] += 1

    save_counter(counter, counter_path)


if __name__ == "__main__":
    counter_name = sys.argv[1]
    wordlist_path = sys.argv[2]
    n_samples = int(sys.argv[3]) if len(sys.argv) > 3 else None
    counter_path = config.MODELS_PATH / f"{counter_name}_counts.txt"
    start_counting(counter_path, n_samples=n_samples)
