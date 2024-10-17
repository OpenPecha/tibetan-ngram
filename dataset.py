import config

tsek = "་"
shed = "།"

def tokenize_syl(text):
    segments = text.split(shed)
    syls = []
    for segment in segments:
        segment = segment.strip()
        if not segment or segment == shed:
            continue
        syls.extend([s+tsek for s in segment.split(tsek)])
    return syls


def get_syls_sentences(n_samples=None):
    n_samples = n_samples or int('inf')
    i = 0
    do_break = False
    for fn in config.DATA_PATH.glob("*.txt"):
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

if __name__ == "__main__":
    text = "༄༅། ། འཕགས་པ་སཱ་ལུ་ལྗང་པ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོའི་རྒྱ་ཆེར་བཤད་པ།༄༅༅། ། རྒྱ་གར་སྐད་དུ། ཨཱརྱ་ཤཱ་ལི་སྟམྦ་ཀ་མ་ཧཱ་ཡཱ་ན་སཱུ་ཏྲ་ཊཱི་ཀཱ།"
    syls = tokenize_syl(text)
    print(syls)