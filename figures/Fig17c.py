import matplotlib.pyplot as plt
import numpy as np

from databases import ACOLE1, ACOLE2, ACOLE3
from methods import statistics_from_blocks, histogram, opt
from colors import color1, color2, color_median
from base import default_axis_config, upper_summary
from Fig17 import top_labels

def boxplot_blocks(ax, blocks, data='percentages'):
    default_axis_config(ax)
    bar_positions = np.arange(len(blocks))*0.8 + 0.8
    bar_width = 0.4
    data_values = [[p for p in block.data[data] if p is not None] for block in blocks]
    data_labels = [block.legend for block in blocks]
    for d, label in zip(data_values[0:3], data_labels[0:3]):
        histogram(d, top_labels[0]+'_'+label)

    for d, label in zip(data_values[3:6], data_labels[3:6]):
        histogram(d, top_labels[1]+ '_'+label)

    values, _, lenghts, medians, _, _ = statistics_from_blocks(blocks)

    positions1 = bar_positions[0:3]
    positions2 = bar_positions[3:6]+bar_width
    values1 = values[0:3]
    values2 = values[3:6]

    boxprops = dict(linewidth=1, color='black')
    medianprops = dict(linewidth=1, color=color_median)

    bp1 = ax.boxplot(data_values[0:3], positions=positions1,
                    patch_artist=True,
                    sym='o',
                    widths=bar_width, boxprops=boxprops, medianprops=medianprops)
    bp2 = ax.boxplot(data_values[3:6], positions=positions2,
                    patch_artist=True,
                    sym='o',
                    widths=bar_width, boxprops=boxprops, medianprops=medianprops)

    colors = [color1, color2]
    for i, bplot in enumerate([bp1, bp2]):
        color = colors[i % len(colors)]  # Ensure colors repeat if there are more boxes than colors
        for patch in bplot['boxes']:
            patch.set_facecolor(color)

    # set y axis title
    ax.set_ylabel('Porcentagem média de acertos')
    ax.set_xlabel('--Atividades--')

    x_labels = [block.legend.replace('Ditado ', 'Ditado\n').replace('por ', 'por\n').replace('*', '') for block in blocks]
    bar_positions = np.concatenate((positions1, positions2), axis=0)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(x_labels, fontsize=8)


    bar_values = np.concatenate((values1, values2), axis=0)
    lenghts = np.concatenate((lenghts[0:3], lenghts[3:6]), axis=0)
    medians = np.concatenate((medians[0:3], medians[3:6]), axis=0)
    y_pos = 140
    for i, p in enumerate(bar_positions):
        x_pos = p
        if i == 1:
            ax.text(x_pos, y_pos, top_labels[0], va='top', ha='center', color='black', fontsize=10)
        if i == 4:
            ax.text(x_pos, y_pos, top_labels[1], va='top', ha='center', color='black', fontsize=10)

    upper_summary(ax, bar_positions, bar_values, medians, lenghts)


def plot_blocks(ax, blocks):
    bar_positions = np.arange(len(blocks))*0.8 + 0.8
    bar_width = 0.4
    # data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    # boxprops = dict(linewidth=1, color='black')
    # medianprops = dict(linewidth=1, color='black')

    values, _, lenghts, medians, _, _ = statistics_from_blocks(blocks)

    default_axis_config(ax)

    positions1 = bar_positions[0:3]
    positions2 = bar_positions[3:6]+bar_width
    values1 = values[0:3]
    values2 = values[3:6]

    bars = ax.bar(positions1, values1, width=bar_width, color=color1)
    for bar, median in zip(bars, medians[0:3]):
        ax.hlines(median, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color='gray')
    bars = ax.bar(positions2, values2, width=bar_width, color=color2)
    for bar, median, i in zip(bars, medians[3:6], np.arange(0,len(medians[3:6])+1)):
        if i == 0:
            ax.hlines(median, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color=color_median, label='Mediana')
        else:
            ax.hlines(median, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color=color_median)

    # set y axis title
    ax.set_ylabel('Porcentagem média de acertos')
    ax.set_xlabel('--Atividades--')

    x_labels = [block.legend.replace('Ditado ', 'Ditado\n').replace('por ', 'por\n').replace('*', '') for block in blocks]
    bar_positions = np.concatenate((positions1, positions2), axis=0)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(x_labels, fontsize=8)

    # concatenate the two numpy arrays

    bar_values = np.concatenate((values1, values2), axis=0)
    lenghts = np.concatenate((lenghts[0:3], lenghts[3:6]), axis=0)
    medians = np.concatenate((medians[0:3], medians[3:6]), axis=0)
    y_pos = 140
    for i, p in enumerate(bar_positions):
        x_pos = p
        if i == 1:
            ax.text(x_pos, y_pos, top_labels[0], va='top', ha='center', color='black', fontsize=10)
        if i == 4:
            ax.text(x_pos, y_pos, top_labels[1], va='top', ha='center', color='black', fontsize=10)

    upper_summary(ax, bar_positions, bar_values, medians, lenghts)

def bar_plot(ACOLE, filename, use_boxplot=False):
    opt.set_filename(filename)
    fig, axs = plt.subplots(1, 1, sharey=True)
    fig.set_size_inches(5, 5.5)
    fig.set_dpi(100)
    # fig.suptitle(title)

    # Group 1 - Regular Blocks
    blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO,
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    if use_boxplot:
        boxplot_blocks(axs, blocks)
    else:
        plot_blocks(axs, blocks)
        handles, labels = axs.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(1.1, 0.5), ncol=1)

    plt.tight_layout()
    plt.savefig(opt.output_path(), bbox_inches='tight')
    # plt.show()
    plt.close()

def plot():
    # Porcentagem média de acertos da primeira ACOLE com palavras regulares e com dificuldades ortográficas
    bar_plot(ACOLE1, 'Fig17c_acole1')
    bar_plot(ACOLE2, 'Fig17c_acole2')
    bar_plot(ACOLE3, 'Fig17c_acole3')
    bar_plot(ACOLE1, 'Fig17c_acole1_boxplot', use_boxplot=True)
    bar_plot(ACOLE2, 'Fig17c_acole2_boxplot', use_boxplot=True)
    bar_plot(ACOLE3, 'Fig17c_acole3_boxplot', use_boxplot=True)

if __name__ == "__main__":
    plot()