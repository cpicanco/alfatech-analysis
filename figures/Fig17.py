import matplotlib.pyplot as plt
import numpy as np

from databases import ACOLE1, ACOLE2, ACOLE3
from methods import statistics_from_blocks, output_path
from base import default_axis_config, upper_summary
from colors import color_median

top_labels = ['Palavras\nregulares - CV', 'Palavras com\ndificuldades ortográficas']

def boxplot_blocks(ax, blocks, show_label=True, data='percentages'):
    default_axis_config(ax)
    bar_positions = np.arange(len(blocks))

    bar_values, _, bar_lengths, bar_medians, _, _ = statistics_from_blocks(blocks)
    data = [[p for p in block.data[data] if p is not None] for block in blocks]

    # add median color to the boxplot
    medianprops = dict(linestyle='solid', linewidth=1, color=color_median)
    boxprops = dict(linestyle='solid', linewidth=1, color='black')

    ax.boxplot(data,
               sym='o',
               positions=bar_positions,
               widths=0.5, boxprops=boxprops, medianprops=medianprops )
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n').replace('*', '') for block in blocks])

    upper_summary(ax, bar_positions, bar_values, bar_medians, bar_lengths, x=-0.5, show_label=show_label)

def plot_blocks(ax, blocks, show_label=True):
    default_axis_config(ax)
    bar_positions = np.arange(len(blocks))

    bar_values, _, bar_lengths, bar_medians, _, _ = statistics_from_blocks(blocks)

    bars = ax.bar(bar_positions, bar_values)
    for m, bar in zip(bar_medians, bars):
        #get x and y values
        ax.hlines(m, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color=color_median)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n').replace('*', '') for block in blocks])

    upper_summary(ax, bar_positions, bar_values, bar_medians, bar_lengths, x=-0.5, show_label=show_label)


def bar_plot(ACOLE, filename, y_padding=1.2, use_boxplot=False):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(8, 5)
    fig.set_dpi(100)

    # Group 1 - Regular Blocks
    normal_blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO]

    axs[0].set_ylabel('Porcentagem média de acertos')
    axs[0].set_title(top_labels[0], y=y_padding)
    if use_boxplot:
        boxplot_blocks(axs[0], normal_blocks)
    else:
        plot_blocks(axs[0], normal_blocks)

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    axs[1].set_title(top_labels[1], y=y_padding)
    if use_boxplot:
        boxplot_blocks(axs[1], difficult_blocks, False)
    else:
        plot_blocks(axs[1], difficult_blocks, False)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

def plot():
    bar_plot(ACOLE1, 'Fig17_acole1')
    bar_plot(ACOLE2, 'Fig17_acole2')
    bar_plot(ACOLE3, 'Fig17_acole3')
    bar_plot(ACOLE1, 'Fig17_acole1_boxplot', use_boxplot=True)
    bar_plot(ACOLE2, 'Fig17_acole2_boxplot', use_boxplot=True)
    bar_plot(ACOLE3, 'Fig17_acole3_boxplot', use_boxplot=True)

if __name__ == "__main__":
    plot()