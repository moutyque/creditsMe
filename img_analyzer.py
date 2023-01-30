import nltk
import pytesseract
import spacy
from PIL import Image
from nltk import word_tokenize


# To find conf for tesseract:
# tesseract --help-oem
# tesseract --help-psm
# TODO: extract all named as set
# TODO: extract job titles => diff between file & names
# If a line contain a name it is not a job title

def process(path):
    txt = pytesseract.image_to_string(Image.open(path), lang='eng', config=f'--psm 11')
    var = [t for t in txt.split("\n") if t]
    nltk_names = [i for i in [nltk_extract_name(t) for t in var] if i]

    with open("ntlk.txt", "w") as n:
        for t in nltk_names:
            n.write(t + "\n")
    # with open("spacy.txt", "w") as n:
    #    for t in snappy_names:
    #        n.writelines(t + "\n")


def spacy_extract_name(txt):
    nlp = spacy.load('en_core_web_trf')  # This model take a lot of time
    for line in txt.split('\n'):
        doc = nlp(line)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # print(ent.text, ent.start_char, ent.end_char, ent.label_)
                return ent.text
    return ""


def nltk_extract_name(quote):
    words = word_tokenize(quote, language='spanish')
    tags = nltk.pos_tag(words)
    var = [t[0] for t in tags if t[1] == "NNP"]
    if len(var) == len(words):
        return " ".join(var)
    else:
        return ""


if __name__ == '__main__':
    process('movie1/frame_149089.jpg')
