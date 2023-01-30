# Project Goal

The idea of this project is to:
- From a movie (torrent to download or perhpas url)
- Read the credits (from a timestanmp to avoid going through the full movie)
- Extract names and associated designation/job
- Save those data inside a DB
- Make the data available though UI & API

## Technical aspect

### Extraction

For the data extraction I think the best would be to use python as it seems there is alread a lot of lib that allow to extract data from move.

- Tesseract: read test from picture
- OCR: Recognize characters (included inside Tesseract)
- OpenCV: allow to manipulate picture. Can be use to pre compute picture from credits to ease text detection with Tesseract.


### Exposition

- Use sql db (which one ?)
- Use a simple UI (Vue.js perhaps)

~~~
sudo apt install tesseract-ocr
pip install pandas
pip install pytesseract
pip install pillow

pip install opencv-python
~~~

## Test

Tesseract has multiple mode for detection.

From the test picture the suitable mode are :
- 1
- 3
- 4 => Best
- 6 => Best
- 11 => Best
- 12 => Best

Each mode mathc more are less the same data, need analyze to see what is the best.
Use multiple mode to improve result.

OEM config doesn't change much so I am gonna use default mode

11 & 12 seems better because they put one thing on a line

So I will check if the line is a name or a job
If name match with previously found job
If previous job is jiberich try later or associated with dummy title

### Get pictures from video
#### Opencv


~~~bash
pip install opencv-python
export OPEN_CV=$(python -c 'import os, cv2; print(os.path.dirname(cv2.__file__))')
curl -sSL https://raw.githubusercontent.com/microsoft/python-type-stubs/main/cv2/__init__.pyi     -o $OPEN_CV/__init__.pyi
sudo apt install ffmpeg -y

~~~
sudo apt install ffmpeg



### Find names

#### spacy
~~~
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg
python -m spacy download es_core_news_sm
~~~
Using: https://nlp.stanford.edu/software/CRF-NER.shtml
https://stackoverflow.com/questions/64109483/how-to-recognize-if-string-is-human-name

Test that: https://www.geeksforgeeks.org/python-named-entity-recognition-ner-using-spacy/

spacy models: https://spacy.io/models

#### nltk
https://www.nltk.org/install.html
~~~
pip install nltk
pip install numpy
~~~

Place : nltk.download()
at the beginning of the script to download package with 'all'

### IMDb

Can check names and job on IMDb