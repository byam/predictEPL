import matplotlib.pyplot as plt
import numpy as np

# red circle, red dashes, blue squares and green triangles
types = ['ro', 'r--', 'bs', 'g^']


# plot single data series
def PlotLineSingleChart(my_list, label, color, title, xlabel, ylabel,
                        xlim=False, ylim=False,
                        x_interval=False, y_interval=False,
                        width=10, height=5):

    # add 0th_minute emotion
    my_list = [0] + my_list

    xdata = np.arange(len(my_list))
    ydata = my_list

    # set plot size
    plt.figure(figsize=(width, height))

    # set subplot
    ax = plt.subplot(1, 1, 1)

    # manipulate xlims, ylims
    xlim_min = 0
    xlim_max = len(my_list)

    ylim_min = 0
    ylim_max = max(my_list)

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

    # plot funtion
    plt.plot(xdata, ydata, label=label, alpha=0.5, color=color)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()


# plot multiple data series
def PlotLineMultipleChart(my_list_list, labels, colors, title, xlabel, ylabel,
                        xlim=False, ylim=False,
                        x_interval=False, y_interval=False,
                        width=20, height=10):
    # add 0th_minute emotion
    my_list = [0] + my_list_list[0]

    # set plot size
    plt.figure(figsize=(width, height))

    # set subplot
    ax = plt.subplot(1, 1, 1)

    # manipulate xlims, ylims
    xlim_min = 0
    xlim_max = len(my_list)

    ylim_min = 0
    ylim_max = max(my_list)

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

    # plot each lists
    for i in range(len(my_list_list)):
        # add 0th minute
        my_list = [0] + my_list_list[i]

        # create x, y datas
        xdata = np.arange(len(my_list))
        ydata = my_list

        # plot funtion
        plt.plot(xdata, ydata, label=labels[i], alpha=0.5, color=colors[i])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
