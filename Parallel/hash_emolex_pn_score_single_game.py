
# coding: utf-8

import os
import sys
import pickle
import time
import datetime
import pandas as pd
from joblib import Parallel, delayed
import multiprocessing

# Local Imports
path = str(os.path.expanduser('~')) + '/git/predictEPL/config'
sys.path.append(path)
import paths

sys.path.append(paths.UTILS)
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


# which week
WEEK_NUM = input()
dfGameInfos = dfGameInfos[dfGameInfos.GW == int(WEEK_NUM)].copy().reset_index(drop=True)


# Convert number strings to integers
dfGameInfos['GW'] = [int(GW) for GW in dfGameInfos['GW']]
dfGameInfos['score_ht_home'] = [int(number) for number in dfGameInfos['score_ht_home']]
dfGameInfos['score_ht_away'] = [int(number) for number in dfGameInfos['score_ht_away']]
dfGameInfos['score_ft_home'] = [int(number) for number in dfGameInfos['score_ft_home']]
dfGameInfos['score_ft_away'] = [int(number) for number in dfGameInfos['score_ft_away']]


# *******************************************************
# *******************************************************

PKL_HASH_EMOLEX = "dtr_hash_svn_2016-01-22_08:26:25.pkl"
PKL_REVIEW = 'detecter_sentiment_reviews_nb0204.pkl'

# Read SVM(hash emolex) detecter
with open(paths.DETECTER_HOME + PKL_REVIEW, 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'utf-8'
    detecter = u.load()


# *******************************************************
# *******************************************************

def AddScorePosNegColumn(df, detecter):
    df = df.copy().reset_index(drop=True)
    score_pos = []
    score_neg = []

    for text in df.text:
        neg, pos = detecter.predict_proba([text])[0]
        score_pos.append(pos)
        score_neg.append(neg)

    df['score_pos'] = score_pos
    df['score_neg'] = score_neg

    return df


# Count Home, Away Emolex
def TweetPNscore(week, team_home, team_away):

    # Read Single as DF
    dfGame = useful_methods.SingleGameDf(week, team_home, team_away, filtering=True, retweet=RETWEET_STATUS)
    if dfGame is None:
        print(None, None)
        return None

    dfGame.ith_minute = [int(ith_minute) for ith_minute in list(dfGame.ith_minute)]

    # Count Emolex Words
    dfHome = AddScorePosNegColumn(dfGame[(dfGame.side == 'home') & (dfGame.ith_minute <= TIME_LIMIT)], detecter)
    dfAway = AddScorePosNegColumn(dfGame[(dfGame.side == 'away') & (dfGame.ith_minute <= TIME_LIMIT)], detecter)

    return (
        dfHome.score_pos.sum(), dfHome.score_neg.sum(),
        dfAway.score_pos.sum(), dfAway.score_neg.sum())


# *******************************************************
# *******************************************************
def PnScoringSingleMatch(ith_row):
    # Team names
    week = dfGameInfos.iloc[ith_row]['GW']
    team_home = dfGameInfos.iloc[ith_row]['home_team']
    team_away = dfGameInfos.iloc[ith_row]['away_team']

    # Scoring by model
    pn_score = TweetPNscore(week, team_home, team_away)

    # print each rows
    print('%s,%s,%s,%s,%s,%s,%s' %
        (week, team_home, team_away,
            pn_score[0], pn_score[1], pn_score[2], pn_score[3]))

    result = (week, team_home, team_away, pn_score[0], pn_score[1], pn_score[2], pn_score[3])

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
results = Parallel(n_jobs=num_cores)(delayed(PnScoringSingleMatch)(i) for i in inputs)


# print time
taken_time = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_taken_time))
print("[Done]: ", taken_time)
print("[Date]: ", datetime.datetime.now())

# Create DF
columns = ['GW', 'home_team', 'away_team', 'pn_home_pos', 'pn_home_neg', 'pn_away_pos', 'pn_away_neg']
dfResult = pd.DataFrame(results, columns=columns)

# Save as CSV
useful_methods.DFtoCSV(dfResult, paths.READ_PATH_RESULTS, 'hash_single', index=False)
print("[Saved in]: %s" % (paths.READ_PATH_RESULTS + 'hash_single.csv'))



















