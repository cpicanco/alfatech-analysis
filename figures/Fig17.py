# python modulararization
import os
import sys
import datetime

base_dir = os.path.abspath(__file__).rsplit("figures", 1)[0]
sys.path.append(os.path.join(base_dir))

# graphication
import matplotlib.pyplot as plt
import numpy as np

# database
from sqlalchemy import text

from queries import template_from_name
from databases import geic_db, ACOLE

def populate_acole_data():
    # get template files
    students_template = template_from_name('students_from_alphatech')
    oldest_acole_template = template_from_name('oldest_program_registration_from_student')
    trials_template = template_from_name('trials_from_student')


    with open(ACOLE.filename()+'.tsv', 'w', encoding='utf8') as file:
        file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS']) + '\n')
        # populate ACOLE data
        with geic_db.connect() as connection:
            students = connection.execute(text(students_template)).fetchall()
            for student_data in students:
                if 'DUPLICATA DESCONSIDERAR' in student_data.FULLNAME:
                    continue

                student = student_data.ID

                acole_registration_template = text(oldest_acole_template).bindparams(
                    STUDENT_ID=student,
                    PROGRAM_ID=ACOLE.ID)
                acole_registration_query = connection.execute(acole_registration_template)
                acole_registration = acole_registration_query.fetchall()
                if acole_registration == []:
                    continue
                acole_registration_id = acole_registration[0][0]

                def get_trials(block_id):
                    trials = connection.execute(text(trials_template).bindparams(
                        STUDENT_ID=student,
                        REGISTRATION_ID=acole_registration_id,
                        BLOCK_ID=block_id)).fetchall()
                    if trials == []:
                        date = datetime.datetime(1900, 1, 1)
                    else:
                        date = trials[0].DATA_EXECUCAO_INICIO
                    if student == 10157:
                        print('ANTES:', trials)
                    return ([1 if trial.RESULTADO < 1 else 0 for trial in trials], date)

                for block in ACOLE.blocks:
                    (trials, date) = get_trials(block)
                    trials_len = len(trials)
                    if trials_len > 0:
                        if student == 10157:
                            print('DEPOIS:', trials)
                        ACOLE.data[block]['students'].append(student_data)
                        percentage = sum(trials)*100.0/trials_len
                        if percentage > 100:
                            print(ACOLE.student_fullname(student_data) + '(ID:' + str(student) + ')' + ' - ',
                                ACOLE.data[block]['legend'] + '(ID:' + str(acole_registration_id) + ')',
                                percentage, trials_len)
                            print(trials)
                            raise Exception('Porcentagem maior que 100%')

                        ACOLE.data[block]['trials'].append(trials)
                        ACOLE.data[block]['percentages'].append(percentage)
                    else:
                        percentage = None
                        trials_len = None
                    info = '\t'.join([
                        ACOLE.student_fullname(student_data),
                        str(student),
                        ACOLE.data[block]['legend'],
                        date.strftime('%d/%m/%Y'),
                        str(acole_registration_id),
                        str(percentage),
                        str(trials_len)])
                    print(info)
                    file.write(info + '\n')

def bar_plot_mean_trial_results(ACOLE_block_ids):
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    fig.set_dpi(100)

    ax.set_title('Média de acertos por bloco')
    ax.set_xlabel('Bloco')
    ax.set_ylabel('Porcentagem de certos')

    ax.set_xticks(np.arange(len(ACOLE_block_ids)))
    ax.set_xticklabels([ACOLE.data[block_id]['legend'] for block_id in ACOLE_block_ids])

    ax.set_ylim(0, 100)

    for block_id in ACOLE_block_ids:
        ax.bar(
            ACOLE_block_ids.index(block_id),
            np.mean(ACOLE.data[block_id]['percentages']),
            yerr=np.std(ACOLE.data[block_id]['percentages']),
            label=ACOLE.data[block_id]['legend'])

    ax.legend()

    plt.savefig(os.path.join(base_dir, 'figures', 'Fig17.png'), bbox_inches='tight')

def mean_porcentage_from_block(Container, block_id):
    percentages = Container.data[block_id]['percentages']
    percentages = [p for p in percentages if p is not None]
    if len(percentages) > 0:
        bar_value = np.mean(percentages)
        bar_std = np.std(percentages)
    else:
        bar_value = np.nan
        bar_std = np.nan
    return bar_value, bar_std

def mean_porcentage_from_blocks(Container, block_ids):
    bar_values = []
    bar_std = []
    for block_id in block_ids:
        bar_value, bar_std_value = mean_porcentage_from_block(Container, block_id)
        bar_values.append(bar_value)
        bar_std.append(bar_std_value)
    return bar_values, bar_std

def bar_plot_regular_difficult_groups():
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(8, 5)
    fig.set_dpi(100)
    fig.suptitle('Média da porcentagem de acertos da primeira ACOLE\ncom palavras regulares e com dificuldades ortográficas')

    for ax in axs:
        ax.set_ylim(0, 100)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x', which='both', bottom=False, top=False)

    # Group 1 - Regular Blocks
    normal_blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO]

    categories = [ACOLE.data[block_id]['legend'].replace('Ditado ', 'Ditado\n') for block_id in normal_blocks]
    bar_positions = np.arange(len(normal_blocks))

    bar_values, bar_std = mean_porcentage_from_blocks(ACOLE, normal_blocks)

    axs[0].set_ylabel('Porcentagem de acertos')
    axs[0].set_title('Palavras regulares')
    axs[0].bar(
        bar_positions,
        bar_values,
        yerr=bar_std)

    axs[0].set_xticks(bar_positions)
    axs[0].set_xticklabels(categories)

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    bar_positions = np.arange(len(difficult_blocks))

    bar_values, bar_std = mean_porcentage_from_blocks(ACOLE, difficult_blocks)

    axs[1].set_title('Palavras com\ndificuldades ortográficas')
    axs[1].spines['left'].set_visible(False)
    axs[1].bar(
        bar_positions,
        bar_values,
        yerr=bar_std)

    axs[1].set_xticks(bar_positions)
    axs[1].set_xticklabels(categories)

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'figures', 'Fig17.png'), bbox_inches='tight')

# Call the function
bar_plot_regular_difficult_groups()

if __name__ == "__main__":
    if ACOLE.cache_exists():
        ACOLE = ACOLE.load_from_file()
    else:
        populate_acole_data()
        ACOLE.save_to_file()

    # bar_plot_mean_trial_results(ACOLE.blocks)
    bar_plot_regular_difficult_groups()