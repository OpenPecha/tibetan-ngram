import re
import sys

import config

tsek = "་"
shed = "།"

def tokenize_syl(text):
    segments = text.split(shed)
    print(segments)
    syls = []
    for segment in segments:
        segment = segment.strip()
        if not segment or segment == shed:
            continue
        syls.extend(re.findall(r'[^་]+་?', segment))
    return syls


def get_syls_sentences(n_samples=None):
    n_samples = n_samples or float('inf')
    i = 0
    do_break = False
    for fn in config.DATA_PATH.glob("*.txt"):
        print(fn)
        lines = fn.read_text().splitlines()
        for line in lines:
            if i >= n_samples:
                do_break = True
                break
            yield tokenize_syl(line)
            i += 1
        if do_break:
            break

def detokenize_syls(syls):
    result = ""
    for syl in syls:
        if not syl.endswith("་"):
            syl += " "
        result += syl
    return result

def create_dataset(n_samples=None, name="dataset.txt"):
    dataset_fn = config.DATA_PATH / name

    with open(str(dataset_fn), 'w') as f:
        for syls in get_syls_sentences(n_samples=n_samples):
            f.write(" ".join(syls))
            f.write("\n")

    print("Dataset created at", dataset_fn)

if __name__ == "__main__":
    n_samples = sys.argv[1] if len(sys.argv) > 1 else None
    create_dataset(n_samples=n_samples)
