import os
import sys
import json
import csv
import time

RAW_DATA_PATH = "/Users/Bya/Dropbox/Research/datas/EPL/TwitterRawJsonData/"
SAVE_DATA_PATH = "/Users/Bya/Dropbox/Research/datas/EPL/ExtractedCsvData/"


# Return Directory's file names
def FolderFiles(folder, directory, ends='.txt'):
    os.chdir(directory)
    for folderName, subFolders, fileNames in os.walk(folder):
        fileNames = filter(lambda filename: filename.endswith(ends), fileNames)
        return list(fileNames)


# Filtering Twitter API
# date, text, tags, user, status
def FilterTweet(tweet):
    date = tweet['created_at']
    text = tweet['text']
    tags = list(map(lambda tag: tag['text'],
               tweet['entities']['hashtags']))
    user = tweet["user"]["screen_name"]
    status = 'tweet'

    if 'retweeted_status' in tweet:
        retweeted = tweet['retweeted_status']
        text = retweeted['text']
        tags = list(map(lambda tag: tag['text'],
           retweeted['entities']['hashtags']))
        status = 'retweet'

    elif 'quoted_status' in tweet:
        quoted = tweet['quoted_status']
        text = text + '. ' + quoted['text']
        qt_tags = list(map(lambda tag: tag['text'],
           quoted['entities']['hashtags']))
        tags = list(set(tags + qt_tags))
        status = 'quoted'

    tweet_list = [
        date,
        text,
        ','.join(map(lambda tag: tag.lower(), tags)),
        user,
        status
    ]

    return tweet_list


def SaveListAppendToCSV(path_to_save, file_name, my_list):
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)
    os.chdir(path_to_save)

    with open(file_name[:-4] + '.csv', 'a') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(my_list)


def ReadTextLineByLine(file_name, directory):
    os.chdir(directory)

    with open(file_name) as file:
        tweets = (line.rstrip() for line in file)

        # removing blank lines
        tweets = list(line for line in tweets if line)

    return tweets


def RawTweetFilterToCSV(week):
    week_folder = 'GW' + str(week)
    week_files = FolderFiles(week_folder, RAW_DATA_PATH)

    os.chdir(RAW_DATA_PATH + week_folder)

    for file_name in week_files:
        start_time = time.time()

        path_to_read = RAW_DATA_PATH + week_folder
        tweets = ReadTextLineByLine(file_name, path_to_read)

        for i in range(len(tweets)):
            try:
                tweet_all = json.loads(tweets[i])
                tweet_list = FilterTweet(tweet_all)

                path_to_save = SAVE_DATA_PATH + week_folder
                SaveListAppendToCSV(path_to_save, file_name, tweet_list)

            except ValueError:
                continue
            except KeyError:
                continue

        print("[Converting Done]: %s (%.2f sec)" % (file_name, time.time() - start_time))

if __name__ == '__main__':
    week_number = int(sys.argv[1])

    RawTweetFilterToCSV(week_number)
