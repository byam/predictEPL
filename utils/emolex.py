import os
import sys
import pandas as pd
from nltk.stem import PorterStemmer


sys.path.append('/Users/Bya/git/predictEPL/config/')
sys.path.append('/Users/Bya/git/predictEPL/utils/')

import paths
import soccer_emolex
import useful_methods
import tokenizer


# Create Emotion Lexicon Dictionary
def EmolexDic():
    # read Emotion-Lexicon.txt
    os.chdir(paths.READ_PATH_EMOLEX)
    with open("Emotion-Lexicon.txt", 'r') as emoleRaw:
        emoleRaw = emoleRaw.readlines()

    # create emotion word dic
    dic_emolex = {}
    dic_emolex_stemmed = {}

    for line in emoleRaw:
        word, category, flag = line.split()
        flag = int(flag)

        if word not in dic_emolex:
            dic_emolex[word] = {}
            dic_emolex_stemmed[PorterStemmer().stem(word)] = {}

        dic_emolex[word][category] = flag
        dic_emolex_stemmed[PorterStemmer().stem(word)][category] = flag
        dic_emolex_stemmed[PorterStemmer().stem(word)]["_original_word"] = word

    print("All Words: %s" % len(dic_emolex.keys()))

    return dic_emolex, dic_emolex_stemmed


# Create Emotion Lexicon, not include some soccer words
# words are in: soccer_emolex.py
def EmolexSoccerDic():
    # read Emotion-Lexicon.txt
    os.chdir(paths.READ_PATH_EMOLEX)
    with open("Emotion-Lexicon-Soccer.txt", 'r') as emoleRaw:
        emoleRaw = emoleRaw.readlines()

    # create emotion word dic
    dic_emolex = {}
    dic_emolex_stemmed = {}

    # Not Include Soccer Words
    ng_words = []
    for words in soccer_emolex.NOT_INCLUDE.values():
        if len(words):
            for word in words:
                ng_words.append(word)

    for line in emoleRaw:
        word, category, flag = line.split()

        # exclude soccer words
        if word not in ng_words:
            flag = int(flag)

            if word not in dic_emolex:
                dic_emolex[word] = {}
                dic_emolex_stemmed[PorterStemmer().stem(word)] = {}

            dic_emolex[word][category] = flag
            dic_emolex_stemmed[PorterStemmer().stem(word)][category] = flag
            dic_emolex_stemmed[PorterStemmer().stem(word)]["_original_word"] = word

    print("All Words: %s" % len(dic_emolex.keys()))

    return dic_emolex, dic_emolex_stemmed


# add 2 dics values
def AddDics(dic_x, dic_y):
    for key in dic_y:
        if key in dic_x:
            dic_x[key] += dic_y[key]


# inpute: words list
# outpute: emolex score as dic
def CountEmolexWords(dic_emolex, dic_emolex_stemmed,
                     words, words_stemmed, debug=False):
    # initialize emolex
    emolex_score = {
        'anger': 0, 'fear': 0, 'disgust': 0, 'sadness': 0,
        'surprise': 0,
        'trust': 0, 'joy': 0, 'anticipation': 0,
        'positive': 0, 'negative': 0,
    }

    # count each word
    for w_i in range(len(words)):
        # word in emolex
        if words[w_i] in dic_emolex:
            if debug:
                print(words[w_i], dic_emolex[words[w_i]])
            AddDics(emolex_score, dic_emolex[words[w_i]])

    # count each word
    for w_i in range(len(words_stemmed)):
        # stemmed word in emolex
        if words_stemmed[w_i] in dic_emolex:
            if debug:
                print(words_stemmed[w_i], dic_emolex[words_stemmed[w_i]])
            AddDics(emolex_score, dic_emolex[words_stemmed[w_i]])

    return emolex_score


# input: SingleGames's 1 game as DF
# outpute: Emolex DF by ith_minute
# NOTE: declare dic emolex before calling method
# => dic_emolex, dic_emolex_stemmed = EmolexDic()
def CreateEmolexDF(df, dic_emolex, dic_emolex_stemmed):
    columns = ['ith_minute',
               'anger', 'fear', 'disgust', 'sadness',
               'surprise',
               'trust', 'joy', 'anticipation',
               'positive', 'negative']

    # Create DF
    dfEmolex = pd.DataFrame(columns=columns)

    # Add emolex dic by minute
    for m_i in range(110):
        # set minute
        ith_minute = str(m_i + 1)

        # ith_minute's tweet list
        tweets = list(df[df['ith_minute'] == ith_minute]['text'])

        # initialize emolex
        emolex_score_ith_minute = {
            'anger': 0, 'fear': 0, 'disgust': 0, 'sadness': 0,
            'surprise': 0,
            'trust': 0, 'joy': 0, 'anticipation': 0,
            'positive': 0, 'negative': 0,
        }

        # PreprocessingTweet & Counting Emolex Score
        for tweet in tweets:
            words, words_stemmed = tokenizer.TweetLemmaSoccerEmolex(tweet)

            # Count emolex words
            emolex_score = CountEmolexWords(dic_emolex, dic_emolex_stemmed, words, words_stemmed)

            # Add values
            AddDics(emolex_score_ith_minute, emolex_score)

        emolex_score_ith_minute['ith_minute'] = ith_minute

        # add dic emolex to DF as row
        dfEmolex.loc[m_i] = pd.Series(emolex_score_ith_minute)

    return dfEmolex


def AppendEmolexWords(emolex_words, word, word_emolex):
    for key in word_emolex.keys():
        if word_emolex[key]:
            emolex_words[key].append(word)


# Return List's Emolex words as List
def EmolexWords(dic_emolex, dic_emolex_stemmed,
                words, words_stemmed):
    # initialize emolex
    emolex_words = {
        'anger': [], 'fear': [], 'disgust': [], 'sadness': [],
        'surprise': [],
        'trust': [], 'joy': [], 'anticipation': [],
        'positive': [], 'negative': [],
    }

    # count each word
    for w_i in range(len(words)):
        word = words[w_i]
        word_stem = words_stemmed[w_i]

        # word in emolex
        if word in dic_emolex:
            if sum(list(dic_emolex[word].values())):
                AppendEmolexWords(emolex_words, word, dic_emolex[word])

        # word_stem in emolex
        elif word_stem in dic_emolex:
            if sum(list(dic_emolex[word_stem].values())):
                AppendEmolexWords(emolex_words, word_stem, dic_emolex[word_stem])

    return emolex_words
