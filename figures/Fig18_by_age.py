import matplotlib.pyplot as plt

from databases import ACOLE1
from methods import statistics_from_block, output_path
from base import default_axis_config, upper_summary
from Fig17 import top_labels
from colors import color_median

filename = 'Fig18_idade'

def plot_blocks(ax, grouped_data, title, write_start_annotation=False):
    num_age_groups = len(grouped_data[0])  # Assuming all age groups have the same number of blocks
    num_blocks = len(grouped_data)
    ax.set_title(title, va='top', y=1.3)
    default_axis_config(ax)

    bar_positions = []
    bar_width = 0.4  # Adjust the width based on your preference
    bar_positions = []
    positions = []
    values = []
    lengths = []
    medians = []
    for i, block_group in enumerate(grouped_data):
        for j, age_block in enumerate(block_group):
            bar_position = (i*1.8) + (i * num_blocks + j) * bar_width
            bar_values, bar_std, bar_length, bar_median, _, _ = statistics_from_block(age_block)
            # save qq plot for visual inspection
            # qq_plot(age_block, filename+'_'+str(age_block.age_group))
            if j == 0:
                bar_positions.append(bar_position)

            if i == 0:
                bars = ax.bar(bar_position, bar_values, width=bar_width-0.05, label=f'{age_block.age_group}', color=f'C{j}')
            else:
                bars = ax.bar(bar_position, bar_values, width=bar_width-0.05, color=f'C{j}')
            ax.hlines(bar_median, bars[0].get_x(), bars[0].get_x() + bars[0].get_width(), linestyles='solid', color=color_median)

            # Annotate mean on top of each bar
            positions.append(bar_position)
            values.append(bar_values)
            lengths.append(bar_length)
            medians.append(bar_median)
    upper_summary(ax, positions, values, medians, lengths, x=-0.5, show_label=write_start_annotation)

    # Set x-axis ticks and labels
    bar_positions = [ i+(bar_width*num_age_groups/2) - (bar_width/2) for i in bar_positions]
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([group[0].legend.replace('Ditado ', 'Ditado\n').replace('*', '') for group in grouped_data])

def bar_plot(ACOLE):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(16, 5)
    fig.set_dpi(100)

    # 7: 3 data points
    # 8: 111 data points
    # 9: 496 data points
    # 10: 850 data points
    # 11: 685 data points
    # 12: 321 data points
    # 13: 141 data points
    # 14: 24 data points
    # 15: 6 data points
    # 19: 3 data points
    grouped_ages = [[7, 8], [9], [10], [11], [12], [13, 14, 15, 19]]

    all_data = [ACOLE.by_age(ages) for ages in grouped_ages]

    leitura = []
    ditado_composicao = []
    ditado_manuscrito = []
    leitura_dificuldades = []
    ditado_composicao_dificuldades = []
    ditado_manuscrito_dificuldades = []

    for data in all_data:
        for block in data.blocks:
            if ACOLE.LEITURA.id == block.id:
                leitura.append(block)
            elif ACOLE.DITADO_COMPOSICAO.id == block.id:
                ditado_composicao.append(block)
            elif ACOLE.DITADO_MANUSCRITO.id == block.id:
                ditado_manuscrito.append(block)
            elif ACOLE.LEITURA_DIFICULDADES.id == block.id:
                leitura_dificuldades.append(block)
            elif ACOLE.DITADO_COMPOSICAO_DIFICULDADES.id == block.id:
                ditado_composicao_dificuldades.append(block)
            elif ACOLE.DITADO_MANUSCRITO_DIFICULDADES.id == block.id:
                ditado_manuscrito_dificuldades.append(block)

    # Group 1 - Regular Blocks
    normal_blocks = [
        leitura,
        ditado_composicao,
        ditado_manuscrito]

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        leitura_dificuldades,
        ditado_composicao_dificuldades,
        ditado_manuscrito_dificuldades]

    axs[0].set_ylabel('Porcentagem média de acertos')
    plot_blocks(axs[0], normal_blocks, top_labels[0], True)
    plot_blocks(axs[1], difficult_blocks, top_labels[1].replace('\n', ' '))

    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.04), ncol=len(grouped_ages))
    fig.text(0.5, -0.05, 'Idade', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
    Porcentagem média de acertos da primeira ACOLE
    com palavras regulares e com dificuldades ortográficas, por idade
"""
def plot():
    bar_plot(ACOLE1)

if __name__ == "__main__":
    plot()