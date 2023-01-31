import cv2
import nltk
import numpy as np
import pytesseract
import spacy
from PIL import Image
from nltk import word_tokenize
from typing import Dict, Set

from paddleocr import PaddleOCR

# To find conf for tesseract:
# tesseract --help-oem
# tesseract --help-psm
# TODO: extract all named as set
# TODO: extract job titles => diff between file & names
# If a line contain a name it is not a job title

name_job = dict()


def process(path, psm=4):
    txt = pytesseract.image_to_string(Image.open(path), lang='eng', config=f'--psm {psm}')
    lines = [t for t in txt.split("\n") if t]
    with open(f"process{psm}.txt", "w") as f:
        f.write(txt)
    current_job = ""
    for line in lines:
        name = nltk_extract_name(line)
        if name and current_job:
            if name in name_job:
                name_job[name].add(current_job)
            else:
                name_job[name] = set()
                name_job[name].add(current_job)
        else:
            current_job = line
    return name_job


def nltk_extract_name(quote):
    words = word_tokenize(quote, language='english')
    tags = nltk.pos_tag(words)
    var = [t[0] for t in tags if t[1] == "NNP"]
    if len(var) == len(words):
        return " ".join(var)
    else:
        return ""


def extract_with_binary(path, psm=11):
    # Load the image
    img = cv2.imread(path)

    # Convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get the binary mask
    msk = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([179, 255, 154]))

    # Extract
    krn = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dlt = cv2.dilate(msk, krn, iterations=5)
    res = 255 - cv2.bitwise_and(dlt, msk)

    # OCR
    txt = pytesseract.image_to_string(res, config=f"--psm {psm}")
    with open(f"extract_with_binary{psm}.txt", "w") as f:
        f.write(txt)


def paddleocr(path):
    ocr = PaddleOCR(lang='en')  # need to run only once to load model into memory
    result = ocr.ocr(path, det=False, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)


def ocr(path, psm=11):
    # Grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph open to remove noise and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening

    # Perform text extraction
    data = pytesseract.image_to_string(invert, lang='eng', config=f'--psm {psm}')
    with open(f"ocr{psm}.txt", "w") as f:
        f.write(data)


if __name__ == '__main__':
    #print(pytesseract.image_to_string(cv2.imread('frames/frame_144889.jpg')))
    #process('frames/frame_144889.jpg', 1)
    #extract_with_binary('frames/frame_144889.jpg', 1)
    #ocr('frames/frame_144889.jpg', 1)
    paddleocr('frames/frame_144889.jpg')
