import matplotlib.pyplot as plt
import numpy as np

from colors import color1, color2, blue2, blue3, color_median

from databases import MODULE1, ACOLE1, ACOLE2
from databases.students import students
from methods import statistics_from_blocks, opt, histogram
from base import default_axis_config, get_grouped_bar_positions, get_ax_top, upper_summary

# def get_positions(num_groups, num_items_per_group, start, gap, width):
#     def plot_position(i, j, start, gap, width):
#         return start + i * (gap + 2 * width) + j * (width + 0.1)

#     positions = []
#     for i in range(num_groups):
#         for j in range(num_items_per_group):
#             positions.append(plot_position(i, j, start, gap, width))
#     return positions

def boxplot_blocks_pairs(ax, blocks, title,
                         title_y=1.4, limity=True,
                         color1=color1, color2=color2,
                         label1='Inicial', label2='Final',
                         bar_width=0.4,
                         data='percentages',
                         write_start_annotation=True):
    default_axis_config(ax, limit_y=limity)
    half = len(blocks) // 2

    data_values = [[p for p in block.data[data] if p is not None] for block in blocks]
    data_labels = [block.base_legend for block in blocks]
    for d, label in zip(data_values, data_labels):
        histogram(d, label, range=(-100, 100), bins=20)

    positions = get_grouped_bar_positions(half, 2, 0.5, 0.5, bar_width).flatten()

    # slice positions
    positions1 = positions[::2]
    positions2 = positions[1::2]

    tick_labels = [block.legend for block in blocks]
    tick_labels = tick_labels[::2]
    bar_values1 = data_values[::2]
    bar_values2 = data_values[1::2]
    boxprops1 = dict(linewidth=2)
    boxprops2 = dict(linewidth=2)
    medianprops = dict(linewidth=2, color='black')
    ax.set_title(title, y=title_y)

    bp1 = ax.boxplot(bar_values1, positions=positions1,
                     patch_artist=True,
                     widths=bar_width,
                     sym='o',
                     boxprops=boxprops1,
                     medianprops=medianprops)
    bp2 = ax.boxplot(bar_values2, positions=positions2,
                     patch_artist=True,
                     widths=bar_width,
                     sym='o',
                     boxprops=boxprops2,
                     medianprops=medianprops)

    colors = [color1, color2]
    for i, bplot in enumerate([bp1, bp2]):
        color = colors[i % len(colors)]  # Ensure colors repeat if there are more boxes than colors
        for patch in bplot['boxes']:
            patch.set_facecolor(color)

    positions = list(positions1) + list(positions2)
    values = bar_values1 + bar_values2
    lengths = [len(v) for v in values]
    medians = [np.median(v) for v in values]
    values = [np.mean(v) for v in values]
    upper_summary(ax, positions, values, medians, lengths, x=0.0, y=125, line_height=8, show_label=write_start_annotation)

    ax.set_xticks(np.array(positions2)-bar_width/2)
    ax.set_xticklabels(tick_labels, ha='center')

    return bp1, bp2, [label1, label2]


def plot_blocks_pairs(ax, blocks, title,
                      color1=color1, color2=color2,
                      label1='Inicial', label2='Final',
                      bar_width=0.4,
                      title_y=1.4,
                      write_start_annotation=True):
    default_axis_config(ax)
    half = len(blocks) // 2
    positions = get_grouped_bar_positions(half, 2, 0.5, 0.5, bar_width).flatten()

    # slice positions
    positions1 = positions[::2]
    positions2 = positions[1::2]
    bar_values, _, bar_lengths, bar_medians, mins, maxs = statistics_from_blocks(blocks)

    tick_labels = [block.legend for block in blocks]
    tick_labels = tick_labels[::2]
    bar_values1 = bar_values[::2]
    bar_values2 = bar_values[1::2]
    medians1 = bar_medians[::2]
    medians2 = bar_medians[1::2]
    ax.set_title(title, y=title_y)

    bars = ax.bar(positions1, bar_values1, width=bar_width, color=color1, label=label1)
    for bar, m in zip(bars, medians1):
        ax.hlines(m, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color=color_median)

    bars = ax.bar(positions2, bar_values2, width=bar_width, color=color2, label=label2)
    for bar, m in zip(bars, medians2):
        ax.hlines(m, bar.get_x(), bar.get_x() + bar.get_width(), linestyles='solid', color=color_median)

    positions = list(positions1) + list(positions2)
    values = bar_values1 + bar_values2
    lengths = bar_lengths[::2] + bar_lengths[1::2]
    medians = bar_medians[::2] + bar_medians[1::2]
    upper_summary(ax, positions, values, medians, lengths, x=0.3, y=125, line_height=8, show_label=write_start_annotation)

    ax.set_xticks(np.array(positions2)-bar_width/2)
    ax.set_xticklabels(tick_labels, ha='center')

