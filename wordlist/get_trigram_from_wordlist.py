import re
from pathlib import Path


def tokenize_syl(text):
    return re.findall(r"[^་]+་?", text)


wordlist_path = Path("data/word_list.txt")
trigrams_fn = Path("data/dict_trigram.txt")

trigrams = {w.strip() for w in trigrams_fn.read_text().splitlines()}
print(len(trigrams))

for word in wordlist_path.read_text().splitlines():
    syls = tokenize_syl(word)
    if len(syls) > 3:
        continue
    trigrams.add(word)

print(len(trigrams))

output_fn = Path("data/trigram_final.txt")
output_fn.write_text("\n".join([w for w in trigrams if w]))
print(output_fn)
