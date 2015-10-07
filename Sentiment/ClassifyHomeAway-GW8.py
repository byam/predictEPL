
# coding: utf-8

# In[1]:

import os
import csv
from pprint import pprint
import pandas as pd
import pickle
import collections


# In[2]:

hashPath = "/Users/Bya/git/EPLdata/"
dataPath = "/Users/Bya/Dropbox/Research/datas/"
modelPath = "/Users/Bya/Dropbox/Research/datas/Pickles/Models/"
tokenizerPath = "/Users/Bya/git/predictEPL/Tokenizers/"

os.chdir(tokenizerPath)
import sentiment_aware as sa
os.chdir(hashPath)
from config import Hashtags


# In[3]:

model = "MovieShortReview"

# read saved classifier
saved_classifier_f = open(modelPath + model + "/naiveBayes.pickle", "rb")
saved_classifier = pickle.load(saved_classifier_f)
saved_classifier_f.close()

# read saved word features
word_features5k_f = open(modelPath + model + "/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

# Define Sentiment Tokenizer Class as tok
tok = sa.Tokenizer(preserve_case=False)
def find_features(document):
    words = tok.tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

# Define Sentiment Analysis function. Using aboves
def sentiment(text):
    return saved_classifier.classify(find_features(text))


# In[4]:

def whichSide(tags, tags_home, tags_away):
    tags = map(lambda tag: '#' + tag.lower(), tags)
    if set(tags).intersection(tags_home) and set(tags).intersection(tags_away):
        return 'both'
    elif set(tags).intersection(tags_home):
        return 'home'
    elif set(tags).intersection(tags_away):
        return 'away'
    else:
        return 'nothing'


# In[5]:

def ReadFileAsDF(fileName, home_team, away_team):
    # both team hashtags
    tags_home = Hashtags.dic[home_team]
    tags_away = Hashtags.dic[away_team]

    # read file as dataframe, and add 'side' column that shows which team's tweet it is 
    dfTweets = pd.read_csv(fileName, header=None, names=['date', 'text', 'user', 'tags'])
    dfTweets['side'] = map(lambda tags: whichSide(tags, tags_home, tags_away), map(lambda tag: tag.split(','), dfTweets['tags']))
    
    # count tweets
    sides = ['home', 'away', 'both', 'nothing']
    numSides =  map(lambda side: (side, len(dfTweets[dfTweets["side"] == side])), sides)
    print numSides
    
    dfHomeTweets = dfTweets[dfTweets["side"] == 'home']
    dfAwayTweets = dfTweets[dfTweets["side"] == 'away']
    dfHomeTweets = pd.DataFrame(dfHomeTweets.values, range(len(dfHomeTweets)), dfHomeTweets.columns)
    dfAwayTweets = pd.DataFrame(dfAwayTweets.values, range(len(dfAwayTweets)), dfAwayTweets.columns)
    
    return dfHomeTweets, dfAwayTweets


# In[6]:

# Create DataFrames for home and away tweets
def SentimentHomeAway(dfHomeTweets, dfAwayTweets):
    home_sent = map(lambda tweet: sentiment(tweet), dfHomeTweets["text"])
    away_sent = map(lambda tweet: sentiment(tweet), dfAwayTweets["text"])
    
    return [collections.Counter(home_sent)['pos'], 
            collections.Counter(home_sent)['neg'],
            collections.Counter(away_sent)['pos'],
            collections.Counter(away_sent)['neg']]


# In[7]:

# Save the dictionary values to file
def ListSaveToCSV(fileName, myList):
    with open(fileName + '.csv', 'a') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(myList)


# In[8]:

def GameNegPos(game, loadFileName, saveFileName):
    
    home_team = game[0]
    away_team = game[1]

    dfHome, dfAway = ReadFileAsDF(loadFileName, home_team, away_team)
    
    listResSent = SentimentHomeAway(dfHome, dfAway)
    listResGame = [home_team, away_team] + listResSent

    os.chdir("/Users/Bya/Dropbox/Research/datas/Results/")
    ListSaveToCSV(saveFileName, listResGame)


# In[9]:

Bournemouth = 'Bournemouth'
Arsenal = 'Arsenal'
Villa = 'Villa'
Chelsea = 'Chelsea'
Crystal = 'Crystal'
Everton = 'Everton'
Leicester = 'Leicester'
Liverpool = 'Liverpool'
City = 'City'
United = 'United'
Newcastle = 'Newcastle'
Norwich = 'Norwich'
Southampton = 'Southampton'
Stoke = 'Stoke'
Sunderland = 'Sunderland'
Swansea = 'Swansea'
Tottenham = 'Tottenham'
Watford = 'Watford'
WestBromwich = 'WestBromwich'
WestHam = 'WestHam'


# In[10]:

listGamesW8 = [(Crystal, WestBromwich),
               
               (Villa, Stoke),
               (Bournemouth, Watford),
               (City, Newcastle),
               (Norwich, Leicester),
               (Sunderland, WestHam),
               
               (Chelsea, Southampton),
               
               (Everton, Liverpool),
               
               (Arsenal, United),
               (Swansea, Tottenham)]

loadFileNameGW8 = ["/Users/Bya/Dropbox/Research/datas/GW8/game1_json.txt.csv",
                   
                   "/Users/Bya/Dropbox/Research/datas/GW8/game2_6_json.txt.csv",
                   "/Users/Bya/Dropbox/Research/datas/GW8/game2_6_json.txt.csv",
                   "/Users/Bya/Dropbox/Research/datas/GW8/game2_6_json.txt.csv",
                   "/Users/Bya/Dropbox/Research/datas/GW8/game2_6_json.txt.csv",
                   "/Users/Bya/Dropbox/Research/datas/GW8/game2_6_json.txt.csv",
                   
                   "/Users/Bya/Dropbox/Research/datas/GW8/game7_json.txt.csv",
                   
                   "/Users/Bya/Dropbox/Research/datas/GW8/game8_json.txt.csv",
                   
                   "/Users/Bya/Dropbox/Research/datas/GW8/game9_10_json.txt.csv",
                   "/Users/Bya/Dropbox/Research/datas/GW8/game9_10_json.txt.csv"]

saveFileNameGW8 = 'GW8'

for i in range(len(listGamesW8)):
    print(listGamesW8[i], loadFileNameGW8[i], saveFileNameGW8)
#     GameNegPos(listGamesW8[i], loadFileNameGW8[i], saveFileNameGW8)

