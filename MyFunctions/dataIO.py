import pandas as pd
import os
import csv


# read csv, return as datafrane
# ex: CSVreturnDF(filepathName, ['date', 'text', 'user', 'tags'])
def CSVtoDF(filepathName, listHeaderNames=None):
    if listHeaderNames is None:
        df = pd.read_csv(filepathName)
    else:
        df = pd.read_csv(filepathName, header=None, names=listHeaderNames)
    return df


# save df to csv file.
def DFtoCSV(df, pathToSave, fileName, index=True):
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)

    os.chdir(pathToSave)

    df.to_csv(fileName + '.csv', sep=',', encoding='utf-8', index=index)


# Save the list values to CSV. Append
def ListSaveToCSVappend(myList, fileName, filepathName):
    os.chdir(filepathName)
    with open(fileName + '.csv', 'a') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(myList)
