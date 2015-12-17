from bs4 import BeautifulSoup
import requests
import pandas as pd
import math
import sys
import time

sys.path.append("/Users/Bya/git/predictEPL/config/")
sys.path.append("/Users/Bya/git/predictEPL/utils/")

import paths
import useful_methods
import names


start_time = time.time()

# All Games Results's URL
url = "http://www.soccerstats.com/results.asp?league=england"
res = requests.get(url)
print("Status Code: ", res.status_code, "\n")

# Parse to Text
soup = BeautifulSoup(res.text, 'html.parser')
print("Page Title: ", soup.title.string, "\n")

# Extract all Gaems row
games = soup.findAll("tr", {"class": "odd"})
print("All Games: ", len(games), "\n")

# Print Time
print("[Done]: %f.2\n" % (time.time() - start_time))


def ExtractGameInfo(game):
    tds = game.findAll("td")

    # extract infos from html text
    date = tds[0].font.string
    time = tds[1].font.string

    teams = tds[2].string.strip()
    home_team = teams.split('-')[0].strip()
    away_team = teams.split('-')[1].strip()

    # change team names
    home_team = names.ChangeTeamName(home_team)
    away_team = names.ChangeTeamName(away_team)

    score_ft = tds[3].font.string
    score_ft_home = score_ft.split('-')[0].strip()
    score_ft_away = score_ft.split('-')[1].strip()

    score_ht = tds[4].string.strip()
    score_ht_home = score_ht.split('-')[0].strip()[1::]
    score_ht_away = score_ht.split('-')[1].strip()[0:-1]

    game_infos = {
        'date': date,
        'time': time,
        'home_team': home_team,
        'away_team': away_team,
        'score_ft_home': score_ft_home,
        'score_ft_away': score_ft_away,
        'score_ht_home': score_ht_home,
        'score_ht_away': score_ht_away,
    }

    return game_infos


columns = ['GW', 'date', 'time',
           'home_team', 'away_team',
           'score_ht_home', 'score_ht_away',
           'score_ft_home', 'score_ft_away']

df = pd.DataFrame(columns=columns)

for g_i in range(len(games)):
    try:
        # extract infos
        game_infos = ExtractGameInfo(games[g_i])

        # add GW
        game_infos['GW'] = str(math.floor(g_i / 10 + 1))

        # add row to df
        df.loc[g_i] = pd.Series(game_infos)
    except:
        print('GW', math.floor(g_i / 10 + 1), "'s data is not yet \n")
        break


# Save as CSV
useful_methods.DFtoCSV(df, paths.READ_PATH_GAME_INFO, 'game_infos', index=False)
print("[Saved in]: %s" % (paths.READ_PATH_GAME_INFO + 'game_infos.csv'))
