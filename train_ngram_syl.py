import dill as pickle
from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline

import config
import dataset
from model import generate_sent

n = 3

print("Loading dataset...")
sents = list(dataset.get_syls_sentences())

print("Creating n-grams...")
train_data, padded_sents = padded_everygram_pipeline(n, sents)

print("Training...")
model = MLE(n)
model.fit(train_data, padded_sents)
print(model.vocab)

print("Generating sentence...")
print(generate_sent(model, 50, random_seed=19))

model_path = config.MODELS_PATH / "tibean_ngram_model.pkl"
with open(str(model_path), 'wb') as fout:
    pickle.dump(model, fout)

print("Model saved to", model_path)
