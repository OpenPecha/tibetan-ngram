import math
import sys
from pathlib import Path

import dill as pickle
from nltk.lm import KneserNeyInterpolated

import config


def load_model(model_path) -> KneserNeyInterpolated:
    with open(str(model_path), 'rb') as f:
        return pickle.load(f)

# Helper function to calculate log probabilities
def get_log_prob(prob):
    if prob == 0:
        return "-inf"
    return f"{math.log10(prob):.4f}"

# Helper function to calculate log backoff weights
def get_log_backoff(backoff):
    if backoff == 0:
        return "-inf"
    return f"{math.log10(backoff):.4f}"

def export(model_path):

    print("Exporting model to ARPA format...")
    trigram_model = load_model(model_path)

    # Collecting unigrams, bigrams, and trigrams
    unigrams = {}
    bigrams = {}
    trigrams = {}

    for word1 in trigram_model.vocab:
        # Extract Unigram
        prob = trigram_model.score(word1)
        backoff_weight = trigram_model.context_counts(tuple([word1])).B()
        unigrams[word1] = (get_log_prob(prob), get_log_backoff(backoff_weight))
        for word2 in trigram_model.vocab:
            # Extract Bigram
            prob = trigram_model.score(word2, [word1])
            if prob > 0:
                bigrams[(word1, word2)] = (get_log_prob(prob))
            for word3 in trigram_model.vocab:
                # Extract Trigram
                prob = trigram_model.score(word3, [word1, word2])
                if prob > 0:
                    trigrams[(word1, word2, word3)] = (get_log_prob(prob))

    # Writing to ARPA file
    export_fn = config.EXPORTS_PATH / f"{model_path.stem}.arpa"
    with open(str(export_fn), 'w') as f:
        # Write headers
        f.write("\\data\\\n")
        f.write(f"ngram 1={len(unigrams)}\n")
        f.write(f"ngram 2={len(bigrams)}\n")
        f.write(f"ngram 3={len(trigrams)}\n\n")

        # Write unigrams
        f.write("\\1-grams:\n")
        for word, (prob, backoff) in unigrams.items():
            f.write(f"{prob} {word} {backoff}\n")

        # Write bigrams
        f.write("\n\\2-grams:\n")
        for (word1, word2), prob in bigrams.items():
            f.write(f"{prob} {word1} {word2}\n")

        # Write trigrams
        f.write("\n\\3-grams:\n")
        for (word1, word2, word3), prob in trigrams.items():
            f.write(f"{prob} {word1} {word2} {word3}\n")

        # End of file
        f.write("\n\\end\\\n")

    print("LM exported to", export_fn)

if __name__ == "__main__":
    model_path = Path(sys.argv[1])
    if not model_path.exists():
        print("Model file not found")
        sys.exit(1)
    export(model_path)
