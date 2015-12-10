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

## Convert Raw Twitter Data

Extract Twitter's date, text, username, tags, status(regular tweet or retweet or quoted tweet).

```sh
$ pwd
/Users/Bya/git/predictEPL

$ python utils/convert_raw_data.py week_number

# example
$ python utils/convert_raw_data.py 14
[Converting Done]: game1_5.txt (11.53 sec)
[Converting Done]: game6.txt (22.83 sec)
[Converting Done]: game7.txt (4.88 sec)
[Converting Done]: game8.txt (0.96 sec)
[Converting Done]: game9_10.txt (14.01 sec)
```