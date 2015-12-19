import matplotlib.pyplot as plt
import numpy as np

# red circle, red dashes, blue squares and green triangles
# point_types = ['ro', 'r--', 'bs', 'g^']

# Emolex Category and Colors
# categorys pos = ['joy', 'trust', 'anticipation']
# colors pos = ['#fadb4d', '#99cc33', '#f2993a']
# categorys neg = ['anger', 'fear', 'disgust', 'sadness']
# colors neg = ['#e43054', '#35a450', '#9f78ba', '#729dc9']


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
            plt.plot(xdata, ydata, types, label=label, markersize=10, alpha=0.1)

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

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
