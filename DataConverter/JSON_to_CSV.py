# coding: utf-8
import os
import sys
import json
import csv


# return filenames as list
def GetFilenames(foldername):
    for folderName, subFolders, fileNames in os.walk(foldername):
        fileNames = filter(lambda filename: filename.endswith('.txt'), fileNames)
        fileNames = map(lambda filename: str(foldername + '/' + filename), fileNames)
        return list(fileNames)


# Save the dictionary values to file
def DicSaveToCSV(fileName, myDic):
    with open(fileName + '.csv', 'a') as f:
        w = csv.DictWriter(f, myDic.keys())
        w.writerow(myDic)


# Parsing JSON file, return as list(if returnList != 0), save to csv file(if saveCSV != 0)
def ParseJson(textFilePath, returnList, saveCSV):
    # Read file
    tweets_file = open(textFilePath, "r")

    # Parsing JSON
    tweets_data = []
    for line in tweets_file:
        try:
            all_data = json.loads(line)
            text = all_data['text'].encode('utf8')
            date = all_data['created_at'].encode('utf8')
            user = all_data["user"]["screen_name"].encode('utf8')
            tags = map(lambda tag: tag['text'],
                       all_data['entities']['hashtags'])

            # if tweet has no tags, check quoted tweets tag
            if len(tags) == 0:
                text = text + '. ' + all_data['quoted_status']['text'].encode('utf8')

                tags = map(lambda tag: tag['text'],
                           all_data['quoted_status']['entities']['hashtags'])

            # if still has no tags
            if len(tags) == 0:
                tags = ['no_tags']

            data_featured = {'text': text,
                             'date': date,
                             'user': user,
                             'tags': ','.join(map(lambda tag: tag.lower(), tags))}
            tweets_data.append(data_featured)

            # add to CSV file
            if(saveCSV):
                DicSaveToCSV(textFilePath, data_featured)

        except:
            continue

    tweets_file.close()

    if(returnList):
        return tweets_data


if __name__ == '__main__':
    # Change the weeknumber
    weeknumber = int(sys.argv[1])

    # Change home directory
    pathData = "/Users/Bya/Dropbox/Research/datas/"
    os.chdir(pathData)

    filenames = GetFilenames('GW' + str(weeknumber))
    for filename in filenames:
        ParseJson(filename, 0, 1)
