import matplotlib.pyplot as plt
import numpy as np

from databases.students import students
from databases import ACOLE1, ACOLE2
from methods import output_path
from base import default_axis_config

top_labels = ['Leitura', 'Ditado por composição', 'Ditado manuscrito']

def boxplot_blocks(ax, blocks, label):
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['deltas'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=1, color='black')
    medianprops = dict(linewidth=2, color='orange')

    bp = ax.boxplot(data[::2], positions=bar_positions[::2], widths=0.6, sym='o', boxprops=boxprops, medianprops=medianprops)
    bp = ax.boxplot(data[1::2], positions=bar_positions[1::2], widths=0.6, sym='o', boxprops=boxprops, medianprops=medianprops)

    ax.set_title(label)
    default_axis_config(ax)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend for block in blocks], rotation=45, ha='right')

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
    bars = ax.bar(bar_positions[::2], means[::2], width=bar_width, color='salmon', label='Sem dificuldades ortográficas')
    bars = ax.bar(bar_positions[1::2]-bar_width, means[1::2], width=bar_width, color='skyblue', label='Com dificuldades ortográficas')

    ax.set_xticks(np.array(bar_positions[1::2]) - bar_width - bar_width / 2)
    ax.set_xticklabels(legends, ha='center')

def bar_plot(ACOLE1, ACOLE2, use_boxplot, filename):
    # df = ACOLE2.days_per_week()
    # min_ = df['mean_days_per_week'].min() # 0.07317073170731707
    # max_ = df['mean_days_per_week'].max() # 2.4615384615384617
    values = [0.72, 1.30, 1.50, 1.70, 2.5]

    reading = []
    composition = []
    manuscript = []

    for r in ACOLE2.custom_range(values):
        blocks1 = ACOLE1.by_frequency(r)
        blocks2 = ACOLE2.by_frequency(r)
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

    for (ax, label, data) in zip(axs, top_labels, groups):
        if use_boxplot:
            boxplot_blocks(ax, data, label)
        else:
            plot_blocks(ax, data, label)

    fig.text(0.5, -0.05, 'Faixa de frequência semanal\n(Dias/Semana)', ha='center', va='center', fontsize=12)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2)

    fig.tight_layout()
    if use_boxplot:
        figure_name = filename+'_boxplot'
    else:
        figure_name = filename
    plt.savefig(output_path(figure_name), bbox_inches='tight')
    plt.close()

def plot():
    ACOLE_1 = ACOLE1.create()
    ACOLE_2 = ACOLE2.create()
    filtered_students = students.create()

    for student in students:
        if student.has_two_acoles():
            acole1, acole2 = student.get_first_and_second_acoles()
            if student.has_m1:
                filtered_students.append(student)
                for block, student_block in zip(ACOLE_1.blocks, student.acoles[acole1].blocks):
                    for key, data in student_block.data.items():
                        if len(data) > 0:
                            block.data[key].append(data[0])

                for block, student_block in zip(ACOLE_2.blocks, student.acoles[acole2].blocks):
                    for key, data in student_block.data.items():
                        if len(data) > 0:
                            block.data[key].append(data[0])

        """
    Diferença entre a porcentagem de acertos na ACOLE final e inicial,
    de estudantes com Módulo 1 completo,
    com estudantes que avançaram até as palavras com dificuldades ortográficas na primeira ACOLE,
    or faixa de frequência no projeto
    """
    bar_plot(ACOLE_1, ACOLE_2, use_boxplot=False, filename='Fig30')
    bar_plot(ACOLE_1, ACOLE_2, use_boxplot=True, filename='Fig30')

if __name__ == "__main__":
   plot()