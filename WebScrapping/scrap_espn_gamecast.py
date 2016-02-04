from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import sys

sys.path.append("/Users/Bya/git/predictEPL/config/")
import names


# Scrap ESPN's soccer live commentary report
# input: url
# output: Comment Status DF
# see the matches: http://www.espnfc.us/barclays-premier-league/23/scores
# output: dataframe, columns: ['minute', 'comment', 'side', 'comment_status']
# side : 'home', 'away', 'both', 'neutral'
# comment_status : 'corner', 'foul', 'goal', 'attemp', 'freekick', 'delay'
#                  'offside', 'substitution', 'yellow_card', 'red_card', 'neutral'

# input: url
# output: home & away team names, HTML text file
def ScrapEspnMatch(url):
    # time measure
    start_time = time.time()

    # Request to URL
    # if failed return nothing
    res = requests.get(url)
    if res.status_code != 200:
        print("[Scrap Failed]: %s" % (res.status_code))
        return

    # parse to html text
    soup = BeautifulSoup(res.text, 'html.parser')

    # Extract Home & Away team names, and change them
    title = soup.title.string
    home_team = title.split(' v ')[0]
    away_team = title.split(' v ')[1].split(' live ')[0]
    home_team = names.ChangeESPNTeamName(home_team)
    away_team = names.ChangeESPNTeamName(away_team)
    print("[Match]: %s VS %s" % (home_team, away_team))

    # print passes time
    print("[Scrap Done]: %.2f sec" % (time.time() - start_time))

    return home_team, away_team, soup


# check text include team's names
def WhichSide(text, home_team, away_team):
    text = str(text).lower()
    home_team = home_team.lower()
    away_team = away_team.lower()

    if home_team in text and away_team in text:
        return 'both'
    elif home_team in text:
        return 'home'
    elif away_team in text:
        return 'away'
    else:
        return 'neutral'


# check text's meaning
def CommentStatus(text):
    text = str(text).lower()

    if text[0:6] == 'corner':
        return 'corner'
    elif text[0:4] == 'foul':
        return 'foul'
    elif text[0:4] == 'goal' or text[0:8] == 'own goal':
        return 'goal'
    elif text[0:6] == 'attemp':
        return 'attemp'
    elif "wins a free kick" in text:
        return 'freekick'
    elif text[0:7] == 'offside':
        return 'offside'
    elif text[0:12] == 'substitution':
        return 'substitution'
    elif 'yellow card' in text:
        return 'yellow_card'
    elif 'red card' in text:
        return 'red_card'
    elif text[0:5] == 'delay':
        return 'delay'
    else:
        return 'neutral'


# Scrap ESPN's soccer live commentary report
# input: url
# output: Comment Status DF
def CreateEspnLiveCommentDF(url):

    home_team, away_team, soup = ScrapEspnMatch(url)

    timestamps = soup.findAll("div", {"class": "timestamp"})
    comments = soup.findAll("div", {"class": "comment"})

    dfComments = pd.DataFrame()
    dfComments['minute'] = [timestamps[-i-1].string[:-1] for i in range(len(timestamps))]
    dfComments['comment'] = [comments[-i-1].string for i in range(len(comments))]

    dfComments['side'] = [WhichSide(comment, home_team, away_team) for comment in dfComments['comment']]
    dfComments['comment_status'] = [CommentStatus(comment) for comment in dfComments['comment']]

    return dfComments


# Adding Half-Time minutes
def AddHtMinute(minute):
    minute = int(minute)

    # adding HT 15 min and Referee's ET 3 min
    if minute > 45:
        minute = minute + 15 + 3
    return minute


# Extract Attacking Minutes
def AttackMinutes(dfGameCast, side):
    # filter attack comments
    attack_minutes = list(dfGameCast[
            (
                (dfGameCast.comment_status == 'corner') |
                (dfGameCast.comment_status == 'offside') |
                (dfGameCast.comment_status == 'freekick') |
                (dfGameCast.comment_status == 'attemp')
            ) & (dfGameCast.side == side)
            ]['minute'])

    # convert to integer and unique minutes
    attack_minutes = [AddHtMinute(minute) for minute in attack_minutes]
    attack_minutes = list(set(attack_minutes))
    attack_minutes.sort()

    # create dic for plot
    attacks_dic = {
        'xdata': attack_minutes,
        'types': 'k^',
        'label': u'攻撃',
    }

    return attacks_dic


# Extract Foul Minutes
def FoulMinutes(dfGameCast, side):
    # filter foul comments
    foul_minutes = list(dfGameCast[
            (dfGameCast.comment_status == 'foul') &
            (dfGameCast.side == side)
             ]['minute'])

    # convert to integer and unique minutes
    foul_minutes = [AddHtMinute(minute) for minute in foul_minutes]
    foul_minutes = list(set(foul_minutes))
    foul_minutes.sort()

    # create dic for plot
    fouls_dic = {
        'xdata': foul_minutes,
        'types': 'ks',
        'label': u'ファール',
    }

    return fouls_dic


# Extract Goal Minutes
def GoalMinutes(dfGameCast):
    goal_minutes = list(dfGameCast[dfGameCast['comment_status'] == 'goal']['minute'])

    goal_minutes = list(map(lambda minute: AddHtMinute(minute), goal_minutes))
    goal_minutes.sort()

    goals_dic = {
        'xdata': goal_minutes,
        'types': 'co',
        'label': u'ゴール',
    }

    return goals_dic


# Goal, Attack, Foul dictionaries
def CreateGAFdics(dfGameCast):
    attacks_dic_home = AttackMinutes(dfGameCast, 'home')
    attacks_dic_away = AttackMinutes(dfGameCast, 'away')

    fouls_dic_home = FoulMinutes(dfGameCast, 'home')
    fouls_dic_away = FoulMinutes(dfGameCast, 'away')

    goals_dic = GoalMinutes(dfGameCast)

    return (goals_dic,
            attacks_dic_home, attacks_dic_away,
            fouls_dic_home, fouls_dic_away)
