# python modules
import os
import sys
import datetime

base_dir = os.path.abspath(__file__).rsplit("figures", 1)[0]
sys.path.append(os.path.join(base_dir))

# graphication
import matplotlib.pyplot as plt
import numpy as np

from databases import ACOLE
from methods import statistics_from_block

def plot_blocks(ax, grouped_data, title):
    num_age_groups = len(grouped_data[0])  # Assuming all age groups have the same number of blocks
    num_blocks = len(grouped_data)

    arange = np.arange(num_blocks)
    bar_width = 0.5  # Adjust the width based on your preference
    bar_positions = []
    for i, block_group in enumerate(grouped_data):
        for j, age_block in enumerate(block_group):
            bar_position = (i) + (i * num_blocks + j) * bar_width
            bar_value, bar_std, bar_length, bar_median, _, _ = statistics_from_block(age_block)

            if j == 0:
                bar_positions.append(bar_position)

            if i == 0:
                bars = ax.bar(bar_position, bar_value, width=bar_width-0.05, label=f'{age_block.age_group}', color=f'C{j}')
            else:
                bars = ax.bar(bar_position, bar_value, width=bar_width-0.05, color=f'C{j}')
            # Annotate mean on top of each bar
            x_pos = bar_position
            y_pos = bar_value + 20
            # if j % 2 == 0:
            #     y_pos = bar_value + 20  # Adjust the vertical position based on your preference
            # else:
            #     y_pos = -20

            ax.text(x_pos, y_pos, f'{bar_value:.1f}', ha='center', color='black', fontsize=9)
            ax.text(x_pos, y_pos - 5, f'{bar_median:.1f}', ha='center', color='black', fontsize=9)
            ax.text(x_pos, y_pos - 10, f'{bar_std:.1f}', ha='center', color='black', fontsize=9)
            ax.text(x_pos, y_pos - 15, f'{bar_length}', ha='center', color='black', fontsize=9)

    # x_pos = 90
    # y_pos = 90
    # ax.text(x_pos, y_pos, 'M =', ha='right', color='black')
    # ax.text(x_pos, y_pos - 5, 'Me =', ha='right', color='black')
    # ax.text(x_pos, y_pos - 10, 'σ =', ha='right', color='black')
    # ax.text(x_pos, y_pos - 15, 'n =', ha='right', color='black')

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    # Set x-axis ticks and labels
    bar_positions = [ i+(bar_width*num_age_groups/2) - (bar_width/2) for i in bar_positions]
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([group[0].legend.replace('Ditado ', 'Ditado\n').replace('*', '') for group in grouped_data])

def bar_plot_regular_difficult_groups(ACOLE):
    fig, axs = plt.subplots(3, 2, sharey=True)
    fig.set_size_inches(12, 18)
    fig.set_dpi(100)
    fig.suptitle('Porcentagem média de acertos da primeira ACOLE\ncom palavras regulares e com dificuldades ortográficas,\n por idade e encaminhamento')

    top_label = ['Palavras regulares', 'Palavras com\ndificuldades ortográficas']

    m1 = ACOLE.by_forwarding('Módulo 1')
    m2 = ACOLE.by_forwarding('Módulo 2')
    m3 = ACOLE.by_forwarding('Módulo 3')

    for i, ACOLE_by_module in enumerate([m1, m2, m3]):
        # grouped_sexes

        grouped_ages = [[7, 8, 9], [10], [11], [12, 13, 14, 15, 19]]

        all_data = [ACOLE_by_module.by_age(ages) for ages in grouped_ages]

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

        if i == 0:
            plot_blocks(axs[i, 0], normal_blocks, top_label[i])
            plot_blocks(axs[i, 1], difficult_blocks, top_label[i+1])
        else:
            plot_blocks(axs[i, 0], normal_blocks, '')
            plot_blocks(axs[i, 1], difficult_blocks, '')

    handles, labels = axs[1, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.020), ncol=len(grouped_ages))

    fig.text(0.5, 0.90,
        'Módulo 1', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, 0.62,
        'Módulo 2', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, 0.32,
        'Módulo 3', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    x_pos = .8
    y_pos = .87
    fig.text(x_pos, y_pos, '1 = média', ha='left', color='black')
    fig.text(x_pos, y_pos - 0.020, '2 = mediana', ha='left', color='black')
    fig.text(x_pos, y_pos - 0.040, '3 = desvio padrão', ha='left', color='black')
    fig.text(x_pos, y_pos - 0.060, '4 = tamanho da amostra', ha='left', color='black')

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'figures', 'Fig20.png'), bbox_inches='tight')

if __name__ == "__main__":
    bar_plot_regular_difficult_groups(ACOLE)
