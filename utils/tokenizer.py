from textblob import TextBlob
from nltk.corpus import stopwords

import sys
sys.path.append("/Users/Bya/git/predictEPL/config/")
import soccer_stopwords


def Lemma(text, stops=True):
    text = text.lower()
    words = TextBlob(text).words

    # Lemma
    words = [word.lemma for word in words]

    if stops:
        # Removing STOP WORDS
        english_stops = set(stopwords.words('english'))
        words = [word for word in words if word not in english_stops]

    return words


# Removing Soccer Stop Words
def TweetLemmaSoccer(text, stops=True):
    text = text.lower()
    words = TextBlob(text).words

    # Lemma
    words = [word.lemma for word in words]

    if stops:
        # Removing STOP WORDS(includes Soccer stops)
        english_stops = set(stopwords.words('english'))
        english_stops_soccer = english_stops | soccer_stopwords.STOP_WORDS
        words = [word for word in words if word not in english_stops_soccer]

    # Removing Twitter Links
    words = [word for word in words if not word.startswith('t.co')]

    return words
