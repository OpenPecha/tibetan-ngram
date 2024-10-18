import sys
from pathlib import Path

modified_ngrams = []
special_chars = ["<s>", "</s>", "<unk>"]

def clean_ngram(ngram):
    modified = False
    for s_char in special_chars:
        if s_char in ngram:
            ngram = ngram.replace(s_char, "")
            modified = True
    if modified:
        return ngram, True
    return ngram, False

def save_counter(counter, output_fn):
    with open(output_fn, "w") as f:
        for ngram, count in counter.items(): 
            f.write(f"{ngram} {count}\n")


def clean(fn):
    counter = {}
    # find ngrams that need to be merged
    for line in fn.read_text().splitlines():
        splits = line.strip().split()
        if len(splits) > 2: continue
        ngram, count = splits
        ngram, is_modified = clean_ngram(ngram)
        if not ngram: continue
        if is_modified:
            modified_ngrams.append(ngram)
        else:
            counter[ngram] = int(count)

    # update count
    for m_ngram in modified_ngrams:
        if m_ngram in counter:
            counter[m_ngram] += 1
        else:
            counter[m_ngram] = 1

    output_fn = fn.parent / f"{fn.stem}_cleaned.txt"
    save_counter(counter, output_fn)


if __name__ == "__main__":
    fn = Path(sys.argv[1])
    clean(fn)
