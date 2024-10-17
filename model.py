import dill as pickle

import config
from dataset import detokenize_syls, tokenize_syl

models = {
    "ngram": "tibetan_ngram_model.pkl",
}

def get_model(model_name):
    model_path = config.MODELS_PATH / models[model_name]
    with open(str(model_path), 'rb') as f:
        return pickle.load(f)

def autocomplete(text_seed, model, n):
    text_seed = tokenize_syl(text_seed)
    completion = model.generate(text_seed=text_seed, num_words=n, random_seed=19)
    if n == 1:
        return completion
    return detokenize_syls(completion)

if __name__ == "__main__":
    model = get_model("ngram")
    text_seed = "སྐད་ཡིག་"
    completion = autocomplete(text_seed, model, 5)
    print(text_seed)
    print(text_seed + completion)
