import matplotlib.pyplot as plt
import numpy as np

from databases.students import students
from databases import ACOLE1, ACOLE2
from methods import opt
from base import default_axis_config
from colors import color1, color2
from Fig27_m1_tests import boxplot_blocks_pairs

top_labels = ['Leitura', 'Ditado por composição', 'Ditado manuscrito']
inner_labels = ['Palavras regulares CV', 'Palavras com\ndificuldades ortográficas']

# def boxplot_blocks(ax, blocks, label):
#     bar_positions = np.arange(len(blocks))

#     data = [[p for p in block.data['deltas'] if p is not None] for block in blocks]
#     boxprops = dict(linewidth=1, color='black')
#     medianprops = dict(linewidth=2, color='orange')

#     bp1 = ax.boxplot(data[::2], positions=bar_positions[::2], widths=0.6, sym='o', boxprops=boxprops, medianprops=medianprops)
#     bp2 = ax.boxplot(data[1::2], positions=bar_positions[1::2], widths=0.6, sym='o', boxprops=boxprops, medianprops=medianprops)

#     ax.set_title(label)
#     default_axis_config(ax)

#     ax.set_xticks(bar_positions)
#     ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')

#     labels = [block.legend for block in blocks]
#     return bp1, bp2, labels

def plot_blocks(ax, blocks, label, y_padding=1.0):
    bar_width = 0.4
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['deltas'] if p is not None] for block in blocks]

    # calculate mean
    means = [np.mean(d) for d in data]

    # ax.set_ylim(0, 100)
    ax.set_title(label, y=y_padding)
    default_axis_config(ax, False)

    legends = [block.legend for block in blocks][0::2]
    ax.bar(bar_positions[::2], means[::2], width=bar_width, color=color1, label=inner_labels[0])
    ax.bar(bar_positions[1::2]-bar_width, means[1::2], width=bar_width, color=color2, label=inner_labels[1])

    ax.set_xticks(np.array(bar_positions[1::2]) - bar_width - bar_width / 2)
    ax.set_xticklabels(legends, ha='center')

filters = {
    'Fig30_m1_completo': lambda students : [student for student in students if student.has_two_acoles() and student.has_m1],
    'Fig30_m1_completo_acoles_completas': lambda students : [student for student in students if student.has_two_complete_acoles() and student.has_m1],
    'Fig30_m1_completo_primeira_acole_incompleta': lambda students : [student for student in students if student.has_two_acoles_first_incomplete() and student.has_m1],

    'Fig31_m2_completo': lambda students : [student for student in students if student.has_two_acoles() and student.has_m2],
    'Fig31_m2_completo_acoles_completas': lambda students : [student for student in students if student.has_two_complete_acoles() and student.has_m2],
    'Fig31_m2_completo_primeira_acole_incompleta': lambda students : [student for student in students if student.has_two_acoles_first_incomplete() and student.has_m2],

    'Fig32_m3_completo': lambda students : [student for student in students if student.has_two_acoles() and student.has_m3],
    'Fig32_m3_completo_acoles_completas': lambda students : [student for student in students if student.has_two_complete_acoles() and student.has_m3],
    'Fig32_m3_completo_primeira_acole_incompleta': lambda students : [student for student in students if student.has_two_acoles_first_incomplete() and student.has_m3],

    'Fig34_has_first_acole_incomplete': lambda students : [student for student in students if student.has_two_acoles_first_incomplete()],
    'Fig33_has_two_acoles': lambda students : [student for student in students if student.has_two_acoles()],
    'Fig35_has_two_complete_acoles': lambda students : [student for student in students if student.has_two_complete_acoles()],
}

def bar_plot(students, use_boxplot, filename):
    if use_boxplot:
        figure_name = filename+'_boxplot'
    else:
        figure_name = filename
    opt.set_filename(figure_name)
    reading = []
    composition = []
    manuscript = []

    ACOLE_1 = ACOLE1.create()
    ACOLE_2 = ACOLE2.create()

    for student in filters[filename](students):
        ac1, ac2 = student.get_first_and_second_acoles()
        for block, student_block in zip(ACOLE_1.blocks, student.acoles[ac1].blocks):
            for key, data in student_block.data.items():
                if len(data) > 0:
                    for d in data:
                        block.data[key].append(d)

        for block, student_block in zip(ACOLE_2.blocks, student.acoles[ac2].blocks):
            for key, data in student_block.data.items():
                if len(data) > 0:
                    for d in data:
                        block.data[key].append(d)

    # df = ACOLE_2.days_per_week()
    # min_ = df['mean_days_per_week'].min() # 0.07317073170731707
    # max_ = df['mean_days_per_week'].max() # 2.4615384615384617
    values = [0.72, 1.30, 1.50, 1.70, 2.5]

    for r in ACOLE2.custom_range(values):
        blocks1 = ACOLE_1.by_frequency(r)
        blocks2 = ACOLE_2.by_frequency(r)
        reading.append(blocks2.LEITURA.delta(blocks1.LEITURA))
        reading.append(blocks2.LEITURA_DIFICULDADES.delta(blocks1.LEITURA_DIFICULDADES))
        composition.append(blocks2.DITADO_COMPOSICAO.delta(blocks1.DITADO_COMPOSICAO))
        composition.append(blocks2.DITADO_COMPOSICAO_DIFICULDADES.delta(blocks1.DITADO_COMPOSICAO_DIFICULDADES))
        manuscript.append(blocks2.DITADO_MANUSCRITO.delta(blocks1.DITADO_MANUSCRITO))
        manuscript.append(blocks2.DITADO_MANUSCRITO_DIFICULDADES.delta(blocks1.DITADO_MANUSCRITO_DIFICULDADES))

    fig, axs = plt.subplots(3, 1, sharey=True)
    fig.set_size_inches(5, 10)
    fig.set_dpi(100)
    # fig.suptitle(title, y=1.035, fontsize=14)

    groups = [reading, composition, manuscript]
    for group in groups:
        for block in group:
            block.legend = str([block.frequency_range.low, block.frequency_range.high])

    axs[1].set_ylabel('Diferença da porcentagem média de acertos')
    bpg1 = []
    bpg2 = []
    for (ax, title, data) in zip(axs, top_labels, groups):
        if use_boxplot:
            bp1, bp2, _ = boxplot_blocks_pairs(ax, data, title, title_y=1.0, limity=False, data='deltas')
            bpg1.append(bp1)
            bpg2.append(bp2)
        else:
            plot_blocks(ax, data, title)

    fig.tight_layout()

    fig.text(0.5, -0.02, 'Faixa de frequência semanal\n(Dias/Semana)', ha='center', va='center', fontsize=12)

    x1 = 0.5
    y1 = 1.05
    if use_boxplot:
        fig.legend([bpg1[0]["boxes"][0], bpg2[0]["boxes"][0]], inner_labels, loc='upper center', bbox_to_anchor=(x1, y1), ncol=2)
    else:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(x1, y1), ncol=2)

    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()

def plot():
    """
    Diferença entre a porcentagem de acertos na ACOLE final e inicial,
    """
    for filename in filters.keys():
        bar_plot(students, use_boxplot=False, filename=filename)
        bar_plot(students, use_boxplot=True, filename=filename)

    # schools = sorted([k for k in students.schools(True).keys()])
    # for school in schools:
    #     for filename in filters.keys():
    #         students_by_school = students.by_school(school)
    #         bar_plot(students_by_school, use_boxplot=False, filename=filename+'_'+school)
    #         bar_plot(students_by_school, use_boxplot=True, filename=filename+'_'+school)
if __name__ == "__main__":
   plot()