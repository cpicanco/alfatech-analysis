import matplotlib.pyplot as plt

from databases import ACOLE1
from methods import output_path

from colors import color_median
from Fig17 import top_labels
from Fig18_by_school_year import plot_blocks

def bar_plot(ACOLE, filename):
    fig, axs = plt.subplots(2, 2, sharey=True)
    fig.set_size_inches(12, 12)
    fig.set_dpi(100)

    # Sex F: 1051 data points
    # Sex M: 1589 data points

    # Feminine
    # Age 8: 45 data points
    # Age 9: 250 data points
    # Age 10: 313 data points
    # Age 11: 272 data points
    # Age 12: 105 data points
    # Age 13: 57 data points
    # Age 14: 6 data points
    # Age 19: 3 data points

    # Masculine
    # Age 7: 3 data points
    # Age 8: 66 data points
    # Age 9: 246 data points
    # Age 10: 537 data points
    # Age 11: 413 data points
    # Age 12: 216 data points
    # Age 13: 84 data points
    # Age 14: 18 data points
    # Age 15: 6 data points

    feminine = ACOLE.by_sex('F')
    masculine = ACOLE.by_sex('M')

    for i, ACOLE_by_sex in enumerate([feminine, masculine]):
        # grouped_sexes
        school_years = [3, 4, 5]
        all_data = [ACOLE_by_sex.by_school_year(school_year) for school_year in school_years]

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
        axs[i, 0].set_ylabel('Porcentagem média de acertos')
        if i == 0:
            plot_blocks(axs[i, 0], normal_blocks, top_labels[i], True)
            plot_blocks(axs[i, 1], difficult_blocks, top_labels[i+1], True)
        else:
            plot_blocks(axs[i, 0], normal_blocks, ' ')
            plot_blocks(axs[i, 1], difficult_blocks, ' ')

    handles, labels = axs[1, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.020), ncol=len(school_years))


    fig.text(0.9, 0.8,
        'Meninas', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.9, 0.33,
        'Meninos', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, -0.04, 'Ano escolar', ha='center', va='center', fontsize=12)

    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
Porcentagem média de acertos da primeira ACOLE
com palavras regulares e com dificuldades ortográficas,
por ano escolar e gênero'
"""
def plot():
    bar_plot(ACOLE1, 'Fig19_ano_escolar_sexo')

if __name__ == "__main__":
    plot()