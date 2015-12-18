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
    text = text.lower()
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
    text = text.lower()

    if text[0:6] == 'corner':
        return 'corner'
    elif text[0:4] == 'foul':
        return 'foul'
    elif text[0:4] == 'goal':
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
