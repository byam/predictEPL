## Predict EPL
Predicting England Premier League's Outcomes Using Sentiment Analysis with Twitter.

This is my undergraduate research work.

## Keywords:

* Sentiment Analysis
* Text Mining
* Natural Language Processing (NLP)
* Machine Learning
* Big Data
* Englad Premier League Stats
* Predicting Models
* Twitter API
* Web Scrapping


## Development environment

* Python
* Jupyter Notebook
* AWS, ubuntu ec2

## Converting and Functions

* Converting to CSV

    * [Scrap Game Infos](#scrap_info)
    * [Download Raw Twitter Data from EC2 server](#download_row)
    * [Convert Raw Twitter Data](#convert_raw)
    * [Split Into Single Games](#split)
    * [Update Odds data](#odds_data)

* Functions

    * [Scrapping ESPN's Soccer Match Gamecast Live Commentary](#scrap_espn)
    * [Plot Emolex](#plot)


---
## Converting

<a name="scrap_info"></a>
### Scrap Game Infos

Update Game Infos from [here](http://www.soccerstats.com/results.asp?league=england)

```sh
$ python WebScrapping/scrap_game_infos.py

Status Code:  200

Page Title:  Premier League

All Games:  380

[Done]: 37.923777.2
GW 17 's data is not yet

[Saved in]: /Users/Bya/Dropbox/Research/datas/EPL/game_infos.csv
```

---

<a name="download_row"></a>
### Download Raw Twitter Data from EC2 server

Change the 'GW16'.

```sh
$ scp -r -i ~/.ssh/bya-aws.pem ubuntu@54.92.75.228:/home/ubuntu/datas/GW'week_number'/ ~/Dropbox/Research/datas/EPL/TwitterRawJsonData


# example
$ scp -r -i ~/.ssh/bya-aws.pem ubuntu@54.92.75.228:/home/ubuntu/datas/GW16/ ~/Dropbox/Research/datas/EPL/TwitterRawJsonData

game1.txt                                                         100%   19MB   2.4MB/s   00:08
game2_5.txt                                                       100%   57MB 718.2KB/s   01:21
game7.txt                                                         100%   85MB 902.8KB/s   01:36
game8_9.txt                                                       100%  138MB   2.1MB/s   01:07
game6.txt                                                         100%  186MB   2.1MB/s   01:27
```

---

<a name="convert_raw"></a>
### Convert Raw Twitter Data

Extract Twitter's date, text, username, tags, status(regular tweet or retweet or quoted tweet).

```sh
$ pwd
/Users/Bya/git/predictEPL

$ python utils/convert_raw_data.py week_number

# example
$ python utils/convert_raw_data.py 16
[Converting Done]: game1.txt (1.72 sec)
[Converting Done]: game2_5.txt (4.73 sec)
[Converting Done]: game6.txt (15.65 sec)
[Converting Done]: game7.txt (8.32 sec)
[Converting Done]: game8_9.txt (12.84 sec)
```

---

<a name="split"></a>
### Split Into Single Games

Add 'GW16' inside `games.py` and `csv_files.py`.

*games.py:*
```python
...

    'GW16':
        [
            ('Norwich', 'Everton'),

            ('Crystal', 'Southampton'),
            ('City', 'Swansea'),
            ('Sunderland', 'Watford'),
            ('WestHam', 'Stoke'),

            ('Bournemouth', 'United'),

            ('Villa', 'Arsenal'),

            ('Liverpool', 'WestBromwich'),
            ('Tottenham', 'Newcastle'),
        ],

...
```

*csv_files.py*
```python
...

    'GW16':
        [
            'game1.csv',

            'game2_5.csv',
            'game2_5.csv',
            'game2_5.csv',
            'game2_5.csv',

            'game6.csv',

            'game7.csv',

            'game8_9.csv',
            'game8_9.csv',
        ],

...
```

*terminal:*
```sh
$ python utils/split_single_games.py week_number

# example: only week 16
$ python utils/split_single_games.py 16

# weeks as : 4to20
$ python utils/split_single_games.py 4to22

Norwich vs Everton :

[('home', 1279), ('away', 2567), ('both', 2015), ('nothing', 34)]

 Crystal vs Southampton :

[('home', 602), ('away', 806), ('both', 492), ('nothing', 11626)]

 City vs Swansea :

[('home', 4660), ('away', 621), ('both', 2464), ('nothing', 5781)]

 Sunderland vs Watford :

[('home', 816), ('away', 954), ('both', 321), ('nothing', 11435)]

 WestHam vs Stoke :

[('home', 955), ('away', 303), ('both', 589), ('nothing', 11679)]

 Bournemouth vs United :

[('home', 2223), ('away', 37910), ('both', 4219), ('nothing', 322)]

 Villa vs Arsenal :

[('home', 4138), ('away', 11554), ('both', 4485), ('nothing', 149)]

 Liverpool vs WestBromwich :

[('home', 19639), ('away', 2268), ('both', 2625), ('nothing', 11629)]

 Tottenham vs Newcastle :

[('home', 4970), ('away', 5485), ('both', 1024), ('nothing', 24682)]
```


<a name="odds_data"></a>
### Update Odds data

* [Copy] Latest Games Odds [Here](http://www.oddsportal.com/soccer/england/premier-league/results/).
* [Paste] `config/odds_portal.py` file's top part.

---

## Functions


<a name="scrap_espn"></a>
### Scrapping ESPN's Soccer Match Gamecast Live Commentary

* See the matches: [here](http://www.espnfc.us/barclays-premier-league/23/scores)
* output: dataframe, columns: ['minute', 'comment', 'side', 'comment_status']
* side : 'home', 'away', 'both', 'neutral'
* comment_status : 'corner', 'foul', 'goal', 'attemp', 'freekick', 'delay'
              'offside', 'substitution', 'yellow_card', 'red_card', 'neutral'

Usage:
```python
import sys

# import function
sys.path.append("/Users/Bya/git/predictEPL/WebScrapping/")
sys.path.append("/Users/Bya/git/predictEPL/config/")

import espn_urls
from scrap_espn_gamecast import CreateEspnLiveCommentDF

# copy paste matches URL
# Output: Dataframe
# url = espn_urls.MatchUrl(GW, filename)
url = 'http://www.espnfc.us/gamecast/422508/gamecast.html'
dfGameCast = CreateEspnLiveCommentDF(url)
```

![espn_scrap](https://github.com/byam/predictEPL/blob/master/img/espn_scrap.png)



**Goal, Attack, Foul minutes:**

* Goal: ['goal']
* Attack: ['corner', 'offside', 'freekick', 'attemp']
* Foul: ['foul']

```python
goals_dic, attacks_dic_home, attacks_dic_away, fouls_dic_home, fouls_dic_away = scrap_espn_gamecast.CreateGAFdics(dfGameCast)
```



---

<a name="plot"></a>
### Plot Emolex

**Colors and Types**:

```python
# red circle, red dashes, blue squares and green triangles
point_types = ['ro', 'r--', 'bs', 'g^']

# Emolex Category and Colors
categorys = [
    'joy', 'trust', 'anticipation',
    'anger', 'fear', 'disgust', 'sadness',
    'surprise',
    'positive', 'negative',
]
colors_el = [
    '#fadb4d', '#99cc33', '#f2993a',
    '#e43054', '#35a450', '#9f78ba', '#729dc9',
    '#3fa5c0',
    'lime', 'saddlebrown',
]
```

**my_plot.PlotLineChart**:

```python
import sys

# import function
sys.path.append("/Users/Bya/git/predictEPL/utils/")
import my_plot


# Plot Line Chart as data series
my_plot.PlotLineChart(
    my_list_list=[
        [1, 4, 9, 16, 25],
    ],
    labels=categorys,
    colors=colors,
    title='Square',
    xlabel='x data',
    ylabel='y data',
    width=20,
    height=10,
    grid=True,
    vline=False,
    xlim=False,
    ylim=False,
    x_interval=False,
    y_interval=False,
    points=False,
)
```

Example:

```python
my_plot.PlotLineChart(
    my_list_list=[
        list(dfFilterEmolexHome[categorys[0]]),     # Emolex DF
        list(dfFilterEmolexHome[categorys[1]]),
        list(dfFilterEmolexHome[categorys[2]]),
    ],
    labels=categorys,
    colors=[
        colors_el[0],
        colors_el[1],
        colors_el[2],
    ],
    title='Emotion Lexicon' + ' Home Team',
    xlabel='Minutes',
    ylabel='Emotion Signal',
    width=20,
    height=10,
    grid=True,
    vline=False,
    xlim=False,
    ylim=False,
    x_interval=False,
    y_interval=False,
    points=[goals_dic, attacks_dic_home, fouls_dic_home],   # ESPN Gamecast minutes
)
```

![plot_emolex](https://github.com/byam/predictEPL/blob/master/img/plot_emolex.png)


**my_plot.HomeAwayPos3Neg4**

```python
my_plot.Pos3Neg4(dfFilterEmolexNonRtAway, goals_dic, attacks_dic_away, fouls_dic_away, title='Away')
```

![plot_pos3neg4](https://github.com/byam/predictEPL/blob/master/img/plot_pos3neg4.png)


**my_plot.EmolexCats**

```python
my_plot.EmolexCats(dfFilterEmolexNonRtAway, ['joy', 'anger', 'surprise'], goals_dic, attacks_dic_away, fouls_dic_away, 'Away')
```

![plot_cats](https://github.com/byam/predictEPL/blob/master/img/plot_cats.png)

---












* Logistic Regressionがこの場合使える。Too Simple Model
Decision Tree, SVMがデータが多くなると精度が上がる。If input become difficult, Accuracy Up.

* Historical Data(Last Year Rank, Goal Rate)
* Current Year Data

































