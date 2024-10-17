
import sys

import dill as pickle
from nltk.lm import KneserNeyInterpolated
from nltk.lm.preprocessing import padded_everygram_pipeline

import config
import dataset


def save_model(model, model_path):
    with open(str(model_path), 'wb') as fout:
        pickle.dump(model, fout)
    print("Model saved to", model_path)

def train(model_path, n_samples=None):
    n = 3
    print("Loading dataset...")
    sents = dataset.get_syls_sentences(n_samples=n_samples)

    print("Creating n-grams...")
    train_data, padded_sents = padded_everygram_pipeline(n, sents)

    print("Training...")
    trigram_model = KneserNeyInterpolated(3)
    trigram_model.fit(train_data, padded_sents)
    print("Vocab size", len(trigram_model.vocab))

    save_model(trigram_model, model_path)

if __name__ == "__main__":
    model_name = sys.argv[1]
    model_path = config.MODELS_PATH / f"{model_name}_trigram_model.pkl"
    train(model_path)