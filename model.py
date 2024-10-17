import sys

import dill as pickle

import config
from dataset import detokenize_syls, tokenize_syl


def get_model(model_path):
    with open(str(model_path), 'rb') as f:
        return pickle.load(f)

def autocomplete(text_seed, model, n):
    text_seed = tokenize_syl(text_seed)
    # if len(text_seed) < n:
    #     raise ValueError("Prefix must have at least n words")
    # if len(text_seed) > n:
    #     text_seed = text_seed[-n:]

    completion = model.generate(text_seed=text_seed, num_words=n, random_seed=19)

    if n == 1:
        return completion
    return detokenize_syls(completion)

if __name__ == "__main__":
    model_path = sys.argv[1]
    model = get_model(model_path)
    text_seed = "སྐད་ཡིག་"
    completion = autocomplete(text_seed, model, 5)
    print(text_seed)
    print(text_seed + completion)
