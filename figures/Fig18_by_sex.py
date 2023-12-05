import matplotlib.pyplot as plt

from databases import ACOLE1
from methods import statistics_from_block, output_path
from base import upper_summary, default_axis_config
from Fig17 import top_labels
from colors import color_median

def plot_blocks(ax, grouped_data, title, write_start_annotation=False):
    num_age_groups = len(grouped_data[0])  # Assuming all age groups have the same number of blocks
    num_blocks = len(grouped_data)

    bar_width = 0.7  # Adjust the width based on your preference
    bar_positions = []
    positions = []
    values = []
    lengths = []
    medians = []
    for i, block_group in enumerate(grouped_data):
        for j, age_block in enumerate(block_group):
            bar_position = (i*1.3) + (i * num_blocks + j) * bar_width
            bar_values, _, bar_length, bar_median, _, _ = statistics_from_block(age_block)
            # save qq plot for visual inspection
            # qq_plot(age_block, filename+'_'+str(age_block.age_group))
            if j == 0:
                bar_positions.append(bar_position)

            if i == 0:
                bars = ax.bar(bar_position, bar_values, width=bar_width-0.05, label='Meninas' if age_block.sex == 'F' else 'Meninos', color=f'C{j}')
            else:
                bars = ax.bar(bar_position, bar_values, width=bar_width-0.05, color=f'C{j}')
            ax.hlines(bar_median, bars[0].get_x(), bars[0].get_x() + bars[0].get_width(), linestyles='solid', color=color_median)

            positions.append(bar_position)
            values.append(bar_values)
            lengths.append(bar_length)
            medians.append(bar_median)

    upper_summary(ax, positions, values, medians, lengths, x=-0.5, show_label=write_start_annotation)

    ax.set_title(title, va='top', y=1.3)
    default_axis_config(ax)

    # Set x-axis ticks and labels
    bar_positions = [ i+(bar_width*num_age_groups/2) - (bar_width/2) for i in bar_positions]
    ax.set_xticks(bar_positions)
    x_labels = [block[0].legend.replace('Ditado ', 'Ditado\n').replace('por ', 'por\n').replace('*', '') for block in grouped_data]
    ax.set_xticklabels(x_labels)

def bar_plot(ACOLE, filename):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(10, 5)
    fig.set_dpi(100)

    sexes = ['F', 'M']

    all_data = [ACOLE.by_sex(sex) for sex in sexes]

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
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.04), ncol=len(sexes))
    fig.text(0.5, -0.05, 'Ano escolar', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
    Porcentagem média de acertos da primeira ACOLE
    com palavras regulares e com dificuldades ortográficas, por ano escolar
"""
def plot():
    filename = 'Fig18_sexo'
    bar_plot(ACOLE1, filename)
    # ACOLE1.summary()

if __name__ == "__main__":
    plot()