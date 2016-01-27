import os
import sys
import pandas as pd


# Local Imports
path = str(os.path.expanduser('~')) + '/git/predictEPL/config'
sys.path.append(path)
import paths

sys.path.append(paths.UTILS)
import soccer_emolex
import soccer_stopwords
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

    for line in emoleRaw:
        word, category, flag = line.split()
        flag = int(flag)

        if word not in dic_emolex:
            dic_emolex[word] = {}

        dic_emolex[word][category] = flag

    print("[Emolex Dic All Words]: %s" % len(dic_emolex.keys()))

    return dic_emolex


# Create Emotion Lexicon, not include some soccer words
# words are in: soccer_emolex.py
def EmolexSoccerDic():
    # read Emotion-Lexicon.txt
    os.chdir(paths.READ_PATH_EMOLEX)
    with open("Emotion-Lexicon-Soccer.txt", 'r') as emoleRaw:
        emoleRaw = emoleRaw.readlines()

    # create emotion word dic
    dic_emolex = {}

    # Not Include Soccer Words
    ng_words = list(soccer_stopwords.STOP_WORDS)
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

            dic_emolex[word][category] = flag

    # print("[Emolex Dic's All Words]: %s" % len(dic_emolex.keys()))

    return dic_emolex


# add 2 dics values
def AddDics(dic_x, dic_y, neg_mark):
    # If word has Negation Marking: 'good_neg'
    if neg_mark:
        if dic_y['positive']:
            dic_x['negative'] += 1

        if dic_y['negative']:
            dic_x['positive'] += 1

    else:
        for key in dic_y:
            if key in dic_x:
                dic_x[key] += dic_y[key]


# input: words list
# output: emolex score as dic
def CountEmolexWords(dic_emolex, words, debug=False):
    # initialize emolex
    emolex_score = {
        'anger': 0, 'fear': 0, 'disgust': 0, 'sadness': 0,
        'surprise': 0,
        'trust': 0, 'joy': 0, 'anticipation': 0,
        'positive': 0, 'negative': 0,
    }

    # count each word
    for w_i in range(len(words)):
        word = words[w_i]

        # If word has Negation Marking: 'good_neg'
        neg_mark = False
        if word.endswith('_neg'):
            word = word[0:-4]
            neg_mark = True

        # word in emolex
        if word in dic_emolex:
            if debug:
                print(word, dic_emolex[word])
            AddDics(emolex_score, dic_emolex[word], neg_mark)

    return emolex_score


# input: SingleGames's 1 game as DF
# outpute: Emolex DF by ith_minute
# NOTE: declare dic emolex before calling method
# => dic_emolex = EmolexDic()
def CreateEmolexDF(df, dic_emolex):
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
        ith_minute = m_i + 1

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
            words = tokenizer.Lemma(tweet)

            # Count emolex words
            emolex_score = CountEmolexWords(dic_emolex, words)

            # Add values
            AddDics(emolex_score_ith_minute, emolex_score, False)

        emolex_score_ith_minute['ith_minute'] = ith_minute

        # add dic emolex to DF as row
        dfEmolex.loc[m_i] = pd.Series(emolex_score_ith_minute)

    return dfEmolex


def AppendEmolexWords(emolex_words, word, word_emolex, neg_mark):
    # If word has Negation Marking: 'good_neg'
    if neg_mark:
        if word_emolex['positive']:
            emolex_words['negative'].append(word + "_neg")
        if word_emolex['negative']:
            emolex_words['positive'].append(word + "_neg")
    else:
        for key in word_emolex.keys():
            if word_emolex[key]:
                emolex_words[key].append(word)


# Return List's Emolex words as List
def EmolexWords(dic_emolex, dic_emolex_stemmed, words):
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

        # If word has Negation Marking: 'good_neg'
        neg_mark = False
        if word.endswith('_neg'):
            word = word[0:-4]
            neg_mark = True

        # word in emolex
        if word in dic_emolex:
            if sum(list(dic_emolex[word].values())):
                AppendEmolexWords(emolex_words, word, dic_emolex[word], neg_mark)

    return emolex_words
