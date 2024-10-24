import sys


def get_ngrams(fn):
    with open(fn) as f:
        for line in f:
            ngram, count = line.split()
            yield (ngram, int(count))


def save_ngrams(ngrams, fn):
    with open(fn, "w") as f:
        for ngram, count in ngrams:
            f.write(f"{ngram} {count}\n")


def main():
    fn = sys.argv[1]
    ngrams = list(get_ngrams(fn))
    ngrams.sort(key=lambda x: x[1], reverse=True)
    save_ngrams(ngrams, fn)


if __name__ == "__main__":
    main()
