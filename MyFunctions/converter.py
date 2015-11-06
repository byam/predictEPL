import os
import pandas as pd

hashPath = "/Users/Bya/git/EPLdata/"
savePath = "/Users/Bya/Dropbox/Research/datas/"


os.chdir("/Users/Bya/git/predictEPL/MyFunctions/")
from dataIO import DFtoCSV


def createTuples(weekGames):
    weekGamesTuples = []
    for i in range(len(weekGames)):
        if i % 2 == 0:
            weekGamesTuples.append((weekGames[i], weekGames[i+1]))
    return weekGamesTuples


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


def read_file_and_save_as_each_game(fileName, teams, GW):
    # teams
    home_team = teams[0]
    away_team = teams[1]

    # both team hashtags
    tags_home = Hashtags.dic[home_team]
    tags_away = Hashtags.dic[away_team]

    # read file as dataframe, and add 'side' column that shows which team's tweet it is
    dfTweets = pd.read_csv(fileName, header=None, names=['date', 'text', 'user', 'tags'])
    dfTweets['side'] = map(lambda tags: whichSide(tags, tags_home, tags_away), map(lambda tag: tag.split(','), dfTweets['tags']))

    # count tweets
    sides = ['home', 'away', 'both', 'nothing']
    numSides = map(lambda side: (side, len(dfTweets[dfTweets["side"] == side])), sides)
    print("\n %s vs %s :\n" % (home_team, away_team))
    print(numSides)

    dfHomeAwayTweets = dfTweets[(dfTweets["side"] == 'home') | (dfTweets["side"] == 'away') | (dfTweets["side"] == 'both')]
    dfHomeAwayTweets = pd.DataFrame(dfHomeAwayTweets.values, range(len(dfHomeAwayTweets)), dfHomeAwayTweets.columns)

    DFtoCSV(dfHomeAwayTweets, savePath + GW + '/SingleGames/', home_team + "_vs_" + away_team, False)


def toSeconds(string):
    try:
        string = string[-19:-11]
        hour, minute, second = map(int, string.split(':'))
        hour = hour * 3600
        minute = minute * 60

        return hour + minute + second
    except:
        return None


class Teams(object):
    def __init__(self):
        self.Bournemouth = 'Bournemouth'
        self.Arsenal = 'Arsenal'
        self.Villa = 'Villa'
        self.Chelsea = 'Chelsea'
        self.Crystal = 'Crystal'
        self.Everton = 'Everton'
        self.Leicester = 'Leicester'
        self.Liverpool = 'Liverpool'
        self.City = 'City'
        self.United = 'United'
        self.Newcastle = 'Newcastle'
        self.Norwich = 'Norwich'
        self.Southampton = 'Southampton'
        self.Stoke = 'Stoke'
        self.Sunderland = 'Sunderland'
        self.Swansea = 'Swansea'
        self.Tottenham = 'Tottenham'
        self.Watford = 'Watford'
        self.WestBromwich = 'WestBromwich'
        self.WestHam = 'WestHam'


# Englad Premier League's 20 teams hashtags
class Hashtags(object):
    dic = {
      # debug
      'debug': ['byambasuren'],

      # AFC Bournemouth
      'Bournemouth': ['#afcb', '#bournemouth'],

      # Arsenal
      'Arsenal': ['#arsenal', '#afc'],

      # Aston Villa
      'Villa': ['#avfc', '#astonvilla', '#astonvillafc', '#villafc'],

      # Chelsea
      'Chelsea': ['#cfc', '#chelsea'],

      # Crystal Palace
      'Crystal': ['#cpfc', '#crystalpalace'],

      # Everton
      'Everton': ['#efc', '#everton'],

      # Leicester City
      'Leicester': ['#lcfc', '#leicesterfc', '#leicestercity',
                    '#leicestercityfc'],

      # Liverpool
      'Liverpool': ['#lfc', '#liverpoolfc', '#livfc'],

      # Manchester City
      'City': ['#mcfc', '#manchestercity', '#mancity'],

      # Manchester United
      'United': ['#mufc', '#manchesterunited', '#manutd'],

      # Newcastle United
      'Newcastle': ['#nufc', '#newcastlefc', '#newcastleunited',
                    '#newcastleunitedfc'],

      # Norwich City
      'Norwich': ['#ncfc', '#norwichcity'],

      # Southampton
      'Southampton': ['#saintsfc', '#southamptonfc'],

      # Stoke City
      'Stoke': ['#scfc', '#stoke', '#stokecity'],

      # Sunderland
      'Sunderland': ['#safc', '#sunderlandfc'],

      # Swansea City
      'Swansea': ['#swans', '#swanseacity'],

      # Tottenham Hotspur
      'Tottenham': ['#coys', '#tottenhamfc', '#spursfc',
                    '#hotspurfc', '#tottenhamhotspurfc', '#tottenhamhotspur'],

      # Watford
      'Watford': ['#watfordfc'],

      # West Bromwich Albion
      'WestBromwich': ['#wba', '#wbafc', '#westbromwichalbion'],

      # West Ham United
      'WestHam': ['#whufc', '#westhamfc', '#westhamunited', '#westhamunitedfc',
                  '#whu'],
      }
