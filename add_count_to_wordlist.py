import sys


def build_counter(fn):
    counter = {}
    with open(fn, "r") as f:
        for line in f:
            word, count = line.strip().split()
            counter[word] = int(count)
    return counter


wordlist_counter = {}


def get_wordlist(fn):
    with open(fn, "r") as f:
        return f.read().splitlines()


def save_counter(counter, fn):
    with open(fn, "w") as f:
        for word, count in counter.items():
            f.write(f"{word} {count}\n")


def process(count_fn, wordlist_fn):
    counter = build_counter(count_fn)
    for word in get_wordlist(wordlist_fn):
        if word in counter:
            wordlist_counter[word] = counter[word]
        else:
            wordlist_counter[word] = 0

    save_counter(wordlist_counter, "data/wordlist_counter.txt")


if __name__ == "__main__":
    count_fn = sys.argv[1]
    wordlist_fn = sys.argv[2]

    process(count_fn, wordlist_fn)
