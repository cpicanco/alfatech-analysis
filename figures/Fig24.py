import matplotlib.pyplot as plt
import numpy as np

from databases import MODULE1
from methods import statistics_from_blocks, output_path

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

    # Annotate mean, min, and max for each block
    for i, box in enumerate(bp['boxes']):
        pos = bar_positions[i]
        mean_val = np.mean(data[i])
        min_val = np.min(data[i])
        max_val = np.max(data[i])

        # ax.text(pos, 1 , f'M={mean_val:.1f}%', ha='center', color='black')
        # ax.text(pos, min_val - 0.01, f'{min_val:.1f}%', ha='center', color='black')
        # ax.text(pos, max_val + 0.01, f'{max_val:.1f}%', ha='center', color='black')

def plot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    bar_values, bar_stds, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks, 'sessions')

    ax.set_ylim(0, 3)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    bars = ax.bar(bar_positions, bar_values)

    ax.set_xticks(bar_positions + 0.4)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')
     # Annotate mean and sigma on top of each column
    return bars, bar_values, bar_positions, bar_lengths, maxs, mins


def bar_plot(MODULE1, filename, title):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(12, 5)
    fig.set_dpi(100)
    fig.suptitle(title)


    complete = [block for block in MODULE1.by_completion(True).blocks if block.min_trials < 0]
    bars, bar_values, bar_positions, bar_lengths, maxs, mins = plot_blocks(axs[0], complete, 'Completo')

    for b, v, p, _len, _max, _min in zip(bars, bar_values, bar_positions, bar_lengths, maxs, mins):
        x_pos = p
        y_pos = v + 0.4
        axs[0].text(x_pos, y_pos, f'{_max}', ha='center', color='black', fontsize=8)
        axs[0].text(x_pos, y_pos - 0.15, f'{_min}', ha='center', color='black', fontsize=8)

    axs[0].text(10, 2.8, f'n = {bar_lengths[0]}', ha='center', color='black', fontsize=10)
    axs[0].annotate(f'= máx', (x_pos+1, y_pos), ha='center', color='black', fontsize=8)
    axs[0].annotate(f'= mín', (x_pos+1, y_pos -0.15), ha='center', color='black', fontsize=8)

    incomplete = [block for block in MODULE1.by_completion(False).blocks if block.min_trials < 0]
    bars, bar_values, bar_positions, bar_lengths, maxs, mins = plot_blocks(axs[1], incomplete, 'Incompleto')
    for b, v, p, _len, _max, _min in zip(bars, bar_values, bar_positions, bar_lengths, maxs, mins):
        x_pos = p
        y_pos = v + 0.4
        axs[1].text(x_pos, 2.8, f'{_len}', ha='center', color='black', fontsize=8)
        axs[1].text(x_pos, y_pos - 0.15, f'{_max}', ha='center', color='black', fontsize=8)
        axs[1].text(x_pos, y_pos - 0.3, f'{_min}', ha='center', color='black', fontsize=8)

    axs[1].text(x_pos+1, 2.8, f'= n ', ha='center', color='black', fontsize=10)
    axs[1].annotate(f'= máx', (x_pos+1, y_pos -0.15), ha='center', color='black', fontsize=8)
    axs[1].annotate(f'= mín', (x_pos+1, y_pos -0.3), ha='center', color='black', fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

def plot():
    bar_plot(MODULE1, 'Fig24',
        'Número médio de sessões dos passos do módulo 1\ncompleto e incompleto')

if __name__ == "__main__":
    plot()