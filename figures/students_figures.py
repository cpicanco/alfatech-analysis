import matplotlib.pyplot as plt
import numpy as np

from databases.students import students
from methods import statistics_from_blocks, opt
from colors import color1, color2
from base import default_axis_config

top_labels = ['Palavras regulares - CV', 'Palavras com\ndificuldades ortográficas']

def plot_blocks(ax, blocks):
    default_axis_config(ax)
    bar_positions = np.arange(len(blocks))*0.8 + 0.2
    bar_width = 0.4
    data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=1, color='black')
    medianprops = dict(linewidth=1, color='black')

    values, _, lens, _, mins, maxs = statistics_from_blocks(blocks)

    positions1 = bar_positions[::2]
    positions2 = bar_positions[1::2]-bar_width
    values1 = values[::2]
    values2 = values[1::2]

    bars = ax.bar(positions1, values1, width=bar_width, label=top_labels[0], color=color1)
    bars = ax.bar(positions2, values2, width=bar_width, label=top_labels[1], color=color2)

    # set y axis title
    ax.set_xlabel('--Atividades--')

    x_labels = [block.legend.replace('Ditado ', 'Ditado\n') for block in blocks]
    ax.set_xticks(positions2 - bar_width/2)
    ax.set_xticklabels(x_labels[::2])
    ax.set_yticks(np.arange(0, 101, 20))
    ax.set_yticklabels(np.arange(0, 101, 20))

    # concatenate the two numpy arrays
    bar_positions = np.concatenate((positions1, positions2), axis=0)
    bar_values = np.concatenate((values1, values2), axis=0)
    lens = np.concatenate((lens[::2], lens[1::2]), axis=0)


    y_text_line = 5
    y_text_start = 110
    y_pos = y_text_start
    ax.text(0, y_pos, f'N =', ha='right', color='black', fontsize=10)
    y_pos = y_pos - y_text_line
    ax.text(0, y_pos, f'M =', ha='right', color='black', fontsize=10)
    y_pos = y_text_start
    for p, v, _len, in zip(bar_positions, bar_values, lens):
        x_pos = p
        y_pos = y_text_start
        ax.text(x_pos, y_pos, f'{_len}', ha='center', color='black', fontsize=8)
        y_pos = y_pos - y_text_line
        ax.text(x_pos, y_pos, f'{v:.1f}', ha='center', color='black', fontsize=8)

def bar_plot(ACOLES, filename):
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
        # Group 1 - Regular Blocks
        blocks = [
            ACOLE.LEITURA,
            ACOLE.LEITURA_DIFICULDADES,
            ACOLE.DITADO_COMPOSICAO,
            ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
            ACOLE.DITADO_MANUSCRITO,
            ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

        plot_blocks(axs, blocks, f'Acole {i+1}')
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(1.2, 0.65), ncol=1)

    plt.tight_layout()
    plt.savefig(opt.output_path(filename), bbox_inches='tight')
    # plt.show()
    plt.close()

def plot():
    opt.extension = '.pdf'
    opt.cd('students')
    for student in students:
        if student.id == 6083:
            if (len(student.acoles) > 0) and (len(student.acoles) < 4):
                bar_plot(student.acoles, 'Fig17_student_'+str(student.id))

    opt.back()

if __name__ == "__main__":
    plot()