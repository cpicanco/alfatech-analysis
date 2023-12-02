import matplotlib.pyplot as plt
import numpy as np

from databases import MODULE1, ACOLE1, ACOLE2
from databases.students import students
from methods import statistics_from_blocks, output_path

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

def plot_blocks_pairs(ax, blocks, title):
    bar_width = 0.4
    half = len(blocks) // 2
    color1 = 'salmon'
    color2 = 'skyblue'
    colors1 = color1
    colors2 = color2
    labels1 = 'Inicial'
    labels2 = 'Final'
    bar_positions1 = np.arange(half)
    bar_positions2 = np.array(bar_positions1) + bar_width
    bar_values, bar_stds, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks)
    tick_labels = [block.legend for block in blocks]
    tick_labels = tick_labels[::2]
    bar_values1 = bar_values[::2]
    bar_values2 = bar_values[1::2]
    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    bars1 = ax.bar(bar_positions1, bar_values1, width=bar_width, color=colors1, label=labels1)
    bars2 = ax.bar(bar_positions2, bar_values2, width=bar_width, color=colors2, label=labels2)

    ax.set_xticks(bar_positions2-bar_width/2)
    ax.set_xticklabels(tick_labels, ha='center')


def do_plot(ACOLE1, MODULE1, ACOLE2, use_boxplot, filename):
    fig, axs = plt.subplots(3, 1, sharey=True)
    fig.set_size_inches(5, 10)
    fig.set_dpi(100)

    for ax in axs:
        ax.set_ylabel('Porcentagem média de acertos')

    regular_acole_label = 'ACOLE\nRegulares\nCV'
    difficult_acole_label = 'ACOLE\nDificuldades'
    ACOLE1.LEITURA.legend = regular_acole_label
    ACOLE2.LEITURA.legend = regular_acole_label
    ACOLE1.LEITURA_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.LEITURA_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTAI.legend = 'Módulo 1\nt. ext. 1'
    MODULE1.EXTAF.legend = 'Módulo 1\nt. ext. 1'
    MODULE1.EXTBI.legend = 'Módulo 1\nt. ext. 2'
    MODULE1.EXTBF.legend = 'Módulo 1\nt. ext. 2'

    acole1_reading = [ACOLE1.LEITURA, ACOLE2.LEITURA]
    acole2_reading = [ACOLE1.LEITURA_DIFICULDADES, ACOLE2.LEITURA_DIFICULDADES]
    module_reading = [MODULE1.EXTAI, MODULE1.EXTAF, MODULE1.EXTBI, MODULE1.EXTBF]
    reading = acole1_reading + acole2_reading + module_reading

    if use_boxplot:
        boxplot_blocks(axs[0], reading, 'Leitura')
    else:
        plot_blocks_pairs(axs[0], reading, 'Leitura')

    ACOLE1.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE2.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE1.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTDI.legend = 'Módulo 1\nt. ext.'
    MODULE1.EXTDF.legend = 'Módulo 1\nt. ext.'

    acole1_dictation = [ACOLE1.DITADO_COMPOSICAO, ACOLE2.DITADO_COMPOSICAO]
    acole2_dictation = [ACOLE1.DITADO_COMPOSICAO_DIFICULDADES, ACOLE2.DITADO_COMPOSICAO_DIFICULDADES]
    module_dictation = [MODULE1.EXTDI, MODULE1.EXTDF]

    dictation = acole1_dictation + acole2_dictation + module_dictation

    if use_boxplot:
        boxplot_blocks(axs[1], dictation, 'Ditado por composição')
    else:
        plot_blocks_pairs(axs[1], dictation, 'Ditado por composição')

    ACOLE1.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE2.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE1.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTCI.legend = 'Módulo 1\nt. ext.'
    MODULE1.EXTCF.legend = 'Módulo 1\nt. ext.'

    acole1_manuscript = [ACOLE1.DITADO_MANUSCRITO, ACOLE2.DITADO_MANUSCRITO]
    acole2_manuscript = [ACOLE1.DITADO_MANUSCRITO_DIFICULDADES, ACOLE2.DITADO_MANUSCRITO_DIFICULDADES]
    module_manuscript = [MODULE1.EXTCI, MODULE1.EXTCF]
    manuscript = acole1_manuscript + acole2_manuscript + module_manuscript
    if use_boxplot:
        boxplot_blocks(axs[2], manuscript, 'Ditado manuscrito')
    else:
        plot_blocks_pairs(axs[2], dictation, 'Ditado manuscrito')

    handles, labels = axs[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center')

    plt.tight_layout()
    if use_boxplot:
        figure_name = filename+'_boxplot'
    else:
        figure_name = filename
    plt.savefig(output_path(figure_name), bbox_inches='tight')
    plt.close()


def plot():
    ACOLE_1 = ACOLE1.create()
    ACOLE_2 = ACOLE2.create()
    MODULE_1 = MODULE1.create()
    for student in students:
        if len(student.acoles) > 1:
            if len(student.modules) > 0:
                if student.has_m1:
                    for block, student_block in zip(ACOLE_1.blocks, student.acoles[0].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

                    for block, student_block in zip(ACOLE_2.blocks, student.acoles[1].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

                    for block, student_block in zip(MODULE_1.blocks, student.modules[0].blocks):
                        for key, data in student_block.data.items():
                            if len(data) > 0:
                                block.data[key].append(data[0])

    """
    Porcentagem média de acertos na ACOLE inicial
    testes de Módulo 1 e ACOLE final'
    """
    do_plot(ACOLE_1, MODULE_1, ACOLE_2, use_boxplot=False, filename='Fig27b')
    do_plot(ACOLE_1, MODULE_1, ACOLE_2, use_boxplot=True,  filename='Fig27b')

if __name__ == "__main__":
    plot()