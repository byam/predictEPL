import os
import sys
import collections
from pprint import pprint
import math
import pandas as pd
import csv

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


sys.path.append('/Users/Bya/git/predictEPL/config/')
sys.path.append('/Users/Bya/git/predictEPL/MyFunctions/')

import paths
import replacers


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


def cleanHash(word):
    if word[0] == '#':
        return word[1::]
    elif word[0] == '@':
        return '@'
    elif word[0:4] == 'http':
        return 'http'
    else:
        return word


def PreprocessingTweet(tweet, debug=False):
    if debug:
        print("====================================")
        print("[Original Tweet]: \n\n %s \n\n" % tweet)

    # can't -> cannot, bya's -> bya is
    replacer = replacers.RegexpReplacer()
    tweet = replacer.replace(tweet.lower())
    if debug:
        print("====================================")
        print("[Replaced Tweet]: \n\n %s \n\n" % tweet)

    # Tweet tokenizer and lower case
    words = TweetTokenizer().tokenize(tweet)
    words = [word.lower() for word in words]
    if debug:
        print("====================================")
        print("[Tokenized Tweet]: \n\n %s \n\n" % words)

    # defining stopwords
    english_stops = set(stopwords.words('english'))
    english_stops_added = english_stops | {'!', '.', ',', ':', ';', '#', '?', 'RT', '-', '@', 'rt', 'http'}
    words = [word for word in words if word not in english_stops_added]
    if debug:
        print("====================================")
        print("[Cleaned Stopwords Tweet]: \n\n %s \n\n" % words)

    # words = map(lambda word: cleanHash(word), words)
    words = [cleanHash(word) for word in words]
    if debug:
        print("====================================")
        print("[Clean hash Tweet]: \n\n %s \n\n" % words)

    # Stemmer
    stemmer = PorterStemmer()
    words_stemmed = list(map(lambda word: stemmer.stem(word), words))
    if debug:
        print("====================================")
        print("[Stemmed hash Tweet]: \n\n %s \n\n" % words_stemmed)

    return words, words_stemmed
