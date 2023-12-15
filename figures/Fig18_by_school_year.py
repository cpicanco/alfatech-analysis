import matplotlib.pyplot as plt

from databases import ACOLE1
from methods import statistics_from_block, opt
from base import upper_summary, default_axis_config
from Fig17 import top_labels
from colors import color_median

def plot_blocks(ax, grouped_data, title, adjustment=0.8, write_start_annotation=False):
    num_items_in_block = len(grouped_data[0])
    num_blocks = len(grouped_data)
    ax.set_title(title, va='top', y=1.3)
    default_axis_config(ax)

    bar_positions = []
    bar_width = 0.4  # Adjust the width based on your preference
    bar_positions = []
    positions = []
    values = []
    lengths = []
    medians = []

    labels = []
    colors = []
    for i, block_group in enumerate(grouped_data):
        for j, block in enumerate(block_group):
            bar_position = (i*adjustment) + (i * num_blocks + j) * bar_width
            bar_values, _, bar_length, bar_median, _, _ = statistics_from_block(block)
            # save qq plot for visual inspection
            # qq_plot(block, filename+'_'+str(block.school))
            if j == 0:
                bar_positions.append(bar_position)

            if i == 0:
                labels.append(str(block.school_year))

            # Annotate mean on top of each bar
            colors.append(j)
            positions.append(bar_position)
            values.append(bar_values)
            lengths.append(bar_length)
            medians.append(bar_median)

    sorted_values = []
    sorted_lengths = []
    sorted_medians = []
    for i in range(num_blocks):
        start_index = i * num_items_in_block
        end_index = (i + 1) * num_items_in_block

        ps = positions[start_index:end_index]
        v = values[start_index:end_index]
        l = lengths[start_index:end_index]
        m = medians[start_index:end_index]
        c = colors[start_index:end_index]

        sorted_v, sorted_l, sorted_m, sorted_cl, sorted_lb = zip(*sorted(list(zip(v, l, m, c, labels)), key=lambda x: x[0]))
        sorted_values.extend(sorted_v)
        sorted_lengths.extend(sorted_l)
        sorted_medians.extend(sorted_m)
        # now plot and do not forget to add labels
        for j, (p, v, l, m, cl, lb) in enumerate(zip(ps, sorted_v, sorted_l, sorted_m, sorted_cl, sorted_lb)):
            if i == 0:
                bars = ax.bar(p, v, width=bar_width-0.05, label=lb, color=f'C{cl}')
            else:
                bars = ax.bar(p, v, width=bar_width-0.05, color=f'C{cl}')
            ax.hlines(m, bars[0].get_x(), bars[0].get_x() + bars[0].get_width(), linestyles='solid', color=color_median)

    upper_summary(ax, positions, sorted_values, sorted_medians, sorted_lengths, x=-0.5, show_label=write_start_annotation)

    # Set x-axis ticks and labels
    bar_positions = [ i+(bar_width*num_items_in_block/2) - (bar_width/2) for i in bar_positions]
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([group[0].legend.replace('Ditado ', 'Ditado\n').replace('*', '') for group in grouped_data])


def bar_plot(ACOLE, filename):
    opt.set_filename(filename)
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(10, 5)
    fig.set_dpi(100)

    # 7: 3 data points
    # 8: 111 data points
    # 9: 496 data points
    # 10: 850 data points
    # 11: 685 data points
    # 12: 321 data points
    # 13: 141 data points
    # 14: 24 data points
    # 15: 6 data points
    # 19: 3 data points
    school_years = [3, 4, 5]

    all_data = [ACOLE.by_school_year(school_year) for school_year in school_years]

    leitura = []
    ditado_composicao = []
    ditado_manuscrito = []
    leitura_dificuldades = []
    ditado_composicao_dificuldades = []
    ditado_manuscrito_dificuldades = []

    for data in all_data:
        for block in data.blocks:
            if ACOLE.LEITURA.id == block.id:
                leitura.append(block)
            elif ACOLE.DITADO_COMPOSICAO.id == block.id:
                ditado_composicao.append(block)
            elif ACOLE.DITADO_MANUSCRITO.id == block.id:
                ditado_manuscrito.append(block)
            elif ACOLE.LEITURA_DIFICULDADES.id == block.id:
                leitura_dificuldades.append(block)
            elif ACOLE.DITADO_COMPOSICAO_DIFICULDADES.id == block.id:
                ditado_composicao_dificuldades.append(block)
            elif ACOLE.DITADO_MANUSCRITO_DIFICULDADES.id == block.id:
                ditado_manuscrito_dificuldades.append(block)

    # Group 1 - Regular Blocks
    normal_blocks = [
        leitura,
        ditado_composicao,
        ditado_manuscrito]

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        leitura_dificuldades,
        ditado_composicao_dificuldades,
        ditado_manuscrito_dificuldades]

    axs[0].set_ylabel('Porcentagem média de acertos')
    plot_blocks(axs[0], normal_blocks, top_labels[0], True)
    plot_blocks(axs[1], difficult_blocks, top_labels[1].replace('\n', ' '))

    handles, labels = axs[0].get_legend_handles_labels()
    sorted_handles_labels = sorted(zip(handles, labels), key=lambda x: x[1])
    handles, labels = zip(*sorted_handles_labels)
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.04), ncol=len(school_years))
    fig.text(0.5, -0.05, 'Ano escolar', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()


def plot():
    """
    Porcentagem média de acertos da primeira ACOLE
    com palavras regulares e com dificuldades ortográficas, por ano escolar
    """
    bar_plot(ACOLE1, 'Fig18_ano_escolar')
    # ACOLE1.summary()

if __name__ == "__main__":
    plot()