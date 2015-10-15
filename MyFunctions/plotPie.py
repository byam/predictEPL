# Standard Library
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy

# Custom Library
os.chdir('/Users/Bya/git/predictEPL/')
from MyFunctions import dataIO


def DFaddcolumnsFTHT(df):
    df['FT(H)'] = map(lambda x: int(x.split('-')[0]), df['FT'])
    df['FT(A)'] = map(lambda x: int(x.split('-')[1]), df['FT'])
    df['HT(H)'] = map(lambda x: int(x.split('-')[0]), df['HT'])
    df['HT(A)'] = map(lambda x: int(x.split('-')[1]), df['HT'])
    return df


# detect conditions on HT and FT
# (1)HT: Home > Away ==> FT: Home > Away 'HH'
# (2)HT: Home > Away ==> FT: Home = Away 'HD'
# (3)HT: Home > Away ==> FT: Home < Away 'HA'

# (4)HT: Home = Away ==> FT: Home > Away 'DH'
# (5)HT: Home = Away ==> FT: Home = Away 'DD'
# (6)HT: Home = Away ==> FT: Home < Away 'DA'

# (7)HT: Home < Away ==> FT: Home > Away 'AH'
# (8)HT: Home < Away ==> FT: Home = Away 'AD'
# (9)HT: Home < Away ==> FT: Home < Away 'AA'
def CompareFTHT(row):
    HThome = row[1]['HT(H)']
    HTaway = row[1]['HT(A)']
    FThome = row[1]['FT(H)']
    FTaway = row[1]['FT(A)']

    condition = ''

    # home team wins till HT
    if HThome > HTaway and FThome > FTaway:
        condition = 'HH'
    elif HThome > HTaway and FThome == FTaway:
        condition = 'HD'
    elif HThome > HTaway and FThome < FTaway:
        condition = 'HA'

    # draw till HT
    elif HThome == HTaway and FThome > FTaway:
        condition = 'DH'
    elif HThome == HTaway and FThome == FTaway:
        condition = 'DD'
    elif HThome == HTaway and FThome < FTaway:
        condition = 'DA'

    # away team wins till HT
    elif HThome < HTaway and FThome > FTaway:
        condition = 'AH'
    elif HThome < HTaway and FThome == FTaway:
        condition = 'AD'
    elif HThome < HTaway and FThome < FTaway:
        condition = 'AA'

    return condition


def CountConditions(df):
    listConditions = ['HH', 'HD', 'HA', 'DH', 'DD', 'DA', 'AH', 'AD', 'AA']
    dicConditions = {}
    for condition in listConditions:
        dicConditions[condition] = len(filter(lambda x:
                                              x == condition, df['condition']))

    return dicConditions


def PlotPieCondtions(dicConditions, title):
    # The slices will be ordered and plotted counter-clockwise.
    keys = dicConditions.keys()
    values = dicConditions.values()
    colors = ['orangered', 'chocolate', 'peru',
              'dimgrey', 'darkgrey', 'lightgrey',
              'palegreen', 'lightsage', 'greenyellow']
    # explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)

    fig = plt.figure(1, figsize=(10, 7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # plt.title('2014/2015')
    fig.suptitle(title, fontsize=15)

    patches, texts, autotexts = ax.pie(values,
                                       labels=keys,
                                       colors=colors,
                                       # explode=explode,
                                       autopct='%1.1f%%',
                                       # shadow=True,
                                       startangle=180)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    percent = map(lambda value: 100.0 * float(value) / sum(values), values)
    labels = ['{0} - {1:1.2f} %- {2} matches'.format(i, j, k) for i, j, k in zip(keys, percent, values)]
    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, values),
                                              key=lambda keys: keys[2],
                                              reverse=True))
    plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.1, 1.), fontsize=15)

    plt.show()


def PlotPieDic3(dicConditions, title):
    # The slices will be ordered and plotted counter-clockwise.
    keys = dicConditions.keys()
    values = dicConditions.values()
    colors = ['orangered',
              'dimgrey', 
              'palegreen']
    # explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)

    fig = plt.figure(1, figsize=(10,7))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    # plt.title('2014/2015')
    fig.suptitle(title, fontsize=15)

    patches, texts, autotexts  = ax.pie(values,
                                       labels=keys,
                                       colors=colors,
                                #        explode=explode,
                                       autopct='%1.1f%%',
                                #        shadow=True, 
                                       startangle=180)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')


    percent = map(lambda value: 100.0 * float(value) / sum(values), values)
    labels = ['{0} - {1:1.2f} %- {2} matches'.format(i,j,k) for i,j,k in zip(keys, percent, values)]
    sort_legend = True
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, values),
                                              key=lambda keys: keys[2],
                                              reverse=True))
    plt.legend(patches, labels, loc='left center', bbox_to_anchor=(-0.1, 1.), fontsize=15)


    plt.show()


def DicConditionsAndPlotPie(df, title, addColumn=None):
    if addColumn is None:
        # split FT, HT scores as Home and Away Teams
        df = DFaddcolumnsFTHT(df)

    # add columns as shows conditions
    df['condition'] = map(lambda row: CompareFTHT(row), df.iterrows())

    # conditions result as dic
    dic = CountConditions(df)

    # plot pie
    PlotPieCondtions(dic, title)

    return dic


def dicHT_HDA(dicConditions):
    dicHTresult = {}
    dicHTresult['HT: Home Wins'] = dicConditions['HH'] + dicConditions['HD'] + dicConditions['HA']
    dicHTresult['HT: Away Wins'] = dicConditions['AH'] + dicConditions['AD'] + dicConditions['AA']
    dicHTresult['HT: Draw'] = dicConditions['DH'] + dicConditions['DD'] + dicConditions['DA']
    return dicHTresult


def dicFT_HDA(dicConditions):
    dicFTresult = {}
    dicFTresult['FT: Home Wins'] = dicConditions['HH'] + dicConditions['DH'] + dicConditions['AH']
    dicFTresult['FT: Away Wins'] = dicConditions['HA'] + dicConditions['DA'] + dicConditions['AA']
    dicFTresult['FT: Draw'] = dicConditions['HD'] + dicConditions['DD'] + dicConditions['AD']
    return dicFTresult
