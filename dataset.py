from botok import TokChunks
from botok.vars import CharMarkers as cm

import config


def is_syl_text(self, char_idx):
    """
    Tests whether the character at the given index is part of the cleaned syllable or not.
    """
    return (
        self.bs.base_structure[char_idx] != cm.TRANSPARENT
        and self.bs.base_structure[char_idx] != cm.SKRT_LONG_VOW
    ) or self.bs.base_structure[char_idx] == cm.SKRT_LONG_VOW

TokChunks._TokChunks__is_syl_text = is_syl_text

def tokenize_syl(text):
    return TokChunks(text, space_as_punct=True).get_syls()


def get_syls_sentences(sample=int(1e9)):
    i = 0
    do_break = False
    for fn in config.DATA_PATH.glob("*.txt"):
        print(fn)
        lines = fn.read_text().splitlines()
        for line in lines:
            if i >= sample:
                print(i)
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