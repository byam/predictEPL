from textblob import TextBlob
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

import re
import sys

sys.path.append("/Users/Bya/git/predictEPL/config/")
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


# Text to Words as List
def TextToWords(text):
    # text to words as list
    text = text.lower()
    words = TextBlob(text).words

    return words


# Text to Words
# Porter Stemmer, Not Remove Stop Words
def StemNoStops(text):
    # text to words as list
    words = Stem(text, english_stops=False, soccer_stops=False)

    return words


# Text to Words
# Porter Stemmer, Not Remove English Stop Words
def StemNoEnglishStops(text):
    # text to words as list
    words = Stem(text, english_stops=False)

    return words


# Text to Words
# Porter Stemmer, Not Remove Soccer Stop Words
def StemNoSoccerStops(text):
    # text to words as list
    words = Stem(text, soccer_stops=False)

    return words


# Text to Words
# Porter Stemmer & Remove English, Soccer Stopwords
def Stem(text, english_stops=True, soccer_stops=True):
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
def Lemma(text, english_stops=True, soccer_stops=True):
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
    words = Lemma(text, english_stops=False, soccer_stops=False)

    return words


# Text to Words
# WordNet Lemmatizer, Not Remove English Stop Words
def LemmaNoEnglishStops(text):
    # text to words as list
    words = Lemma(text, english_stops=False)

    return words


# Text to Words
# WordNet Lemmatizer, Not Remove Soccer Stop Words
def LemmaNoSoccerStops(text):
    # text to words as list
    words = Lemma(text, soccer_stops=False)

    return words

##########################################################


# Removing Soccer Stop Words
def TweetLemmaSoccer(text, stops=True):
    text = text.lower()
    words = TextBlob(text).words

    # Lemma
    words = [word.lemma for word in words]

    if stops:
        # Removing STOP WORDS(includes Soccer stops)
        english_stops = ENGLISH_STOP_WORDS
        english_stops_soccer = english_stops | soccer_stopwords.STOP_WORDS
        words = [word for word in words if word not in english_stops_soccer]

    # Removing Twitter Links
    words = [word for word in words if not word.startswith('t.co')]

    return words


def TweetLemmaSoccerNeg(text, stops=True):
    # Checking negation words: 'not good'
    # if found add suffix: 'not good_NEG'
    neglect_text = NegationMark(text)
    if neglect_text is not None:
        text = neglect_text

    # Text to Words
    text = text.lower()
    words = TextBlob(text).words

    # Lemma
    words_lemma = []
    for word in words:
        # if word has negation mark: bad_neg, good_neg
        if word.endswith('_neg'):
            word = word[0:-4]
            word = TextBlob(word).words[0].lemma + "_neg"

        # regular words
        else:
            word = word.lemma

        words_lemma.append(word)

    if stops:
        # Removing STOP WORDS(includes Soccer stops)
        english_stops = ENGLISH_STOP_WORDS
        english_stops_soccer = english_stops | soccer_stopwords.STOP_WORDS

        words_lemma = [word for word in words_lemma if word not in english_stops_soccer]

    # Removing Twitter Links
    words_lemma = [word for word in words_lemma if not word.startswith('t.co')]

    return words_lemma


def TweetLemmaSoccerEmolex(text, stops=True):
    # Checking negation words: 'not good'
    # if found add suffix: 'not good_NEG'
    neglect_text = NegationMark(text)
    if neglect_text is not None:
        text = neglect_text

    text = text.lower()
    words = TextBlob(text).words

    words_not_lemma = words

    # Lemma
    words_lemma = []
    for word in words:
        # if word has negation mark: bad_neg, good_neg
        if word.endswith('_neg'):
            word = word[0:-4]
            word = TextBlob(word).words[0].lemma + "_neg"

        # regular words
        else:
            word = word.lemma

        words_lemma.append(word)

    if stops:
        # Removing STOP WORDS(includes Soccer stops)
        english_stops = ENGLISH_STOP_WORDS
        english_stops_soccer = english_stops | soccer_stopwords.STOP_WORDS

        words_lemma = [word for word in words_lemma if word not in english_stops_soccer]
        words_not_lemma = [word for word in words_not_lemma if word not in english_stops_soccer]

    # Removing Twitter Links
    words_lemma = [word for word in words_lemma if not word.startswith('t.co')]
    words_not_lemma = [word for word in words_not_lemma if not word.startswith('t.co')]

    return words_not_lemma, words_lemma


# Checking text has negation marks,
# if has, adding '_NEG' suffix
def NegationMark(text, debug=False):
    # lower case
    text = text.lower() + '.'

    # adding '_NEG' suffix
    neglected_text = re.sub(
        r'''((n\'t|n\’t)|(\s+(?:never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|
        shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)))\s[\w\s#-']+[(.|:|;|!|?|,|\n)$]''',
        lambda match: re.sub(r'(\s+)(\w+)', r' \2_NEG', match.group(0)),
        text,
        flags=re.IGNORECASE)

    # show results
    if debug:
        print("---Txt---")
        print(text)
        print("---NEG---")
        print(neglected_text)

    # no negation in text
    if '_NEG' not in neglected_text:
        return None

    # Return Suffixed text
    return neglected_text


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
