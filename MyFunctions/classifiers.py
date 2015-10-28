import os
os.chdir('/Users/Bya/git/predictEPL/MyFunctions/')
import tokenizers
import senti_word_net
import featx
import replacers

from nltk.corpus import stopwords

import pickle
with open('/Users/Bya/nltk_data/taggers/treebank_aubt.pickle', 'rb') as f:
    tagger_aubt = pickle.load(f)

from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer


with open("/Users/Bya/git/predictEPL/NLTK/NLTK_TUTORIAL/pickled_algos/naiveBayes_for_short_reviews_NEW.pickle", "rb") as saved_classifier_f:
    nb_classifier = pickle.load(saved_classifier_f)


def cleanHash(word):
    if word[0] == '#':
        return '#'
    elif word[0] == '@':
        return '@'
    elif word[0:4] == 'http':
        return 'http'
    else:
        return word


def nb_swn(tweet):
    # can't -> cannot, bya's -> bya is
    replacer = replacers.RegexpReplacer()
    tweet = replacer.replace(tweet)

    # Tweet tokenizer
    words = TweetTokenizer().tokenize(tweet)

    # defining stopwords
    english_stops = set(stopwords.words('english'))
    english_stops_added = english_stops | {'.', ',', '!', ':', ';', '#', '?', 'RT', '-', '@', 'rt'}
    words = [word.lower() for word in words if word.lower() not in english_stops_added]

    # Lemmatizer
    lemmatizer = WordNetLemmatizer()
    words = map(lambda word: lemmatizer.lemmatize(word), words)

    # words = map(lambda word: cleanHash(word), words)
    words = [cleanHash(word) for word in words]

    # defining stopwords
    english_stops_added = {'.', ',', '!', ':', ';', '#', '?', 'RT', '-', '@', 'rt'}
    words = [word.lower() for word in words if word.lower() not in english_stops_added]


    # Naive Bayes
    probs = nb_classifier.prob_classify(featx.bag_of_words(words))

    senti_nb = probs.max()
    senti_nb_pos = probs.prob('pos')
    senti_nb_neg = probs.prob('neg')


    # SentiWordNet
    taggedAUBTwords = tagger_aubt.tag(words)
    wordsWNtag = list(map(lambda word: senti_word_net.wordnet_sanitize(word), taggedAUBTwords))
    senti_swn_pos, senti_swn_neg, senti_swn_obj = senti_word_net.pos_neg_score_words(wordsWNtag)

    if senti_swn_pos > senti_swn_neg:
        senti_swn = 'pos'
    else:
        senti_swn = 'neg'

    return senti_nb, senti_nb_pos, senti_nb_neg, senti_swn, senti_swn_pos, senti_swn_neg, senti_swn_obj


def createTuples(weekGames):
    weekGamesTuples = []
    for i in range(len(weekGames)):
        if i % 2 == 0:
            weekGamesTuples.append((weekGames[i], weekGames[i+1]))
    return weekGamesTuples


class Teams(object):
    def __init__(self):
        self.Bournemouth = 'Bournemouth'
        self.Arsenal = 'Arsenal'
        self.Villa = 'Villa'
        self.Chelsea = 'Chelsea'
        self.Crystal = 'Crystal'
        self.Everton = 'Everton'
        self.Leicester = 'Leicester'
        self.Liverpool = 'Liverpool'
        self.City = 'City'
        self.United = 'United'
        self.Newcastle = 'Newcastle'
        self.Norwich = 'Norwich'
        self.Southampton = 'Southampton'
        self.Stoke = 'Stoke'
        self.Sunderland = 'Sunderland'
        self.Swansea = 'Swansea'
        self.Tottenham = 'Tottenham'
        self.Watford = 'Watford'
        self.WestBromwich = 'WestBromwich'
        self.WestHam = 'WestHam'
