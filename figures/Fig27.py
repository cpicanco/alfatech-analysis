# python modules
import os
import sys
import datetime

base_dir = os.path.abspath(__file__).rsplit("figures", 1)[0]
sys.path.append(os.path.join(base_dir))

# graphication
import matplotlib.pyplot as plt
import numpy as np

from databases.students import students
from databases import MODULE1, ACOLE1, ACOLE2

from methods import statistics_from_blocks

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

    bar_values, bar_stds, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks)

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    bars = ax.bar(bar_positions, bar_values)

    ax.set_xticks(bar_positions + 0.4)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')


def bar_plot(ACOLE1, MODULE1, ACOLE2, use_boxplot=False):
    fig, axs = plt.subplots(3, 1, sharey=True)
    fig.set_size_inches(5, 14)
    fig.set_dpi(100)

    if use_boxplot:
        title = 'Distribuição da porcentagem de acertos na ACOLE inicial,\ntestes de Módulo 1 e ACOLE final'
    else:
        title = 'Porcentagem média de acertos na ACOLE inicial,\ntestes de Módulo 1 e ACOLE final'

    fig.suptitle(title, fontsize=14)

    ACOLE1.LEITURA.legend = 'ACOLE inicial'
    ACOLE1.LEITURA_DIFICULDADES.legend = 'ACOLE inicial - Dificuldades'
    MODULE1.EXTAI.legend = 'Módulo 1 t. ext. inicial - A'
    MODULE1.EXTBI.legend = 'Módulo 1 t. ext. inicial - B'
    MODULE1.EXTAF.legend = 'Módulo 1 t. ext. final - A'
    MODULE1.EXTBF.legend = 'Módulo 1 t. ext. final - B'
    MODULE1.EXTCI.legend = 'Módulo 1 inicial - B'
    ACOLE2.LEITURA.legend = 'ACOLE final'
    ACOLE2.LEITURA_DIFICULDADES.legend = 'ACOLE final - Dificuldades'

    acole1_reading = [ACOLE1.LEITURA, ACOLE1.LEITURA_DIFICULDADES]
    module_reading = [MODULE1.EXTAI, MODULE1.EXTBI, MODULE1.EXTAF, MODULE1.EXTBF]
    acole2_reading = [ACOLE2.LEITURA, ACOLE2.LEITURA_DIFICULDADES]
    reading = acole1_reading + module_reading + acole2_reading

    if use_boxplot:
        boxplot_blocks(axs[0], reading, 'Leitura')
    else:
        plot_blocks(axs[0], reading, 'Leitura')

    ACOLE1.DITADO_COMPOSICAO.legend = 'ACOLE inicial'
    ACOLE1.DITADO_COMPOSICAO_DIFICULDADES.legend = 'ACOLE inicial - Dificuldades'
    MODULE1.EXTDI.legend = 'Módulo 1 t. ext. inicial - A'
    MODULE1.EXTDF.legend = 'Módulo 1 t. ext. final - A'
    ACOLE2.DITADO_COMPOSICAO.legend = 'ACOLE final'
    ACOLE2.DITADO_COMPOSICAO_DIFICULDADES.legend = 'ACOLE final - Dificuldades'

    acole1_dictation = [ACOLE1.DITADO_COMPOSICAO, ACOLE1.DITADO_COMPOSICAO_DIFICULDADES]
    module_dictation = [MODULE1.EXTDI, MODULE1.EXTDF]
    acole2_dictation = [ACOLE2.DITADO_COMPOSICAO, ACOLE2.DITADO_COMPOSICAO_DIFICULDADES]
    dictation = acole1_dictation + module_dictation + acole2_dictation

    if use_boxplot:
        boxplot_blocks(axs[1], dictation, 'Ditado por composição')
    else:
        plot_blocks(axs[1], dictation, 'Ditado por composição')

    ACOLE1.DITADO_MANUSCRITO.legend = 'ACOLE inicial'
    ACOLE1.DITADO_MANUSCRITO_DIFICULDADES.legend = 'ACOLE inicial - Dificuldades'
    MODULE1.EXTCI.legend = 'Módulo 1 inicial - B'
    MODULE1.EXTCF.legend = 'Módulo 1 final - B'
    ACOLE2.DITADO_MANUSCRITO.legend = 'ACOLE final'
    ACOLE2.DITADO_MANUSCRITO_DIFICULDADES.legend = 'ACOLE final - Dificuldades'

    acole1_manuscript = [ACOLE1.DITADO_MANUSCRITO, ACOLE1.DITADO_MANUSCRITO_DIFICULDADES]
    module_manuscript = [MODULE1.EXTCI, MODULE1.EXTCF]
    acole2_manuscript = [ACOLE2.DITADO_MANUSCRITO, ACOLE2.DITADO_MANUSCRITO_DIFICULDADES]
    manuscript = acole1_manuscript + module_manuscript + acole2_manuscript

    if use_boxplot:
        boxplot_blocks(axs[2], manuscript, 'Ditado manuscrito')
    else:
        plot_blocks(axs[2], dictation, 'Ditado manuscrito')

    plt.tight_layout()
    if use_boxplot:
        figure_name = 'Fig27_boxplot.png'
    else:
        figure_name = 'Fig27.png'
    plt.savefig(os.path.join(base_dir, 'figures', figure_name), bbox_inches='tight')

if __name__ == "__main__":
    ACOLE1 = ACOLE1.create()
    ACOLE2 = ACOLE2.create()
    MODULE1 = MODULE1.create()
    for student in students:
        if len(student.acoles) > 1:
            if len(student.modules) > 0:
                if student.has_m1:
                    for block, student_block in zip(ACOLE1.blocks, student.acoles[0].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

                    for block, student_block in zip(ACOLE2.blocks, student.acoles[1].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

                    for block, student_block in zip(MODULE1.blocks, student.modules[0].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

    bar_plot(ACOLE1, MODULE1, ACOLE2)
    bar_plot(ACOLE1, MODULE1, ACOLE2, use_boxplot=True)