import matplotlib.pyplot as plt
import numpy as np

from databases.students import students
from methods import statistics_from_blocks, opt
from colors import color1, color2, color_median
from base import default_axis_config

top_labels = ['Palavras regulares - CV', 'Palavras com\ndificuldades ortográficas']

def plot_blocks(ax, blocks, title, show_text=True):
    bar_positions = np.arange(len(blocks))*0.8 + 0.8
    bar_width = 0.4
    # data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    # boxprops = dict(linewidth=1, color='black')
    # medianprops = dict(linewidth=1, color='black')

    values, _, _, _, _, _ = statistics_from_blocks(blocks)

    default_axis_config(ax)

    positions1 = bar_positions[0:3]
    positions2 = bar_positions[3:6]+bar_width
    values1 = values[0:3]
    values2 = values[3:6]

    bars = ax.bar(positions1, values1, width=bar_width, color=color1)
    bars = ax.bar(positions2, values2, width=bar_width, color=color2)

    # set y axis title
    ax.set_title(title, y=1.4)
    ax.set_xlabel('--Atividades--')

    x_labels = [block.legend.replace('Ditado ', 'Ditado\n').replace('por ', 'por\n').replace('*', '') for block in blocks]
    bar_positions = np.concatenate((positions1, positions2), axis=0)
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(x_labels, fontsize=8)

    # concatenate the two numpy arrays

    bar_values = np.concatenate((values1, values2), axis=0)
    y_pos = 140
    for i, p in enumerate(bar_positions):
        x_pos = p
        if i == 1:
            ax.text(x_pos, y_pos, top_labels[0], va='top', ha='center', color='black', fontsize=10)
        if i == 4:
            ax.text(x_pos, y_pos, top_labels[1], va='top', ha='center', color='black', fontsize=10)

    # concatenate the two numpy arrays
    bar_positions = np.concatenate((positions1, positions2), axis=0)
    bar_values = np.concatenate((values1, values2), axis=0)

    y_text_start = 110
    y_pos = y_text_start
    if show_text:
        ax.text(0, y_pos, f'M =', ha='right', color='black', fontsize=10)
    for p, v in zip(bar_positions, bar_values):
        x_pos = p
        y_pos = y_text_start
        ax.text(x_pos, y_pos, f'{v:.1f}', ha='center', color='black', fontsize=8)

def bar_plot(ACOLES, filename):
    opt.set_filename(filename)
    fig, axs = plt.subplots(1, len(ACOLES), sharey=True)
    fig.set_size_inches(5*len(ACOLES), 5)
    fig.set_dpi(100)
    # fig.suptitle(title)

    if len(ACOLES) == 1:
        axs.set_ylabel('Porcentagem de acertos')
        axs = [axs]
    else:
        axs[0].set_ylabel('Porcentagem de acertos')

    for i, (ACOLE, axs) in enumerate(zip(ACOLES, axs)):
        blocks = [
            ACOLE.LEITURA,
            ACOLE.DITADO_COMPOSICAO,
            ACOLE.DITADO_MANUSCRITO,
            ACOLE.LEITURA_DIFICULDADES,
            ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
            ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

        show_text = i == 0
        plot_blocks(axs, blocks, f'Acole {i+1}', show_text)

    plt.tight_layout()
    plt.savefig(opt.output_path(), bbox_inches='tight')
    # plt.show()
    plt.close()

def plot():
    opt.extension = '.pdf'
    opt.cd('students')
    for student in students:
        if student.forwarding is None:
            continue

        if student.has_m1:
            if (len(student.acoles) > 0) and (len(student.acoles) < 4):
                bar_plot(student.acoles, f'Fig17_{len(student.acoles)}_m1_student_{student.id}_encaminhado_para_{student.forwarding.lower()}_acoles')
        if student.has_m2:
            if (len(student.acoles) > 0) and (len(student.acoles) < 4):
                bar_plot(student.acoles, f'Fig17_{len(student.acoles)}_m2_student_{student.id}_encaminhado_para_{student.forwarding.lower()}_acoles')
        if student.has_m3:
            if (len(student.acoles) > 0) and (len(student.acoles) < 4):
                bar_plot(student.acoles, f'Fig17_{len(student.acoles)}_m3_student_{student.id}_encaminhado_para_{student.forwarding.lower()}_acoles')
    opt.back()

if __name__ == "__main__":
    plot()