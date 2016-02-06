
# coding: utf-8
import os
import sys
import time
import datetime
import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import multiprocessing


# Local Imports
path = str(os.path.expanduser('~')) + '/git/predictEPL/config'
sys.path.append(path)
import paths

sys.path.append(paths.UTILS)
import emolex
import useful_methods


# *******************************************************
# *******************************************************

# Limitations
TIME_LIMIT = 63
RETWEET_STATUS = False
FILTER_STATUS = True
START_TIME = 1
END_TIME = 63


# *******************************************************
# *******************************************************

# Game Infos
os.chdir(paths.READ_PATH_GAME_INFO)
dfGameInfos = useful_methods.csv_dic_df('game_infos.csv')
dfGameInfos = useful_methods.DropNanGames(dfGameInfos)


# Convert number strings to integers
dfGameInfos['GW'] = [int(GW) for GW in dfGameInfos['GW']]
dfGameInfos['score_ht_home'] = [int(number) for number in dfGameInfos['score_ht_home']]
dfGameInfos['score_ht_away'] = [int(number) for number in dfGameInfos['score_ht_away']]
dfGameInfos['score_ft_home'] = [int(number) for number in dfGameInfos['score_ft_home']]
dfGameInfos['score_ft_away'] = [int(number) for number in dfGameInfos['score_ft_away']]


# Read Emotion-Lexicon-Soccer as Dictionary
dic_emolex_soccer = emolex.EmolexSoccerDic()


# *******************************************************
# *******************************************************

# ### Emolex Count Functions


# Summing counted emolex
def EmolexSumList(dfEmolex, start=1, end=60):
    # Time Interval
    dfEmolex.ith_minute = [int(ith_minute) for ith_minute in list(dfEmolex.ith_minute)]
    dfEmolex = dfEmolex[(dfEmolex.ith_minute >= start) & (dfEmolex.ith_minute <= end)]

    # Sum Emolex Count
    anger = dfEmolex.anger.sum()
    fear = dfEmolex.fear.sum()
    disgust = dfEmolex.disgust.sum()
    sadness = dfEmolex.sadness.sum()
    surprise = dfEmolex.surprise.sum()
    trust = dfEmolex.trust.sum()
    joy = dfEmolex.joy.sum()
    anticipation = dfEmolex.anticipation.sum()
    positive = dfEmolex.positive.sum()
    negative = dfEmolex.negative.sum()

    return np.array([anger, fear, disgust, sadness,
            surprise,
            trust, joy, anticipation,
            positive, negative])


# Count Home, Away Emolex
def CountGameEmolexEmoji(week, team_home, team_away):

    # Read Single as DF
    dfGame = useful_methods.SingleGameDf(week, team_home, team_away, filtering=FILTER_STATUS, retweet=RETWEET_STATUS)
    if dfGame is None:
        return (None, None)

    dfGame.ith_minute = [int(ith_minute) for ith_minute in list(dfGame.ith_minute)]

    # Count Emolex Words
    dfEmolexHome = emolex.CreateEmolexDF(dfGame[(dfGame.side == 'home') & (dfGame.ith_minute <= TIME_LIMIT)], dic_emolex_soccer)
    dfEmolexAway = emolex.CreateEmolexDF(dfGame[(dfGame.side == 'away') & (dfGame.ith_minute <= TIME_LIMIT)], dic_emolex_soccer)

    # Sum Emolex
    dic_emolex_home = EmolexSumList(dfEmolexHome, start=START_TIME, end=END_TIME)
    dic_emolex_away = EmolexSumList(dfEmolexAway, start=START_TIME, end=END_TIME)

    # Count Emoji Sentiment Count
    dic_emoji_sent_home = useful_methods.EmojiSentimentCount(dfGame, 'home', START_TIME, END_TIME)
    dic_emoji_sent_away = useful_methods.EmojiSentimentCount(dfGame, 'away', START_TIME, END_TIME)

    # Merge: Emolex & Emoji Sentiment
    dic_emolex_home[-2] += dic_emoji_sent_home['pos']
    dic_emolex_home[-1] += dic_emoji_sent_home['neg']

    dic_emolex_away[-2] += dic_emoji_sent_away['pos']
    dic_emolex_away[-1] += dic_emoji_sent_away['neg']

    return (dic_emolex_home, dic_emolex_away)


# *******************************************************
# *******************************************************
def EmolexCountSingleMatch(ith_row):
    # Team names
    week = dfGameInfos.iloc[ith_row]['GW']
    team_home = dfGameInfos.iloc[ith_row]['home_team']
    team_away = dfGameInfos.iloc[ith_row]['away_team']

    # Count Emolex Word
    emolex_count = CountGameEmolexEmoji(week, team_home, team_away)

    # print each rows
    print('%s, %s, %s, %s, %s' %
        (week, team_home, team_away, emolex_count[0], emolex_count[1]))

    result = (week, team_home, team_away, emolex_count[0], emolex_count[1])

    return result


# *******************************************************
# *******************************************************

# Parallel computing

# number of cores
num_cores = multiprocessing.cpu_count()

# row indexes as inputs
inputs = range(len(dfGameInfos))

# parallel loop
start_taken_time = time.time()


# results
results = Parallel(n_jobs=num_cores)(delayed(EmolexCountSingleMatch)(i) for i in inputs)


# print time
taken_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_taken_time))
print("[Done]: ", taken_time)
print("[Date]: ", datetime.datetime.now())


# columns
columns = ['GW', 'home_team', 'away_team', 'emolex_home', 'emolex_away']
dfResult = pd.DataFrame(results, columns=columns)

# Save as CSV
useful_methods.DFtoCSV(dfResult, paths.READ_PATH_RESULTS, 'emolex_emoji_all_ht', index=False)
print("[Saved in]: %s" % (paths.READ_PATH_RESULTS + 'emolex_emoji_all_ht.csv'))


















