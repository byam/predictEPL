# inside 'featx.py'
import collections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
os.chdir('/Users/Bya/git/predictEPL/MyFunctions/')
import tokenizers


def bag_of_words(words):
    return dict([(word, True) for word in words])
# Example:
# bag_of_words(['the', 'quick', 'brown', 'fox'])
# {'brown': True, 'fox': True, 'quick': True, 'the': True}


def bag_of_words_not_in_set(words, badwords):
    return bag_of_words(set(words) - set(badwords))
# Example:
# bag_of_words_not_in_set(['the', 'quick', 'brown', 'fox'], ['the'])
# {'brown': True, 'fox': True, 'quick': True}


def bag_of_non_stopwords(words, stopfile='english'):
    badwords = stopwords.words(stopfile)
    return bag_of_words_not_in_set(words, badwords)
# Example:
# bag_of_non_stopwords(['the', 'quick', 'brown', 'fox'])
# {'brown': True, 'fox': True, 'quick': True}


def label_feats_from_corpus_list(corp, feature_detector=bag_of_non_stopwords):
    label_feats = collections.defaultdict(list)
    for c in corp:
        label = c[1]
        text = c[0]
        feats = feature_detector(word_tokenize(text))
        label_feats[label].append(feats)
    return label_feats

def label_feats_from_corpus_list_bya_token(corp, feature_detector=bag_of_words):
    label_feats = collections.defaultdict(list)
    for c in corp:
        label = c[1]
        text = c[0]
        feats = feature_detector(tokenizers.bya_token(text))
        label_feats[label].append(feats)
    return label_feats


def split_label_feats(lfeats, split=0.75):
    train_feats = []
    test_feats = []
    for label, feats in lfeats.items():
        cutoff = int(len(feats) * split)
        train_feats.extend([(feat, label) for feat in feats[:cutoff]])
        test_feats.extend([(feat, label) for feat in feats[cutoff:]])
    return train_feats, test_feats