def boxplot_blocks(ax, blocks, title, title_y=1.4):
    default_axis_config(ax)
    label1 = 'Acole Inicial'
    label2 = 'Acole Final'
    label3 = 'Teste Ext. Int.'
    label4 = 'Teste Ext. Fin.'

    data_values = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    data_labels = [block.base_legend for block in blocks]
    for d, label in zip(data_values, data_labels):
        histogram(d, label, range=(-100, 100), bins=20)
    wd = 0.5
    positions = get_grouped_bar_positions(len(blocks), 1, 0.5, 0.5, wd).flatten()

    tick_labels = ['Palavras\nReg. CV', 'Ext.\nInt.', 'Ext.\nFin.', 'Palavras\nReg. CV']
    bar_values = data_values
    boxprops = dict(linewidth=2)
    medianprops = dict(linewidth=2, color='black')
    ax.set_title(title, y=title_y)

    bp1 = ax.boxplot(bar_values[0], positions=[positions[0]],
                    patch_artist=True,
                    widths=wd,
                    sym='o',
                    boxprops=boxprops,
                    medianprops=medianprops)

    bp2 = ax.boxplot(bar_values[-1], positions=[positions[-1]],
                    patch_artist=True,
                    widths=wd,
                    sym='o',
                    boxprops=boxprops,
                    medianprops=medianprops)

    bp3 = ax.boxplot(bar_values[1], positions=[positions[1]],
                    patch_artist=True,
                    widths=wd,
                    sym='o',
                    boxprops=boxprops,
                    medianprops=medianprops)

    bp4 = ax.boxplot(bar_values[2], positions=[positions[2]],
                    patch_artist=True,
                    widths=wd,
                    sym='o',
                    boxprops=boxprops,
                    medianprops=medianprops)

    colors = [color1, color2, blue2, blue3]
    for i, bplot in enumerate([bp1, bp2, bp3, bp4]):
        color = colors[i % len(colors)]  # Ensure colors repeat if there are more boxes than colors
        for patch in bplot['boxes']:
            patch.set_facecolor(color)

    positions = positions
    values = bar_values
    lengths = [len(v) for v in values]
    medians = [np.median(v) for v in values]
    values = [np.mean(v) for v in values]
    upper_summary(ax, positions, values, medians, lengths, x=0.0, y=125, line_height=8, show_label=False)

    ax.set_xticks(np.array(positions))
    ax.set_xticklabels(tick_labels, ha='center')

    return bp1, bp2, bp3, bp4, [label1, label2, label3, label4]

def plot_blocks(ax, blocks, title, title_y=1.4):
    label1 = 'Acole Inicial'
    label2 = 'Acole Final'
    label3 = 'Teste Ext. Int.'
    label4 = 'Teste Ext. Fin.'
    default_axis_config(ax)
    bar_positions = np.arange(len(blocks))
    colors = [color1, blue2, blue3, color2]
    labels = [label1, label3, label4, label2]

    bars_list = []
    bar_values, _, bar_lengths, bar_medians, _, _ = statistics_from_blocks(blocks)
    ax.set_title(title, y=title_y)
    for values, color, label, pos in zip(bar_values, colors, labels, bar_positions):
        bars_list.append(ax.bar(pos, values, color=color, label=label))
    for m, bars in zip(bar_medians, bars_list):
        ax.hlines(m, bars[0].get_x(), bars[0].get_x() + bars[0].get_width(), linestyles='solid', color=color_median)

    ax.set_xticks(bar_positions)
    tick_labels = ['Palavras\nReg. CV', 'Ext.\nInt.', 'Ext.\nFin.', 'Palavras\nReg. CV']
    ax.set_xticklabels(tick_labels)

    upper_summary(ax, bar_positions, bar_values, bar_medians, bar_lengths, x=-0.5, y=125, line_height=8, show_label=False)

