import matplotlib.pyplot as plt
import numpy as np

from databases.students import students
from databases import ACOLE1
from methods import statistics_from_block, output_path
from base import default_axis_config, upper_summary
from Fig17 import top_labels
from colors import color_median

filename = 'Fig18_escola'

def plot_blocks(ax, grouped_data, title, write_start_annotation=False):
    num_schools = len(grouped_data[0])
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

    labels = []
    colors = []
    for i, block_group in enumerate(grouped_data):
        for j, block in enumerate(block_group):
            bar_position = (i*2.6) + (i * num_blocks + j) * bar_width
            bar_values, _, bar_length, bar_median, _, _ = statistics_from_block(block)
            # save qq plot for visual inspection
            # qq_plot(block, filename+'_'+str(block.school))
            if j == 0:
                bar_positions.append(bar_position)

            if i == 0:
                labels.append(block.school)

            # Annotate mean on top of each bar
            colors.append(j)
            positions.append(bar_position)
            values.append(bar_values)
            lengths.append(bar_length)
            medians.append(bar_median)

    sorted_values = []
    sorted_lengths = []
    sorted_medians = []
    for i in range(num_blocks):
        start_index = i * num_schools
        end_index = (i + 1) * num_schools

        ps = positions[start_index:end_index]
        v = values[start_index:end_index]
        l = lengths[start_index:end_index]
        m = medians[start_index:end_index]
        c = colors[start_index:end_index]

        sorted_v, sorted_l, sorted_m, sorted_cl = zip(*sorted(list(zip(v, l, m, c)), key=lambda x: x[0]))
        sorted_values.extend(sorted_v)
        sorted_lengths.extend(sorted_l)
        sorted_medians.extend(sorted_m)
        # now plot and do not forget to add labels
        for j, (p, v, l, m, cl) in enumerate(zip(ps, sorted_v, sorted_l, sorted_m, sorted_cl)):
            if i == 0:
                bars = ax.bar(p, v, width=bar_width-0.05, label=labels[j], color=f'C{cl}')
            else:
                bars = ax.bar(p, v, width=bar_width-0.05, color=f'C{cl}')
            ax.hlines(m, bars[0].get_x(), bars[0].get_x() + bars[0].get_width(), linestyles='solid', color=color_median)

    upper_summary(ax, positions, sorted_values, sorted_medians, sorted_lengths, x=-0.5, show_label=write_start_annotation)

    # Set x-axis ticks and labels
    bar_positions = [ i+(bar_width*num_schools/2) - (bar_width/2) for i in bar_positions]
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([group[0].legend.replace('Ditado ', 'Ditado\n').replace('*', '') for group in grouped_data])

def bar_plot(ACOLE):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(18, 5)
    fig.set_dpi(100)

    schools = [k for k in students.schools(True).keys()]

    all_data = [ACOLE.by_school(school) for school in schools]

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
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)
    fig.text(0.5, -0.25, 'Escolas', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
    Porcentagem média de acertos da primeira ACOLE
    com palavras regulares e com dificuldades ortográficas, por escola
"""
def plot():
    bar_plot(ACOLE1)

if __name__ == "__main__":
    plot()