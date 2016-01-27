import os
import sys
import collections
from pprint import pprint
import math
import pandas as pd
import csv

# Local Imports
path = str(os.path.expanduser('~')) + '/git/predictEPL/config'
sys.path.append(path)
import paths
import odds_portal
import names


# Return Directory's file names
def FolderFiles(folder, directory, ends='.txt'):
    os.chdir(directory)
    for folderName, subFolders, fileNames in os.walk(folder):
        fileNames = filter(lambda filename: filename.endswith(ends), fileNames)
        return list(fileNames)


# Return Game's start time
def GameStartTime(week, home_team, away_team):
    week = str(week)

    os.chdir(paths.READ_PATH_GAME_INFO)
    dfGameInfos = csv_dic_df("game_infos.csv")

    start_time = dfGameInfos[
        (dfGameInfos['GW'] == week) &
        (dfGameInfos['home_team'] == home_team) &
        (dfGameInfos['away_team'] == away_team)
    ]['time'].iloc[0]

    return start_time


# read csv as dataframe
def csv_dic_df(filename, head=[]):
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        dic = {}

        if len(head) == 0:
            headers = next(reader)
        else:
            headers = head
        for header in headers:
            dic[header] = []

        for row in reader:
            if len(row) == len(headers):
                for i in range(len(row)):
                    dic[headers[i]].append(row[i])

        df = pd.DataFrame(dic)

    return df


# save df to csv file.
def DFtoCSV(df, pathToSave, fileName, index=True):
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)

    os.chdir(pathToSave)

    if os.path.exists(fileName + '.csv'):
        os.remove(fileName + '.csv')

    df.to_csv(fileName + '.csv', sep=',', encoding='utf-8', index=index, header=True)


def DateToSeconds(string):
    try:
        string = string[-19:-11]
        hour, minute, second = map(int, string.split(':'))

        hour = hour * 3600
        minute = minute * 60

        return hour + minute + second
    except:
        return None


def DateToMinute(date_string, start_time):
    # string to seconds
    date_seconds = DateToSeconds(date_string)

    # string to seconds
    string = start_time[-5::]
    hour, minute = map(int, string.split(':'))
    start_seconds = hour * 3600 + minute * 60

    # convert to ith minute
    ith_minute = math.ceil((date_seconds - start_seconds) / 60)

    return ith_minute


# Filtering Tweets
# remove: live stream tweets, bot accounts
# ith_minute starts: 1
def FilterDF(df):
    df = df.copy()

    # string to int
    df['ith_minute'] = [int(ith_minute) for ith_minute in df['ith_minute']]

    dfFilter = df[
            (df['text_status'] == 'normal') &
            (df['user_status'] == 'normal') &
            (df['ith_minute'] > 0)
        ].copy()

    dfFilter = dfFilter.reset_index(drop=True)
    dfFilter['ith_minute'] = [str(ith_minute) for ith_minute in dfFilter['ith_minute']]

    return dfFilter


# Tweet, Retweet, Quoted tweet's percentage
def TweetsPercentageByWeek(week):
    # find files
    GW = 'GW' + str(week)
    single_games = FolderFiles('SingleGames', paths.READ_PATH_EXTRACTED_CSV + GW, '.csv')

    # counting tweets
    all_week = 0
    tweet = 0
    retweet = 0
    quoted = 0

    for single_game in single_games:
        # read data as df
        os.chdir(paths.READ_PATH_EXTRACTED_CSV + GW + '/SingleGames/')
        dfTweets = csv_dic_df(single_game)

        tweet += len(dfTweets[(dfTweets['status'] == 'tweet')])
        retweet += len(dfTweets[(dfTweets['status'] == 'retweet')])
        quoted += len(dfTweets[(dfTweets['status'] == 'quoted')])

        all_week += len(dfTweets)

    print("All Tweet Number: ", all_week)
    print("\tNormal Tweet: %s(%.2f)" % (tweet, tweet/all_week))
    print("\tNormal Retweet: %s(%.2f)" % (retweet, retweet/all_week))
    print("\tNormal Quoted: %s(%.2f)" % (quoted, quoted/all_week))


# Printing Most Common Element os List
def ShowMostCommon(my_list, most=10):
    counter = collections.Counter(my_list)
    most_common = list(counter.most_common(most))
    pprint(most_common)


