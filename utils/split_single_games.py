# coding: utf-8

import os
import sys
import pandas as pd

sys.path.append('/Users/Bya/git/predictEPL/config/')

from games import GAMES
from csv_files import FILES
from hash_tags import HashTags
from paths import READ_PATH_EXTRACTED_CSV
from paths import SAVE_PATH_SINGLE_GAME


# save df to csv file.
def DFtoCSV(df, pathToSave, fileName, index=True):
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)

    os.chdir(pathToSave)

    df.to_csv(fileName + '.csv', sep=',', encoding='utf-8', index=index)


def WhichSide(tags, tags_home, tags_away):
    tags = list(map(lambda tag: '#' + tag.lower(), tags))
    if set(tags).intersection(tags_home) and set(tags).intersection(tags_away):
        return 'both'
    elif set(tags).intersection(tags_home):
        return 'home'
    elif set(tags).intersection(tags_away):
        return 'away'
    else:
        return 'nothing'


def SplitSingleGameAndSave(file_name, teams, GW):
    # teams
    home_team = teams[0]
    away_team = teams[1]

    # both team hashtags
    tags_home = HashTags.dic[home_team]
    tags_away = HashTags.dic[away_team]

    # read file as dataframe, and add 'side' column that shows which team's tweet it is
    os.chdir(READ_PATH_EXTRACTED_CSV + GW)
    dfTweets = pd.read_csv(file_name, header=None, names=['date', 'text', 'tags', 'user', 'status'])
    dfTweets['side'] = [WhichSide(str(tags).split(','), tags_home, tags_away) for tags in dfTweets['tags']]

    # count tweets
    sides = ['home', 'away', 'both', 'nothing']
    numSides = map(lambda side: (side, len(dfTweets[dfTweets["side"] == side])), sides)
    print("\n %s vs %s :\n" % (home_team, away_team))
    print(list(numSides))

    dfHomeAwayTweets = dfTweets[(dfTweets["side"] == 'home') | (dfTweets["side"] == 'away') | (dfTweets["side"] == 'both')]
    dfHomeAwayTweets = pd.DataFrame(dfHomeAwayTweets.values, range(len(dfHomeAwayTweets)), dfHomeAwayTweets.columns)

    DFtoCSV(dfHomeAwayTweets, SAVE_PATH_SINGLE_GAME + GW + '/SingleGames/', home_team + "_vs_" + away_team, False)


def WeekSplit(week):
    GW = 'GW' + str(week)

    week_games = GAMES[GW]
    week_files = FILES[GW]

    for i in range(len(week_games)):
        SplitSingleGameAndSave(week_files[i], week_games[i], GW)


if __name__ == '__main__':
    week = int(sys.argv[1])
    WeekSplit(week)
