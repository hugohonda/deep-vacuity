# -*- coding: utf-8 -*-

import re
import unicodedata
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('portuguese'))

def normalize (text):
    normalized = None
    try:
      text = unicodedata.normalize('NFKD', text)
      text = text.encode('ascii', 'ignore').decode('utf-8')
      text = re.sub('(\\d|\\W)+', ' ', text)
      text = re.sub(r'\s+', ' ', text)
      normalized = text
    except:
      normalized = ''
    return normalized

def tokenize (text):
    tokenized = None
    try:
      tokens = word_tokenize(text, language ='portuguese')
      tokenized = [w.lower() for w in tokens if w.lower() not in stop_words and len(w) > 2]
    except:
      tokenized = []
    return tokenized

def preprocess (text):
    normalized = normalize(text)
    tokenized = tokenize(normalized)
    preprocessed = ' '.join(tokenized)
    return preprocessed