import matplotlib.pyplot as plt
import numpy as np

from colors import color1, color2, color3

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

def plot_blocks_pairs(ax, blocks, title, color1=color1, color2=color2, label1='Inicial', label2='Final', bar_width=0.4):
    half = len(blocks) // 2
    bar_positions1 = np.arange(half)
    bar_positions2 = np.array(bar_positions1) + bar_width
    bar_values, _, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks)
    tick_labels = [block.legend for block in blocks]
    tick_labels = tick_labels[::2]
    bar_values1 = bar_values[::2]
    bar_values2 = bar_values[1::2]
    ax.set_ylim(0, 100)
    ax.set_title(title, y=1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    ax.bar(bar_positions1, bar_values1, width=bar_width, color=color1, label=label1)
    ax.bar(bar_positions2, bar_values2, width=bar_width, color=color2, label=label2)

    ax.set_xticks(bar_positions2-bar_width/2)
    ax.set_xticklabels(tick_labels, ha='center')


def do_plot(ACOLE1, MODULE1, ACOLE2, use_boxplot, filename):
    fig, axs = plt.subplots(3, 2, sharey=True)
    fig.set_size_inches(5, 10)
    fig.set_dpi(100)

    for i in range(3):
        axs[i, 0].set_ylabel('Porcentagem média de acertos')

    regular_acole_label = 'Palavras\nReg.CV'
    difficult_acole_label = 'Palavras\nDif. Ort.'
    ext_test_label = 'Testes\nextensivos'
    ACOLE1.LEITURA.legend = regular_acole_label
    ACOLE2.LEITURA.legend = regular_acole_label
    ACOLE1.LEITURA_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.LEITURA_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTAI.legend = ext_test_label+' 1'
    MODULE1.EXTAF.legend = ext_test_label+' 1'
    MODULE1.EXTBI.legend = ext_test_label+' 2'
    MODULE1.EXTBF.legend = ext_test_label+' 2'

    acole1_reading = [ACOLE1.LEITURA, ACOLE2.LEITURA]
    acole2_reading = [ACOLE1.LEITURA_DIFICULDADES, ACOLE2.LEITURA_DIFICULDADES]
    module_reading = [MODULE1.EXTAI, MODULE1.EXTAF, MODULE1.EXTBI, MODULE1.EXTBF]
    reading = acole1_reading + acole2_reading
    column1_label = 'ACOLE\ninicial e final'
    column2_label = 'Módulo 1\ntestes extensivos'
    if use_boxplot:
        boxplot_blocks(axs[0, 0], reading, column1_label)
    else:
        plot_blocks_pairs(axs[0, 0], reading, column1_label)

    if use_boxplot:
        boxplot_blocks(axs[0, 1], module_reading, column2_label)
    else:
        plot_blocks_pairs(axs[0, 1], module_reading, column2_label, color1=color3, label1='Intermediário')


    ACOLE1.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE2.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE1.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTDI.legend = ext_test_label
    MODULE1.EXTDF.legend = ext_test_label

    acole1_dictation = [ACOLE1.DITADO_COMPOSICAO, ACOLE2.DITADO_COMPOSICAO]
    acole2_dictation = [ACOLE1.DITADO_COMPOSICAO_DIFICULDADES, ACOLE2.DITADO_COMPOSICAO_DIFICULDADES]
    module_dictation = [MODULE1.EXTDI, MODULE1.EXTDF]

    dictation = acole1_dictation + acole2_dictation

    if use_boxplot:
        boxplot_blocks(axs[1, 0], dictation, ' ')
    else:
        plot_blocks_pairs(axs[1, 0], dictation, ' ')

    if use_boxplot:
        boxplot_blocks(axs[1, 1], module_dictation, ' ')
    else:
        plot_blocks_pairs(axs[1, 1], module_dictation, ' ', color1=color3, label1='Intermediário', bar_width=0.2)

    ACOLE1.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE2.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE1.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTCI.legend = ext_test_label
    MODULE1.EXTCF.legend = ext_test_label

    acole1_manuscript = [ACOLE1.DITADO_MANUSCRITO, ACOLE2.DITADO_MANUSCRITO]
    acole2_manuscript = [ACOLE1.DITADO_MANUSCRITO_DIFICULDADES, ACOLE2.DITADO_MANUSCRITO_DIFICULDADES]
    module_manuscript = [MODULE1.EXTCI, MODULE1.EXTCF]
    manuscript = acole1_manuscript + acole2_manuscript
    if use_boxplot:
        boxplot_blocks(axs[2, 0], manuscript, ' ')
    else:
        plot_blocks_pairs(axs[2, 0], manuscript, ' ')

    if use_boxplot:
        boxplot_blocks(axs[2, 1], module_manuscript, ' ')
    else:
        plot_blocks_pairs(axs[2, 1], module_manuscript, ' ', color1=color3, label1='Intermediário', bar_width=0.2)


    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.35, -0.06),)

    handles, labels = axs[0, 1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.75, -0.06),)

    fig.text(0.5, .9,
        'Leitura', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, .6,
        'Ditado por composição', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, .29,
        'Ditado manuscrito', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')


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
    filename = 'Fig27_m1_testes'
    do_plot(ACOLE_1, MODULE_1, ACOLE_2, use_boxplot=False, filename=filename)
    do_plot(ACOLE_1, MODULE_1, ACOLE_2, use_boxplot=True,  filename=filename)

if __name__ == "__main__":
    plot()