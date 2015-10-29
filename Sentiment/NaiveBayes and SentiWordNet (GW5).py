
# coding: utf-8

# In[1]:

import os
os.chdir('/Users/Bya/git/predictEPL/MyFunctions/')

from classifiers import nb_swn, createTuples, Teams
import dataIO
import pandas as pd
import time


# In[2]:

def preprocess(x):
    # 不要な行, 列のフィルタなど、データサイズを削減する処理
    return x

def tweetSentiment(home_team, away_team, GW):
    filePath = '/Users/Bya/Dropbox/Research/datas/' + GW +'/SingleGames/' + home_team + '_vs_' + away_team + '.csv'
    
    reader = pd.read_csv(filePath, chunksize=1000)
    dfHA = pd.concat((preprocess(r) for r in reader), ignore_index=True)

    dfHA['nb'] = None
    dfHA['nb_pos'] = None
    dfHA['nb_neg'] = None
    
    dfHA['swn'] = None
    dfHA['swn_pos'] = None
    dfHA['swn_neg'] = None
    dfHA['swn_obj'] = None
    
    for row in dfHA.iterrows():
        tweet = row[1]['text']
        
        try:
            nb, nb_pos, nb_neg, swn, swn_pos, swn_neg, swn_obj = nb_swn(tweet)
        except:
            nb, nb_pos, nb_neg, swn, swn_pos, swn_neg, swn_obj = 0, 0, 0, 0, 0, 0, 0


        row[1]['nb'] = nb
        row[1]['nb_pos'] = nb_pos
        row[1]['nb_neg'] = nb_neg
        row[1]['swn'] = swn
        row[1]['swn_pos'] = swn_pos
        row[1]['swn_neg'] = swn_neg
        row[1]['swn_obj'] = swn_obj
    
    savePath = '/Users/Bya/Dropbox/Research/datas/Results/NB_SWN/' + GW
    dataIO.DFtoCSV(dfHA, savePath, home_team + "_vs_" + away_team, False)


# In[3]:

team = Teams()
weekGames = [
#     team.Everton, team.Chelsea,
    
#     team.Arsenal, team.Stoke,
#     team.Crystal, team.City,
#     team.Norwich, team.Bournemouth,
#     team.Watford, team.Swansea,
#     team.WestBromwich, team.Southampton,
    
#     team.United, team.Liverpool,
    
    team.Sunderland, team.Tottenham,
    
    team.Leicester, team.Villa,
    
    team.WestHam, team.Newcastle,
            ]


# In[ ]:

weekGames = createTuples(weekGames)

GW = 'GW5'

t1 = time.time()

for game in weekGames:
    t2 = time.time()
    home_team = game[0]
    away_team = game[1]

    tweetSentiment(home_team, away_team, GW)
    print("%s Time: %s" % (game, time.time() - t2))

print("Time: %s" % (time.time() - t1))

