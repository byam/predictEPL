import os
import sys
import time
import pandas as pd

sys.path.append("../utils/")
sys.path.append("../config/")

import paths
import emolex
import tokenizer
import useful_methods

# All Game Infos
os.chdir(paths.READ_PATH_GAME_INFO)
dfGameInfos = useful_methods.csv_dic_df('game_infos.csv')

# Convert number strings to integers
dfGameInfos['GW'] = [int(GW) for GW in dfGameInfos['GW']]
dfGameInfos['score_ht_home'] = [int(number) for number in dfGameInfos['score_ht_home']]
dfGameInfos['score_ht_away'] = [int(number) for number in dfGameInfos['score_ht_away']]
dfGameInfos['score_ft_home'] = [int(number) for number in dfGameInfos['score_ft_home']]
dfGameInfos['score_ft_away'] = [int(number) for number in dfGameInfos['score_ft_away']]

# HT: Equal games
# dfGameInfosEqual = dfGameInfos[(dfGameInfos['score_ht_home'] == dfGameInfos['score_ht_away']) &
#                                (dfGameInfos['GW'] >= 4)].copy()

weeks = list(dfGameInfos['GW'])
home_teams = list(dfGameInfos['home_team'])
away_teams = list(dfGameInfos['away_team'])
score_ht_homes = list(dfGameInfos['score_ht_home'])
score_ht_aways = list(dfGameInfos['score_ht_away'])
score_ft_homes = list(dfGameInfos['score_ft_home'])
score_ft_aways = list(dfGameInfos['score_ft_away'])


# Create Again Hash Emolex Soccer Data
# Saving Created DF to CSV
def HashEmolexAllCreate():
    # Emolex dic
    dic_emolex_soccer, dic_emolex_stemmed_soccer = emolex.EmolexSoccerDic()

    # Define: All Hash Emolex DF
    dfNewHashEmolex = pd.DataFrame(columns=['text', 'hash_emolex_word', 'sentiments'])
    texts = []
    hash_emolexs = []
    sentiments = []

    start_time = time.time()

    # Start All Here
    for index in range(len(weeks)):
        try:
            # Read Single Game as DF
            filename = home_teams[index] + '_vs_' + away_teams[index] + '.csv'
            os.chdir(paths.READ_PATH_EXTRACTED_CSV + 'GW' + str(weeks[index]) + '/SingleGames/')
            df = useful_methods.csv_dic_df(filename)

            ###########################################################################
            # Filter DF: remove tweets of stream, bots ...
            dfFilter = useful_methods.FilterDF(df[df.status != 'retweet'])

            # Add column: hash_emolex
            dfFilter['hash_emolex'] = [tokenizer.HashEmolex(tags, dic_emolex_soccer) for tags in dfFilter.tags]

            # Emolex in Hashtags
            dfHashEmolex = dfFilter[(dfFilter.hash_emolex != '')]

            # Check through each Tweet
            for i in range(len(dfHashEmolex)):
                # hash tags
                hash_emolex = dfHashEmolex.iloc[i]['hash_emolex'].split(',')

                # each tag
                for emo in set(hash_emolex):
                    if emo in dic_emolex_soccer:
                        text = (dfHashEmolex.iloc[i]['text'])
                        if text not in texts:
                            # appedings
                            texts.append(text)
                            hash_emolexs.append(emo)
                            sentiment = ",".join([key for key, value in dic_emolex_soccer[emo].items() if (value > 0)])
                            sentiments.append(sentiment)
        except:
            continue

    print("[Done]: %.2f" % (time.time() - start_time))

    # Result
    dfNewHashEmolex['text'] = texts
    dfNewHashEmolex['hash_emolex_word'] = hash_emolexs
    dfNewHashEmolex['sentiments'] = sentiments

    # Save
    useful_methods.DFtoCSV(dfNewHashEmolex, "/Users/Bya/Dropbox/Research/datas/TweetsPN/", "hash_emolex_all", index=False)
    print("[Saved in]: /Users/Bya/Dropbox/Research/datas/TweetsPN/hash_emolex_all.csv")


# Read CSV Hash Emolex Soccer Data
def HashEmolexAllRead():
    os.chdir("/Users/Bya/Dropbox/Research/datas/TweetsPN/")
    df = useful_methods.csv_dic_df('hash_emolex_all.csv')
    return df


# Read CSV Twitter Pos, Nega Equal Soccer Data
def TweetPnEqualRead():
    os.chdir("/Users/Bya/Dropbox/Research/datas/TweetsPN/")
    df = useful_methods.csv_dic_df('tweets_pn_eq.csv')
    return df
