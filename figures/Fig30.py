# python modules
import os
import sys
import pandas as pd

base_dir = os.path.abspath(__file__).rsplit("figures", 1)[0]
sys.path.append(os.path.join(base_dir))

# graphication
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

from databases.students import students
from databases.ranges import RangeContainer
from databases import ACOLE1, ACOLE2

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

def bar_plot(ACOLE1, MODULE3, ACOLE2, use_boxplot=False):
    if use_boxplot:
        title = 'Distribuição da porcentagem de acertos na ACOLE inicial,\nno Módulo 3 (completo) e ACOLE final'
    else:
        title = 'Porcentagem média de acertos na ACOLE inicial,\n no Módulo 3 (completo) e ACOLE final'

    initial_acole_label = 'ACOLE inicial'
    initial_acole_difficulties_label = 'ACOLE inicial - Dificuldades'
    final_acole_label = 'ACOLE final'
    final_acole_difficulties_label = 'ACOLE final - Dificuldades'

    ACOLE1.LEITURA.legend = initial_acole_label
    ACOLE1.LEITURA_DIFICULDADES.legend = initial_acole_difficulties_label
    ACOLE1.DITADO_COMPOSICAO.legend = initial_acole_label
    ACOLE1.DITADO_COMPOSICAO_DIFICULDADES.legend = initial_acole_difficulties_label
    ACOLE1.DITADO_MANUSCRITO.legend = initial_acole_label
    ACOLE1.DITADO_MANUSCRITO_DIFICULDADES.legend = initial_acole_difficulties_label

    ACOLE2.LEITURA.legend = final_acole_label
    ACOLE2.LEITURA_DIFICULDADES.legend = final_acole_difficulties_label
    ACOLE2.DITADO_COMPOSICAO.legend = final_acole_label
    ACOLE2.DITADO_COMPOSICAO_DIFICULDADES.legend = final_acole_difficulties_label
    ACOLE2.DITADO_MANUSCRITO.legend = final_acole_label
    ACOLE2.DITADO_MANUSCRITO_DIFICULDADES.legend = final_acole_difficulties_label

    # Get the data from
    reading = [
        ACOLE1.LEITURA,
        ACOLE1.LEITURA_DIFICULDADES,
        ACOLE2.LEITURA,
        ACOLE2.LEITURA_DIFICULDADES]

    composition = [
        ACOLE1.DITADO_COMPOSICAO,
        ACOLE1.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE2.DITADO_COMPOSICAO,
        ACOLE2.DITADO_COMPOSICAO_DIFICULDADES]

    manuscript = [
        ACOLE1.DITADO_MANUSCRITO,
        ACOLE1.DITADO_MANUSCRITO_DIFICULDADES,
        ACOLE2.DITADO_MANUSCRITO,
        ACOLE2.DITADO_MANUSCRITO_DIFICULDADES]

    # Get the data for the big axis
    module3 = [block for block in MODULE3.blocks if block.min_trials == 0]

    fig = plt.figure(figsize=(8, 8))
    fig.set_dpi(300)
    fig.suptitle(title, fontsize=14)
    gs = GridSpec(2, 3, height_ratios=[1.5, 1.5], width_ratios=[1, 1, 1])

    # Create three axes on the top row
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)
    ax3 = fig.add_subplot(gs[0, 2], sharey=ax1)

    # Create a larger axis at the bottom that spans all three columns
    ax_big = fig.add_subplot(gs[1, :], sharey=ax1)

    # Add content to the axes (you can customize this based on your data)
    if use_boxplot:
        boxplot_blocks(ax1, reading, 'Leitura')
        boxplot_blocks(ax2, composition, 'Ditado por composição')
        boxplot_blocks(ax3, manuscript, 'Ditado manuscrito')
        boxplot_blocks(ax_big, module3, 'Módulo 3')
    else:
        plot_blocks(ax1, reading, 'Leitura')
        plot_blocks(ax2, composition, 'Ditado por composição')
        plot_blocks(ax3, manuscript, 'Ditado manuscrito')
        plot_blocks(ax_big, module3, 'Módulo 3')

    # Adjust layout and add legends if needed
    fig.tight_layout()
    # ax1.legend()
    # ax2.legend()
    # ax3.legend()
    # ax_big.legend()

    # Show the plot
    if use_boxplot:
        figure_name = 'Fig30_boxplot.png'
    else:
        figure_name = 'Fig30.png'
    plt.savefig(os.path.join(base_dir, 'figures', figure_name), bbox_inches='tight')


if __name__ == "__main__":
    pass
    # ACOLE1 = ACOLE1.create()
    # ACOLE2 = ACOLE2.create()
    # filtered_students = students.create()

    # for student in students:
    #     if len(student.acoles) > 1:
    #         if len(student.modules) > 0:
    #             if student.has_m1:
    #                 filtered_students.append(student)
    #                 for block, student_block in zip(ACOLE1.blocks, student.acoles[0].blocks):
    #                     for key, data in student_block.data.items():
    #                         if len(data) > 0:
    #                             block.data[key].append(data[0])

    #                 for block, student_block in zip(ACOLE2.blocks, student.acoles[1].blocks):
    #                     for key, data in student_block.data.items():
    #                         if len(data) > 0:
    #                             block.data[key].append(data[0])

    # df = filtered_students.days_per_week()
    # ranges = RangeContainer(np.linspace(df.min(), df.max(), 6))
    # for r in ranges:
    #     ACOLE1.by_frequency(r).summary()
