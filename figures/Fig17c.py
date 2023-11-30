import matplotlib.pyplot as plt
import numpy as np

from databases import ACOLE1, ACOLE2, ACOLE3
from methods import statistics_from_blocks, output_path
from colors import color1, color2, color_median
from base import default_axis_config, upper_summary
from Fig17 import top_labels


def boxplot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=2, color='black')
    medianprops = dict(linewidth=2, color='black')

    bp = ax.boxplot(data, positions=bar_positions, widths=0.6, showfliers=False, boxprops=boxprops, medianprops=medianprops)

    ax.set_ylim(0, 100)
    ax.set_title(title, y=2.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    x_labels = [block.legend.replace('Ditado ', 'Ditado\n') for block in blocks][0:3]
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(x_labels)

    # Annotate mean, min, and max for each block
    for i, box in enumerate(bp['boxes']):
        pos = bar_positions[i]
        mean_val = np.mean(data[i])
        min_val = np.min(data[i])
        max_val = np.max(data[i])

        ax.text(pos, 95 , f'M={mean_val:.1f}%', ha='center', color='black')
        ax.text(pos, min_val - 5, f'{min_val:.1f}%', ha='center', color='black')
        ax.text(pos, max_val + 2, f'{max_val:.1f}%', ha='center', color='black')

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

def bar_plot(ACOLE, filename):
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

    plot_blocks(axs, blocks)
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(1.1, 0.5), ncol=1)

    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    # plt.show()
    plt.close()

def plot():
    # Porcentagem média de acertos da primeira ACOLE com palavras regulares e com dificuldades ortográficas
    bar_plot(ACOLE1, 'Fig17c_acole1')

    # Porcentagem média de acertos da segunda ACOLE com palavras regulares e com dificuldades ortográficas
    bar_plot(ACOLE2, 'Fig17c_acole2')

    # Porcentagem média de acertos da terceira ACOLE com palavras regulares e com dificuldades ortográficas
    bar_plot(ACOLE3, 'Fig17c_acole3')

if __name__ == "__main__":
    plot()