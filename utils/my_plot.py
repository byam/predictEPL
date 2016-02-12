import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

fp_small = FontProperties(fname=r'/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc', size=14)
# red circle, red dashes, blue squares and green triangles
# point_types = ['ro', 'r--', 'bs', 'g^']

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


# plot multiple data series
def PlotLineChart(my_list_list, labels, colors, title, xlabel, ylabel,
                xlim=False, ylim=False, points=False, grid=False, vline=False,
                x_interval=False, y_interval=False,
                width=20, height=10):
    # add 0th_minute emotion
    my_list = [0] + my_list_list[0]
    # xlims, ylims
    xlim_min = 0
    xlim_max = len(my_list)
    ylim_min = 0
    ylim_max = max(my_list)

    # set plot size
    plt.figure(figsize=(width, height))
    # set subplot
    ax = plt.subplot(1, 1, 1)
    ax.grid(grid)

    # plot each lists
    for i in range(len(my_list_list)):
        # add 0th minute
        my_list = [0] + my_list_list[i]

        # create x, y datas
        xdata = np.arange(len(my_list))
        ydata = my_list

        ylim_max = max(max(ydata), ylim_max)

        # plot funtion
        plt.plot(xdata, ydata, label=labels[i], alpha=0.9, color=colors[i])

    # plotting points
    if points:
        p_i = 0
        for point in points:
            xdata = point['xdata']
            ydata = [ylim_max * (7 + p_i) / 10] * len(xdata)
            types = point['types']
            label = point['label']
            p_i += 1

            # plot points
            plt.plot(xdata, ydata, types, label=label, markersize=10, alpha=0.3)

            # plot vertical lines
            if vline:
                for x in xdata:
                    plt.axvline(x, color=types[0], alpha=0.3)

    # setted limit
    if xlim:
        xlim_min, xlim_max = xlim
        ax.set_xlim(xlim_min, xlim_max)
    if ylim:
        ylim_min, ylim_max = ylim
        ax.set_ylim(ylim_min, ylim_max)
    if x_interval:
        plt.xticks(np.arange(xlim_min, xlim_max + 1, x_interval))
    if y_interval:
        plt.yticks(np.arange(ylim_min, ylim_max + 1, y_interval))

    plt.xlabel(xlabel, fontproperties=fp_small)
    plt.ylabel(ylabel, fontproperties=fp_small)
    plt.axvline(x=48, color="orange", alpha=0.5)
    # plt.title(title)
    plt.legend(prop=fp_small, loc="upper right")


# Plotting Emolex POS3, NEG4 Categories
def Pos3Neg4(dfEmolex, goals_dic, attacks_dic, fouls_dic, title=''):
    # POS3
    PlotLineChart(
        my_list_list=[
            list(dfEmolex[categorys[0]]),
            list(dfEmolex[categorys[1]]),
            list(dfEmolex[categorys[2]]),
        ],
        labels=[categorys[0], categorys[1], categorys[2]],
        colors=[colors_el[0], colors_el[1], colors_el[2]],
        title='Emotion Lexicon POS3: [' + title + ']',
        xlabel='Minutes', ylabel='Emotion Signals',
        width=20, height=7,
        grid=True,
        x_interval=5,
        points=[goals_dic, attacks_dic, fouls_dic]
    )

    # NEG4
    PlotLineChart(
        my_list_list=[
            list(dfEmolex[categorys[3]]),
            list(dfEmolex[categorys[4]]),
            list(dfEmolex[categorys[5]]),
            list(dfEmolex[categorys[6]]),
        ],
        labels=[categorys[3], categorys[4], categorys[5], categorys[6]],
        colors=[colors_el[3], colors_el[4], colors_el[5], colors_el[6]],
        title='Emotion Lexicon NEG4: [' + title + ']',
        xlabel='Minutes', ylabel='Emotion Signals',
        width=20, height=7,
        grid=True,
        x_interval=5,
        points=[goals_dic, attacks_dic, fouls_dic]
    )


# Plotting Emolex POS3, NEG4 Categories, No Points
def Pos3Neg4NoPoints(dfEmolex, title=''):
    # POS3
    PlotLineChart(
        my_list_list=[
            list(dfEmolex[categorys[0]]),
            list(dfEmolex[categorys[1]]),
            list(dfEmolex[categorys[2]]),
        ],
        labels=[categorys[0], categorys[1], categorys[2]],
        colors=[colors_el[0], colors_el[1], colors_el[2]],
        title='Emotion Lexicon POS3: [' + title + ']',
        xlabel='Minutes', ylabel='Emotion Signals',
        width=20, height=7,
        grid=True,
        x_interval=5
    )

    # NEG4
    PlotLineChart(
        my_list_list=[
            list(dfEmolex[categorys[3]]),
            list(dfEmolex[categorys[4]]),
            list(dfEmolex[categorys[5]]),
            list(dfEmolex[categorys[6]]),
        ],
        labels=[categorys[3], categorys[4], categorys[5], categorys[6]],
        colors=[colors_el[3], colors_el[4], colors_el[5], colors_el[6]],
        title='Emotion Lexicon NEG4: [' + title + ']',
        xlabel='Minutes', ylabel='Emotion Signals',
        width=20, height=7,
        grid=True,
        x_interval=5
    )


# Plotting Emolex's selected categories
def EmolexCats(dfEmolex, emolex_cats,
        goals_dic=False, attacks_dic=False, fouls_dic=False, title=''):

    # Adding Emolex Category
    my_list_list = []
    labels = []
    colors = []
    for emolex_cat in emolex_cats:
        my_list_list.append(list(dfEmolex[emolex_cat]))
        labels.append(emolex_cat)
        colors.append(colors_el[categorys.index(emolex_cat)])

    # if no gamecast
    if not goals_dic:
        points = False
    else:
        points = [goals_dic, attacks_dic, fouls_dic]

    # Plot Line Chart
    PlotLineChart(
        my_list_list=my_list_list,
        labels=labels,
        colors=colors,
        title='Emotion Lexicon: [' + title + ']',
        xlabel='Minutes', ylabel='Emotion Signals',
        width=20, height=7,
        grid=True,
        x_interval=5,
        points=points
    )


# Plotting Emolex's selected categories
def EmolexCatsNoPoints(dfEmolex, emolex_cats, title=''):
    # Adding Emolex Category
    my_list_list = []
    labels = []
    colors = []
    for emolex_cat in emolex_cats:
        my_list_list.append(list(dfEmolex[emolex_cat]))
        labels.append(emolex_cat)
        colors.append(colors_el[categorys.index(emolex_cat)])

    # Plot Line Chart
    PlotLineChart(
        my_list_list=my_list_list,
        labels=labels,
        colors=colors,
        title='Emotion Lexicon: [' + title + ']',
        xlabel='Minutes', ylabel='Emotion Signals',
        width=20, height=7,
        grid=True,
        x_interval=5
    )
