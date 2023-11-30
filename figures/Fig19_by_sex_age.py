import matplotlib.pyplot as plt

from databases import ACOLE1
from methods import statistics_from_block, output_path
from base import default_axis_config, upper_summary
from colors import color_median
from Fig17 import top_labels

def plot_blocks(ax, grouped_data, title, write_start_annotation=False):
    num_age_groups = len(grouped_data[0])
    num_blocks = len(grouped_data)

    bar_width = 0.5
    bar_positions = []
    positions = []
    values = []
    lengths = []
    medians = []
    for i, block_group in enumerate(grouped_data):
        for j, age_block in enumerate(block_group):
            bar_position = (i) + (i * num_blocks + j) * bar_width
            bar_value, _, bar_length, bar_median, _, _ = statistics_from_block(age_block)

            if j == 0:
                bar_positions.append(bar_position)

            if i == 0:
                bars = ax.bar(bar_position, bar_value, width=bar_width-0.05, label=f'{age_block.age_group}', color=f'C{j}')
            else:
                bars = ax.bar(bar_position, bar_value, width=bar_width-0.05, color=f'C{j}')
            ax.hlines(bar_median, bars[0].get_x(), bars[0].get_x() + bars[0].get_width(), linestyles='solid', color=color_median)

            positions.append(bar_position)
            values.append(bar_value)
            lengths.append(bar_length)
            medians.append(bar_median)

    ax.set_title(title, va='top', y=1.3)
    default_axis_config(ax)

    upper_summary(ax, positions, values, medians, lengths, x=-0.5, show_label=write_start_annotation)

    # Set x-axis ticks and labels
    bar_positions = [ i+(bar_width*num_age_groups/2) - (bar_width/2) for i in bar_positions]
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([group[0].legend.replace('Ditado ', 'Ditado\n').replace('*', '') for group in grouped_data])

def bar_plot(ACOLE, filename):
    fig, axs = plt.subplots(2, 2, sharey=True)
    fig.set_size_inches(12, 12)
    fig.set_dpi(100)

    # Sex F: 1051 data points
    # Sex M: 1589 data points

    # Feminine
    # Age 8: 45 data points
    # Age 9: 250 data points
    # Age 10: 313 data points
    # Age 11: 272 data points
    # Age 12: 105 data points
    # Age 13: 57 data points
    # Age 14: 6 data points
    # Age 19: 3 data points

    # Masculine
    # Age 7: 3 data points
    # Age 8: 66 data points
    # Age 9: 246 data points
    # Age 10: 537 data points
    # Age 11: 413 data points
    # Age 12: 216 data points
    # Age 13: 84 data points
    # Age 14: 18 data points
    # Age 15: 6 data points

    feminine = ACOLE.by_sex('F')
    masculine = ACOLE.by_sex('M')

    for i, ACOLE_by_sex in enumerate([feminine, masculine]):
        # grouped_sexes
        if i == 0:
            grouped_ages = [[8, 9], [10], [11], [12, 13, 14, 19]]
        else:
            grouped_ages = [[7, 8, 9], [10], [11], [12, 13, 14, 15]]
        all_data = [ACOLE_by_sex.by_age(ages) for ages in grouped_ages]

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
        axs[i, 0].set_ylabel('Porcentagem média de acertos')
        if i == 0:
            plot_blocks(axs[i, 0], normal_blocks, top_labels[i], True)
            plot_blocks(axs[i, 1], difficult_blocks, top_labels[i+1], True)
        else:
            plot_blocks(axs[i, 0], normal_blocks, ' ')
            plot_blocks(axs[i, 1], difficult_blocks, ' ')

    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.445), ncol=len(grouped_ages))

    handles, labels = axs[1, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.020), ncol=len(grouped_ages))


    fig.text(0.9, 0.8,
        'Meninas', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.9, 0.33,
        'Meninos', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, -0.04, 'Idade', ha='center', va='center', fontsize=12)

    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
Porcentagem média de acertos da primeira ACOLE
com palavras regulares e com dificuldades ortográficas,
por idade e gênero'
"""
def plot():
    bar_plot(ACOLE1, 'Fig19_idade_genero')

if __name__ == "__main__":
    plot()