from textblob import TextBlob
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import re
import sys
import os

# Local Imports
path = str(os.path.expanduser('~')) + '/git/predictEPL/config'
sys.path.append(path)
import soccer_stopwords
import english_stopwords


##########################################################
# DEFINITIONS

# Porter Stemmer & WordNet Lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

# English Stop Words
ENGLISH_STOP_WORDS = english_stopwords.STOP_WORDS
ENGLISH_STOP_WORDS_STEM = set([stemmer.stem(word) for word in list(ENGLISH_STOP_WORDS)])
ENGLISH_STOP_WORDS_LEMMA = set([lemmatizer.lemmatize(word) for word in list(ENGLISH_STOP_WORDS)])

# Soccer Stop Words
SOCCER_STOP_WORDS = soccer_stopwords.STOP_WORDS
SOCCER_STOP_WORDS_STEM = set([stemmer.stem(word) for word in list(SOCCER_STOP_WORDS)])
SOCCER_STOP_WORDS_LEMMA = set([lemmatizer.lemmatize(word) for word in list(SOCCER_STOP_WORDS)])


##########################################################


# Checking text has negation marks,
# if has, adding '_NEG' suffix
def NegationMark(text, debug=False):
    # lower case
    text = " " + text.lower() + '.'

    # adding '_NEG' suffix
    neglected_text = re.sub(
        r'''((n\'t|n\’t)|(\W(?:never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|
        shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)))\s[\w\s#-']+[(.|:|;|!|?|,|\n)$]''',
        lambda match: re.sub(r'(\s+)(\w+)', r' \2_neg', match.group(0)),
        text,
        flags=re.IGNORECASE)

    # show results
    if debug:
        print("---Txt---")
        print(text)
        print("---NEG---")
        print(neglected_text)

    # Return Suffixed text
    return neglected_text[1:-1]


# Text to Words as List
# Remove: '@, #, !, . ...'
def TextToWords(text):
    # text to words as list
    text = text.lower()
    words = TextBlob(text).words

    return words


# Text to Words
# Porter Stemmer, Not Remove Stop Words
def StemNoStops(text):
    # text to words as list
    words = Stem(text, negation=False, english_stops=False, soccer_stops=False)

    return words


# Text to Words
# Porter Stemmer, Not Remove English Stop Words
def StemNoEnglishStops(text):
    # text to words as list
    words = Stem(text, negation=False, english_stops=False)

    return words


# Text to Words
# Porter Stemmer, Not Remove Soccer Stop Words
def StemNoSoccerStops(text):
    # text to words as list
    words = Stem(text, negation=False, soccer_stops=False)

    return words


# Text to Words
# Porter Stemmer
# Remove English, Soccer Stop Words
# Not use Negation Mark
def StemNoNegation(text):
    # text to words as list
    words = Stem(text, negation=False)

    return words


# Text to Words
# Porter Stemmer & Remove English, Soccer Stopwords
def Stem(text, negation=True, english_stops=True, soccer_stops=True):
    if negation:
        # Adding '_neg' suffix to negation word clause
        text = NegationMark(text)

    # text to words as list
    words = TextToWords(text)

    # Stemming
    words = [stemmer.stem(word) for word in words]

    if english_stops:
        # Removing English STOPWORDS
        words = [word for word in words if word not in ENGLISH_STOP_WORDS_STEM]

    if soccer_stops:
        # Removing Soccer STOPWORDS
        words = [word for word in words if word not in SOCCER_STOP_WORDS_STEM]

    # Removing Twitter Links
    words = [word for word in words if not word.startswith('t.co')]

    return words


# Text to Words
# WordNet Lemmatizer & Remove English Stopwords
def Lemma(text, negation=True, english_stops=True, soccer_stops=True):
    if negation:
        # Adding '_neg' suffix to negation word clause
        text = NegationMark(text)

    # text to words as list
    words = TextToWords(text)

    # Lemmatizing
    words = [lemmatizer.lemmatize(word) for word in words]

    if english_stops:
        # Removing English STOPWORDS
        words = [word for word in words if word not in ENGLISH_STOP_WORDS_LEMMA]

    if soccer_stops:
        # Removing Soccer STOPWORDS
        words = [word for word in words if word not in SOCCER_STOP_WORDS_LEMMA]

    # Removing Twitter Links
    words = [word for word in words if not word.startswith('t.co')]

    return words


# Text to Words
# WordNet Lemmatizer, Not Remove Stop Words
def LemmaNoStops(text):
    # text to words as list
    words = Lemma(text, negation=False, english_stops=False, soccer_stops=False)

    return words


# Text to Words
# WordNet Lemmatizer, Not Remove English Stop Words
def LemmaNoEnglishStops(text):
    # text to words as list
    words = Lemma(text, negation=False, english_stops=False)

    return words


# Text to Words
# WordNet Lemmatizer, Not Remove Soccer Stop Words
def LemmaNoSoccerStops(text):
    # text to words as list
    words = Lemma(text, negation=False, soccer_stops=False)

    return words


# Text to Words
# WordNet Lemmatizer
# Remove English, Soccer Stop Words
# Not use Negation Mark
def LemmaNoNegation(text):
    # text to words as list
    words = Lemma(text, negation=False)

    return words

##########################################################


# Check Hashtag Words in Emolex
# input: 'lfc,boring,good'
# return: 'boring,good'
def HashEmolex(tags, dic_emolex_soccer):
    tags = tags.split(',')
    ret = []

    for tag in tags:
        # Check tag in Emolex
        if tag in dic_emolex_soccer and sum(list(dic_emolex_soccer[tag].values())) != 0:
            ret.append(tag)

        # Lemma Tag
        else:
            tag_lemma = WordNetLemmatizer().lemmatize(tag)
            if tag_lemma in dic_emolex_soccer and sum(list(dic_emolex_soccer[tag_lemma].values())) != 0:
                ret.append(tag_lemma)

    return ",".join(ret)


# Check Unicode Emoji in Text
# input: text
# output: emojis or ""
def EmojiText(text):

    emotion_re = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u26FF\u2700-\u27BF]',
        re.UNICODE)

    return ",".join(emotion_re.findall(text))


# Check Unicode Emoticons in Text
# input: text
# output: emoticons or ""
def EmoticonText(text):
    # This particular element is used in a couple ways, so we define it
    # with a name:
    emoticon_string = r"""
        \s+
        (?:
          [<>]?
          [:;=]                     # eyes
          [\-o\*\']?                 # optional nose
          [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
          |
          [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
          [\-o\*\']?                 # optional nose
          [:;=]                     # eyes
          [<>]?
        )"""

    emoticon_re = re.compile(emoticon_string, re.VERBOSE | re.I | re.UNICODE)

    emoticons = emoticon_re.findall(text)
    emoticons = [emoticon.strip() for emoticon in emoticons]

    return ",".join(emoticons)
