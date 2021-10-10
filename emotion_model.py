from math import sqrt
import copy
import pandas as pd
import numpy as np
import markovify
import nltk
import spacy
import re
import nltk
import warnings
import json
import pymorphy2
import copy
import gensim
import gensim.downloader as download_api
from gensim.models import Word2Vec
from pymystem3 import Mystem
from string import punctuation
from pprint import pprint
from summa.keywords import keywords
from nltk.corpus import gutenberg
from nltk import download, sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer

nltk.download('gutenberg')
nltk.download('stopwords')
nltk.download("punkt")
nltk.download('stopwords')
warnings.filterwarnings('ignore')
russian_model = download_api.load('word2vec-ruscorpora-300')

emotion_list = ['отвращение', 'страх', 'злость', 'стыд', 'радость', 'горе', 'волнение', 'грусть']
useful_pos_list = ['INFN', 'NOUN', 'ADJF', 'ADJS', 'VERB', 'ADVB']


def tag(word):
    morph = pymorphy2.MorphAnalyzer(lang='ru')

    w = morph.parse(word)[0].tag.POS
    tg = copy.deepcopy(w)
    if w == 'ADJF' or w == 'ADJS':
        w = 'ADJ'
    elif w == 'ADVB':
        w = 'ADV'
    elif w == 'INFN':
        w = 'VERB'
    tagged = str(word) + '_' + str(w)

    return tagged


# please pass text as copy of python string
def preprocess_phrase(phrase):
    morph = pymorphy2.MorphAnalyzer(lang='ru')

    phrase = phrase.lower()
    phrase = re.sub(r'[^\w\s]', '', phrase)

    phrase_array = phrase.split()
    useful_phrases = []
    for i in phrase_array:
        cur_word = morph.parse(i)[0].normalized
        if cur_word.tag.POS in useful_pos_list:
            useful_phrases.append(cur_word.word)
    return useful_phrases


def get_emotion_array(phrase):
    contest = preprocess_phrase(phrase)

    if len(contest) == 0:
        print("Недостаточно слов для анализа")
        return []

    emotion_rank = []
    for emotion in emotion_list:
        cur_vec = []
        counter = 0
        for word in contest:
            try:
                score = russian_model.similarity(tag(word), tag(emotion))
                cur_vec.append(score ** 2.5)
                counter += 1
            except:
                cur_vec.append(0.0)

        if counter == 0:
            print("Недостаточно слов для анализа")
            return []
        cur_vec.sort(reverse=True)
        cur_vec = cur_vec[:max(3, len(contest))]
        cur_score = 0.0
        for scr in cur_vec:
            cur_score += scr
        cur_score /= len(cur_vec)
        emotion_rank.append(cur_score)
    max_score = 0.0
    for scr in emotion_rank:
        max_score = max(scr, max_score)
    for i in range(len(emotion_rank)):
        emotion_rank[i] = emotion_rank[i] / max_score
    ans = []
    for i in range(len(emotion_list)):
        ans.append((emotion_list[i], emotion_rank[i]))
    return ans