def MostCommonUsersByWeek(week, users_number=20, filtered=False):
    # find files
    GW = 'GW' + str(week)
    single_games = FolderFiles('SingleGames', paths.READ_PATH_EXTRACTED_CSV + GW, '.csv')

    # accumulating users
    all_users = []

    for single_game in single_games:
        os.chdir(paths.READ_PATH_EXTRACTED_CSV + GW + '/SingleGames/')
        dfTweets = csv_dic_df(single_game)

        if filtered:
            dfTweets = dfTweets[(dfTweets.text_status == 'normal') & (dfTweets.user_status == 'normal')]

        user = list(dfTweets['user'])
        all_users += user

    print("All User Number: ", len(all_users))
    print("Unique User Number: %s (%.2f)\n" % (len(set(all_users)), len(set(all_users))/len(all_users)))

    counter = collections.Counter(all_users)
    most_common = list(counter.most_common(users_number))
    pprint(most_common)


# Read oddsportal.com
def OddsPortalDf():
    lines = odds_portal.RAW_ODDS.split("\n")

    dfOdds = pd.DataFrame(columns=[
            "GW",
            "time",
            "team_home", "team_away",
            "score_ft_home", "score_ft_away",
            "odds_home", "odds_away", "odds_draw"
        ])

    d_i = 0
    for i_line in range(len(lines) - 1, -1, -1):
        try:
            if lines[i_line][2] == ":":
                # extract datas
                time = lines[i_line].split(" - ")[0][0:5]
                home_team = lines[i_line].split(" - ")[0][5::].strip()
                away_team = lines[i_line].split(" - ")[1][0:-4].strip()
                scores = lines[i_line].split(" - ")[1][-4:-1]
                score_ft_home, score_ft_away = scores.split(":")
                odds_home, odds_draw, odds_away = lines[i_line + 1:i_line + 4]
                GW = math.floor(d_i / 10) + 1

                # change names
                home_team = names.ChangeTeamName(home_team)
                away_team = names.ChangeTeamName(away_team)

                # datas to dic
                odds_infos = {
                    "GW": GW,
                    "time": time,
                    "team_home": home_team,
                    "team_away": away_team,
                    "score_ft_home": score_ft_home,
                    "score_ft_away": score_ft_away,
                    "odds_home": odds_home,
                    "odds_draw": odds_draw,
                    "odds_away": odds_away
                }

                # adding Row to DF
                dfOdds.loc[d_i] = pd.Series(odds_infos)
                d_i += 1
        except:
            continue

    return dfOdds


# Read Single Game as DF
# input: week, home, away teams
# output: dataframe
def SingleGameDf(week, team_home, team_away, filtering=False, retweet=True):
    GW = 'GW' + str(week)
    if GW in ['GW1', 'GW2', 'GW3', 'GW4', 'GW12']:
        print("[Not Game Exists]: Check your inputs")
        return

    # ex: ['Chelsea_vs_Norwich.csv', ...]
    filenames = FolderFiles(GW + '/SingleGames', paths.READ_PATH_EXTRACTED_CSV, ends='.csv')

    # ex: [('Chelsea, Norwich.csv'), ...]
    filenames_teams = [(filename.split('_vs_')[0], filename.split('_vs_')[1].split('.csv')[0]) for filename in filenames]

    # if game not exists
    if (team_home, team_away) not in filenames_teams:
        print("[Not Game Exists]: Check your inputs")
        return

    # Set Game
    filename = team_home + '_vs_' + team_away + '.csv'

    # Read DF
    os.chdir(paths.READ_PATH_EXTRACTED_CSV + GW + '/SingleGames')
    df = csv_dic_df(filename)

    # Exclude retweet
    if not retweet:
        df = df[df.status != 'retweet']
        df = df.reset_index(drop=True)

    # Filter:
    if filtering:
        df = FilterDF(df)

    return df


# Checking Single Game's data is available
# return: True or False
def CheckSingleGameFile(week, team_home, team_away):
    GW = 'GW' + str(week)
    if GW in ['GW1', 'GW2', 'GW3', 'GW4', 'GW12']:
        return False

    # ex: ['Chelsea_vs_Norwich.csv', ...]
    filenames = FolderFiles(GW + '/SingleGames', paths.READ_PATH_EXTRACTED_CSV, ends='.csv')

    # ex: [('Chelsea, Norwich.csv'), ...]
    filenames_teams = [(filename.split('_vs_')[0], filename.split('_vs_')[1].split('.csv')[0]) for filename in filenames]

    # if game not exists
    if (team_home, team_away) not in filenames_teams:
        return False

    return True


# Dropping No Data Games
# return: df
def DropNanGames(dfGameInfos):
    df = dfGameInfos.copy()

    drop_index = []

    for ith_row in range(len(df)):
        # Team names
        week = df.iloc[ith_row]['GW']
        team_home = df.iloc[ith_row]['home_team']
        team_away = df.iloc[ith_row]['away_team']

        if not CheckSingleGameFile(week, team_home, team_away):
            drop_index.append(ith_row)

    df = df.drop(df.index[drop_index]).copy().reset_index(drop=True)

    return df
