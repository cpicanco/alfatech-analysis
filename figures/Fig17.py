import matplotlib.pyplot as plt
import numpy as np

from databases import ACOLE1, ACOLE2, ACOLE3
from methods import statistics_from_blocks, output_path
from base import default_axis_config
from colors import color_median

top_labels = ['Palavras\nregulares - CV', 'Palavras com\ndificuldades ortográficas']

def boxplot_blocks(ax, blocks):
    default_axis_config(ax)
    ax.set_ylabel('Porcentagem de acertos')

    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=2, color='black')
    medianprops = dict(linewidth=2, color='black')

    bp = ax.boxplot(data, positions=bar_positions, widths=0.6, showfliers=False, boxprops=boxprops, medianprops=medianprops)

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

def plot_blocks(ax, blocks):
    default_axis_config(ax)

    bar_positions = np.arange(len(blocks))

    bar_values, bar_stds, bar_lengths, bar_medians, _, _ = statistics_from_blocks(blocks)

    bars = ax.bar(bar_positions, bar_values)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n') for block in blocks])

     # Annotate mean and sigma on top of each column
    for bar, value, position, std, blen, bme in zip(bars, bar_values, bar_positions, bar_stds, bar_lengths, bar_medians):
        x_pos = bar.get_x() + bar.get_width() / 2
        y_pos = value + 20
        ax.text(x_pos, y_pos - 15, f'N = {blen}', ha='center', color='black')
        ax.text(x_pos, y_pos, f'M={value:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 5, f'Me = {bme:.1f}', ha='center', color='black')
        ax.hlines(bme, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color=color_median)

def bar_plot(ACOLE, filename, title, y_padding=1.2):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(8, 5)
    fig.set_dpi(100)
    fig.suptitle(title)

    # Group 1 - Regular Blocks
    normal_blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO]

    axs[0].set_ylabel('Porcentagem média de acertos')
    axs[0].set_title(top_labels[0], y=y_padding)
    plot_blocks(axs[0], normal_blocks)

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    axs[1].set_title(top_labels[1], y=y_padding)
    plot_blocks(axs[1], difficult_blocks)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

def plot():
    bar_plot(ACOLE1, 'Fig17_acole1',
        'Porcentagem média de acertos da primeira ACOLE\ncom palavras regulares e com dificuldades ortográficas',
        1.0)
    bar_plot(ACOLE2, 'Fig17_acole2',
        'Porcentagem média de acertos da segunda ACOLE\ncom palavras regulares e com dificuldades ortográficas',
        1.2)
    bar_plot(ACOLE3, 'Fig17_acole3',
        'Porcentagem média de acertos da terceira ACOLE\ncom palavras regulares e com dificuldades ortográficas',
        1.2)

if __name__ == "__main__":
    plot()