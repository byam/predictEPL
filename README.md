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


---

## 0. Scrap Game Infos

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

## 1. Download Raw Twitter Data from EC2 server

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

## 2. Convert Raw Twitter Data

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


## 3. Split Into Single Games

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

# example
$ python utils/split_single_games.py 16

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


