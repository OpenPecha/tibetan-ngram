import json
import re
from pathlib import Path


def tokenize_syl(text):
    return re.findall(r"[^་]+་?", text)


def main():
    words = set()
    path = Path("data/dict")
    for fn in path.iterdir():
        print(fn)
        data = json.loads(fn.read_text())
        for row in data["rows"]:
            word = row[0]
            try:
                syls = tokenize_syl(word)
            except:
                continue
            if len(syls) > 3:
                continue
            words.add(row[0])

    output_path = Path("data/dict.txt")
    output_path.write_text("\n".join([w for w in words if w]))
    print(output_path)


if __name__ == "__main__":
    main()
