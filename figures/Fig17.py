# python modules
import os
import sys
import datetime

base_dir = os.path.abspath(__file__).rsplit("figures", 1)[0]
sys.path.append(os.path.join(base_dir))

# graphication
import matplotlib.pyplot as plt
import numpy as np

from databases import geic_db, ACOLE, populate_acole_data
from methods import statistics_from_blocks

def boxplot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=2, color='black')
    medianprops = dict(linewidth=2, color='black')

    bp = ax.boxplot(data, positions=bar_positions, widths=0.6, showfliers=False, boxprops=boxprops, medianprops=medianprops)

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n') for block in blocks])

    # Annotate mean, min, and max for each block
    for i, box in enumerate(bp['boxes']):
        pos = bar_positions[i]
        mean_val = np.mean(data[i])
        min_val = np.min(data[i])
        max_val = np.max(data[i])

        ax.text(pos, 95 , f'M={mean_val:.1f}%', ha='center', color='black')
        ax.text(pos, min_val - 5, f'{min_val:.1f}%', ha='center', color='black')
        ax.text(pos, max_val + 2, f'{max_val:.1f}%', ha='center', color='black')

def plot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    bar_values, bar_stds, bar_lengths, bar_medians, _, _ = statistics_from_blocks(blocks)

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    bars = ax.bar(bar_positions, bar_values)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n') for block in blocks])

     # Annotate mean and sigma on top of each column
    for bar, value, position, std, blen, bme in zip(bars, bar_values, bar_positions, bar_stds, bar_lengths, bar_medians):
        x_pos = bar.get_x() + bar.get_width() / 2
        y_pos = value + 20
        ax.text(x_pos, y_pos, f'{value:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 5, f'Me = {bme:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 10, f'σ = {std:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 15, f'n = {blen}', ha='center', color='black')


def bar_plot_regular_difficult_groups(ACOLE):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(8, 5)
    fig.set_dpi(100)
    fig.suptitle('Média da porcentagem de acertos da primeira ACOLE\ncom palavras regulares e com dificuldades ortográficas')

    # Group 1 - Regular Blocks
    normal_blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO]

    plot_blocks(axs[0], normal_blocks, 'Palavras regulares')

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    plot_blocks(axs[1], difficult_blocks, 'Palavras com\ndificuldades ortográficas')

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'figures', 'Fig17.png'), bbox_inches='tight')

if __name__ == "__main__":
    bar_plot_regular_difficult_groups(ACOLE)