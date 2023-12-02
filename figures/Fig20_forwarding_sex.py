import matplotlib.pyplot as plt
import numpy as np

from databases import ACOLE1
from methods import output_path

from Fig17 import top_labels
from Fig18_by_sex import plot_blocks

def bar_plot(ACOLE, filename):
    fig, axs = plt.subplots(3, 2, sharey=True)
    fig.set_size_inches(12, 18)
    fig.set_dpi(100)

    m1 = ACOLE.by_forwarding('Módulo 1')
    m2 = ACOLE.by_forwarding('Módulo 2')
    m3 = ACOLE.by_forwarding('Módulo 3')

    for i, ACOLE_by_module in enumerate([m1, m2, m3]):
        # grouped_sexes

        sexes = ['F', 'M']

        all_data = [ACOLE_by_module.by_sex(sex) for sex in sexes]

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
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.020), ncol=len(sexes))

    fig.text(0.5, 1.01,
        'Encaminhamento para o Módulo 1', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, 0.65,
        'Encaminhamento para o Módulo 2', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, 0.31,
        'Encaminhamento para o Módulo 3', ha='center', va='center', fontsize=12, color='black', weight='bold', backgroundcolor='white')

    fig.text(0.5, -0.04, 'Gênero', ha='center', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path(filename), bbox_inches='tight')
    plt.close()

"""
Porcentagem média de acertos da primeira ACOLE
com palavras regulares e com dificuldades ortográficas,
por idade e encaminhamento'
"""

def plot():
    bar_plot(ACOLE1, 'Fig20_sexo_encaminhamento')

if __name__ == "__main__":
    plot()
