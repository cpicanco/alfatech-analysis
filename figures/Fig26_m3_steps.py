import matplotlib.pyplot as plt
import numpy as np

from databases import MODULE3
from methods import statistics_from_blocks, output_path

from base import upper_summary_2

def boxplot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['sessions'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=2, color='black')
    medianprops = dict(linewidth=2, color='black')

    bp = ax.boxplot(data, positions=bar_positions, widths=0.6, showfliers=False, boxprops=boxprops, medianprops=medianprops)

    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')

def plot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    bar_values, bar_stds, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks, 'sessions')

    ax.set_ylim(0, 3)
    ax.set_title(title, y=1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    ax.bar(bar_positions, bar_values)

    ax.set_xticks(bar_positions + 0.4)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')

    return bar_positions, bar_lengths, maxs, mins


def bar_plot(MODULE1, filename):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(10, 5)
    fig.set_dpi(100)

    axs[0].set_ylabel('Número médio de sessões')
    complete = [block for block in MODULE1.by_completion(True).blocks if block.min_trials < 0]
    bar_positions, bar_lengths, maxs, mins = plot_blocks(axs[0], complete, 'Completo')
    upper_summary_2(axs[0], bar_positions, bar_lengths, mins, maxs,
                     x=-0.5, y=3.45, line_height=0.15, show_label=True, show_n=False)

    incomplete = [block for block in MODULE1.by_completion(False).blocks if block.min_trials < 0]
    bar_positions, bar_lengths, maxs, mins = plot_blocks(axs[1], incomplete, 'Incompleto')
    upper_summary_2(axs[1], bar_positions, bar_lengths, mins, maxs,
                     x=-0.5, y=3.45, line_height=0.15, show_label=False)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
Número médio de sessões dos passos do módulo 3
completo e incompleto'
"""

def plot():
    bar_plot(MODULE3, 'Fig26_m3_passos')

if __name__ == "__main__":
    plot()