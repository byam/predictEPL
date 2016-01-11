# coding: utf-8

import os
import sys
import pandas as pd

sys.path.append('/Users/Bya/git/predictEPL/config/')
sys.path.append('/Users/Bya/git/predictEPL/utils/')


from games import GAMES
from csv_files import FILES
from hash_tags import HashTags
import paths
import fake_tweets
import users

from useful_methods import DateToMinute
from useful_methods import GameStartTime


# save df to csv file.
def DFtoCSV(df, pathToSave, fileName, index=True):
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)

    os.chdir(pathToSave)

    if os.path.exists(fileName + '.csv'):
        os.remove(fileName + '.csv')

    df.to_csv(fileName + '.csv', sep=',', encoding='utf-8', index=index, header=True)


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


def TextStatus(text):
    text = text.lower()
    for tuples in fake_tweets.STREAM_TWEETS_TUPLES:
        if tuples[0] in text and tuples[1] in text:
            return 'stream'
    return 'normal'


def UserStatus(user):
    if user in users.BOT:
        return 'bot'
    elif user in users.STREAMS:
        return 'stream'
    elif user in users.NON_ENGLISH:
        return 'non_english'
    elif user in users.MEDIAS:
        return 'media'
    else:
        return 'normal'


def SplitSingleGameAndSave(file_name, teams, GW):
    # teams
    home_team = teams[0]
    away_team = teams[1]

    # both team hashtags
    tags_home = HashTags.dic[home_team]
    tags_away = HashTags.dic[away_team]

    # read file as dataframe, and add 'side' column that shows which team's tweet it is
    os.chdir(paths.READ_PATH_EXTRACTED_CSV + GW)
    dfTweets = pd.read_csv(file_name, header=None, names=['date', 'text', 'tags', 'user', 'status'])
    dfTweets['user'] = [user.lower() for user in dfTweets['user']]
    dfTweets['side'] = [WhichSide(str(tags).split(','), tags_home, tags_away) for tags in dfTweets['tags']]

    # add 'user_status' and 'text_status' column
    dfTweets['text_status'] = [TextStatus(text) for text in dfTweets['text']]
    dfTweets['user_status'] = [UserStatus(user) for user in dfTweets['user']]

    # add 'ith_minute' column
    week = GW[2::]
    start_time = GameStartTime(week, home_team, away_team)
    dfTweets['ith_minute'] = [DateToMinute(date, start_time) for date in dfTweets['date']]

    # count tweets
    sides = ['home', 'away', 'both', 'nothing']
    numSides = map(lambda side: (side, len(dfTweets[dfTweets["side"] == side])), sides)
    print("\n %s vs %s :\n" % (home_team, away_team))
    print(list(numSides))

    dfHomeAwayTweets = dfTweets[(dfTweets["side"] == 'home') | (dfTweets["side"] == 'away') | (dfTweets["side"] == 'both')]
    dfHomeAwayTweets = pd.DataFrame(dfHomeAwayTweets.values, range(len(dfHomeAwayTweets)), dfHomeAwayTweets.columns)

    DFtoCSV(dfHomeAwayTweets, paths.SAVE_PATH_SINGLE_GAME + GW + '/SingleGames/', home_team + "_vs_" + away_team, False)


def WeekSplit(week):
    GW = 'GW' + str(week)

    week_games = GAMES[GW]
    week_files = FILES[GW]

    for i in range(len(week_games)):
        SplitSingleGameAndSave(week_files[i], week_games[i], GW)

if __name__ == '__main__':
    week_number = sys.argv[1]

    # weeks as : 4to20
    if 'to' in week_number:
        start, end = list(map(int, week_number.split('to')))
        for week in range(start, end + 1):
            # gw 12 data is no available
            if week == 12:
                continue
            print("\n\n=======================================")
            print("[Week]: ", week)
            WeekSplit(week)
    # only week : 4
    else:
        WeekSplit(week_number)