def do_plot(ACOLE_1, MODULE_1, ACOLE_2, use_boxplot, filename):
    if use_boxplot:
        figure_name = filename+'_boxplot'
    else:
        figure_name = filename
    opt.set_filename(figure_name)

    ACOLE1 = ACOLE_1.create()
    ACOLE2 = ACOLE_2.create()
    MODULE1 = MODULE_1.create()
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


    fig, axs = plt.subplots(3, 2, sharey=True)
    fig.set_size_inches(5, 10)
    fig.set_dpi(100)

    axs[1, 0].set_ylabel('Porcentagem média de acertos')
    column1_label = 'ACOLE'
    column2_label = 'ACOLE/Módulo 1'
    regular_acole_label = 'Palavras\nReg.CV'
    difficult_acole_label = 'Palavras\nDif. Ort.'
    ext_test_label = 'Testes\nextensivos'
    ACOLE1.LEITURA.legend = regular_acole_label
    ACOLE2.LEITURA.legend = regular_acole_label
    ACOLE1.LEITURA_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.LEITURA_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTAI.legend = ext_test_label
    MODULE1.EXTBI.legend = ext_test_label
    MODULE1.EXTAF.legend = ext_test_label
    MODULE1.EXTBF.legend = ext_test_label

    ACOLE1.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE2.DITADO_COMPOSICAO.legend = regular_acole_label
    ACOLE1.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.DITADO_COMPOSICAO_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTDI.legend = ext_test_label
    MODULE1.EXTDF.legend = ext_test_label

    ACOLE1.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE2.DITADO_MANUSCRITO.legend = regular_acole_label
    ACOLE1.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    ACOLE2.DITADO_MANUSCRITO_DIFICULDADES.legend = difficult_acole_label
    MODULE1.EXTCI.legend = ext_test_label
    MODULE1.EXTCF.legend = ext_test_label

    acole_reading = [
        ACOLE1.LEITURA,
        ACOLE2.LEITURA,
        ACOLE1.LEITURA_DIFICULDADES,
        ACOLE2.LEITURA_DIFICULDADES]

    acole_dictation = [
        ACOLE1.DITADO_COMPOSICAO,
        ACOLE2.DITADO_COMPOSICAO,
        ACOLE1.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE2.DITADO_COMPOSICAO_DIFICULDADES]

    acole_manuscript = [
        ACOLE1.DITADO_MANUSCRITO,
        ACOLE2.DITADO_MANUSCRITO,
        ACOLE1.DITADO_MANUSCRITO_DIFICULDADES,
        ACOLE2.DITADO_MANUSCRITO_DIFICULDADES]

    module_reading = [
        ACOLE1.LEITURA,
        MODULE1.EXTAI.merge(MODULE1.EXTBI),
        MODULE1.EXTAF.merge(MODULE1.EXTBF),
        ACOLE2.LEITURA,]

    module_dictation = [
        ACOLE1.DITADO_COMPOSICAO,
        MODULE1.EXTDI,
        MODULE1.EXTDF,
        ACOLE2.DITADO_COMPOSICAO]

    module_manuscript = [
        ACOLE1.DITADO_MANUSCRITO,
        MODULE1.EXTCI,
        MODULE1.EXTCF,
        ACOLE2.DITADO_MANUSCRITO]

    if use_boxplot:
        bp1, bp2, labels1 = boxplot_blocks_pairs(axs[0, 0], acole_reading, column1_label)
        bp1, bp2, bp3, bp4, labels2 = boxplot_blocks(axs[0, 1], module_reading, column2_label)
        boxplot_blocks_pairs(axs[1, 0], acole_dictation, ' ')
        boxplot_blocks(axs[1, 1], module_dictation, ' ')
        boxplot_blocks_pairs(axs[2, 0], acole_manuscript, ' ')
        boxplot_blocks(axs[2, 1], module_manuscript, ' ')
    else:
        plot_blocks_pairs(axs[0, 0], acole_reading, column1_label)
        plot_blocks(axs[0, 1], module_reading, column2_label)
        plot_blocks_pairs(axs[1, 0], acole_dictation, ' ')
        plot_blocks(axs[1, 1], module_dictation, ' ')
        plot_blocks_pairs(axs[2, 0], acole_manuscript, ' ')
        plot_blocks(axs[2, 1], module_manuscript, ' ')

    x1, x2 = 0.35, 0.75
    y1 = -0.1
    if use_boxplot:
        fig.legend([bp1["boxes"][0], bp2["boxes"][0]], labels1, loc='lower center', bbox_to_anchor=(x1, y1))
        fig.legend([bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0], bp4["boxes"][0]], labels2, loc='lower center', bbox_to_anchor=(x2, y1))
    else:
        ax1 = axs[0, 0]
        ax2 = axs[0, 1]
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(x1, y1))

        handles, labels = ax2.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(x2, y1))

    plt.tight_layout()

    ax1_top, unit1 = get_ax_top(axs[0, 0])
    ax2_top, unit2  = get_ax_top(axs[1, 0])
    ax3_top, unit3 = get_ax_top(axs[2, 0])
    center_x = 0.5
    fig.text(center_x, ax1_top-unit1*5,
        'Leitura', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(center_x, ax2_top-unit2*3.5,
        'Ditado por composição', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(center_x, ax3_top-unit3*3.5,
        'Ditado manuscrito', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()


def plot():
    """
    Porcentagem média de acertos na ACOLE inicial
    testes de Módulo 1 e ACOLE final'
    """
    filename = 'Fig27_m1_testes'
    do_plot(ACOLE1, MODULE1, ACOLE2, use_boxplot=False, filename=filename)
    do_plot(ACOLE1, MODULE1, ACOLE2, use_boxplot=True,  filename=filename)

if __name__ == "__main__":
    plot()