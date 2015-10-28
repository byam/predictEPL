import os
os.chdir('/Users/Bya/git/predictEPL/MyFunctions/')

import replacers
import featx
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet


def bya_token(text, stopWords=False, wordNet=False):
    # can't -> cannot, bya's -> bya is
    replacer = replacers.RegexpReplacer()
    text = replacer.replace(text)
    # print(text)

    # "Hello-World. \n Bya is cannot do \t this."
    # ['Hello-World', 'Bya', 'is', 'cannot', 'do', 'this']
    tokenizer = RegexpTokenizer("[\w']+")
    words = tokenizer.tokenize(text)
    # print(words)

    # 'cooking' -> 'cook'
    # stemmer = PorterStemmer()
    # words = map(lambda word: stemmer.stem(word), words)

    # Lemmatizer
    lemmatizer = WordNetLemmatizer()
    words = list(map(lambda word: lemmatizer.lemmatize(word), words))
    # print(words)

    if stopWords:
        # defining stopwords
        english_stops = set(stopwords.words('english'))
        english_stops_added = english_stops | {'.'}
        words = [word.lower() for word in words if word.lower() not in english_stops_added]
        # print(words)

    if wordNet:
        # only use WordNet words
        words = [word for word in words if len(wordnet.synsets(word))]
        # print(words)

    return words
