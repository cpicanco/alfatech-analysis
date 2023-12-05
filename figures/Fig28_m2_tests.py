import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

from colors import color1
from databases.students import students
from databases import MODULE2, ACOLE1, ACOLE2

from methods import statistics_from_blocks, output_path
from Fig27_m1_tests import plot_blocks_pairs

def boxplot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=2, color='black')
    medianprops = dict(linewidth=2, color='black')

    bp = ax.boxplot(data, positions=bar_positions, widths=0.6, sym='o', boxprops=boxprops, medianprops=medianprops)

    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')

def plot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    bar_values, bar_stds, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks)

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    bars = ax.bar(bar_positions, bar_values, color=color1)

    ax.set_xticks(bar_positions + 0.4)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')


def bar_plot(students, use_boxplot, filename):
    ACOLE_1 = ACOLE1.create()
    ACOLE_2 = ACOLE2.create()
    MODULE_2 = MODULE2.create()
    for student in students:
        if len(student.acoles) > 1:
            if student.modules[1] is not None:
                if student.has_m2:
                    for block, student_block in zip(ACOLE_1.blocks, student.acoles[0].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

                    for block, student_block in zip(ACOLE_2.blocks, student.acoles[1].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

                    for block, student_block in zip(MODULE_2.blocks, student.modules[1].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])
    regular_acole_label = 'ACOLE\nRegulares\nCV'
    difficult_acole_label = 'ACOLE\nDificuldades'
    ACOLE_1.LEITURA.legend = regular_acole_label
    ACOLE_2.LEITURA.legend = regular_acole_label
    ACOLE_1.LEITURA_DIFICULDADES.legend = difficult_acole_label
    ACOLE_2.LEITURA_DIFICULDADES.legend = difficult_acole_label
    ACOLE_1.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE_2.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE_1.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    ACOLE_2.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    ACOLE_1.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE_2.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE_1.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    ACOLE_2.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label

    # Get the data from
    reading = [
        ACOLE_1.LEITURA,
        ACOLE_2.LEITURA,
        ACOLE_1.LEITURA_DIFICULDADES,
        ACOLE_2.LEITURA_DIFICULDADES]

    composition = [
        ACOLE_1.DITADO_COMPOSICAO,
        ACOLE_2.DITADO_COMPOSICAO,
        ACOLE_1.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE_2.DITADO_COMPOSICAO_DIFICULDADES]

    manuscript = [
        ACOLE_1.DITADO_MANUSCRITO,
        ACOLE_2.DITADO_MANUSCRITO,
        ACOLE_1.DITADO_MANUSCRITO_DIFICULDADES,
        ACOLE_2.DITADO_MANUSCRITO_DIFICULDADES]

    # Get the data for the big axis
    module_2 = [block for block in MODULE_2.blocks if block.min_trials == 0]

    fig = plt.figure(figsize=(8, 8))
    fig.set_dpi(300)
    gs = GridSpec(2, 3, height_ratios=[1.5, 1.5], width_ratios=[1, 1, 1])

    # Create three axes on the top row
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)
    ax3 = fig.add_subplot(gs[0, 2], sharey=ax1)

    # Create a larger axis at the bottom that spans all three columns
    ax_big = fig.add_subplot(gs[1, :], sharey=ax1)

    ax1.set_ylabel('Porcentagem média de acertos')
    ax_big.set_ylabel('Porcentagem média de acertos')
    # Add content to the axes (you can customize this based on your data)
    if use_boxplot:
        boxplot_blocks(ax1, reading, 'Leitura')
        boxplot_blocks(ax2, composition, 'Ditado por composição')
        boxplot_blocks(ax3, manuscript, 'Ditado manuscrito')
        boxplot_blocks(ax_big, module_2, 'Módulo 2')
    else:
        plot_blocks_pairs(ax1, reading, 'Leitura')
        plot_blocks_pairs(ax2, composition, 'Ditado por composição')
        plot_blocks_pairs(ax3, manuscript, 'Ditado manuscrito')
        plot_blocks(ax_big, module_2, 'Módulo 2')

    fig.tight_layout()
    plt.tight_layout()
    if use_boxplot:
        figure_name = filename+'_boxplot'
    else:
        figure_name = filename
    plt.savefig(output_path(figure_name), bbox_inches='tight')
    plt.close()

def plot():
    """
    Porcentagem média de acertos na ACOLE inicial
    testes de Módulo 2 (completo) e ACOLE final
    """
    filename = 'Fig28_m2_testes'
    bar_plot(students, use_boxplot=False, filename=filename)
    bar_plot(students, use_boxplot=True, filename=filename)

if __name__ == "__main__":
    plot()