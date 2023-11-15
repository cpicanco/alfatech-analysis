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

                    return ([trial.RESULTADO if trial.RESULTADO <= 1 else 0 for trial in trials], date)

                for block in ACOLE.blocks:
                    (trials, date) = get_trials(block)
                    trials_len = len(trials)
                    if trials_len > 0:
                        ACOLE.data[block]['students'].append(student_data)
                        porcentage = sum(trials)*100.0/trials_len
                        if porcentage > 100:
                            print(ACOLE.student_fullname(student_data) + '(ID:' + str(student) + ')' + ' - ',
                                ACOLE.data[block]['legend'] + '(ID:' + str(acole_registration_id) + ')',
                                porcentage, trials_len)
                            print(trials)
                            raise Exception('Porcentagem maior que 100%')

                        ACOLE.data[block]['trials'].append(trials)
                        ACOLE.data[block]['porcentages'].append(porcentage)
                    else:
                        porcentage = None
                        trials_len = None
                    info = '\t'.join([
                        ACOLE.student_fullname(student_data),
                        str(student),
                        ACOLE.data[block]['legend'],
                        date.strftime('%d/%m/%Y'),
                        str(acole_registration_id),
                        str(porcentage),
                        str(trials_len)])
                    print(info)
                    file.write(info + '\n')

# bar plot with mean results for block
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
            np.mean(ACOLE.data[block_id]['porcentages']),
            yerr=np.std(ACOLE.data[block_id]['porcentages']),
            label=ACOLE.data[block_id]['legend'])

    ax.legend()

    plt.savefig(os.path.join(base_dir, 'figures', 'Fig17.png'), bbox_inches='tight')

def bar_plot_regular_difficult_groups():
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    fig.set_dpi(100)

    ax.set_title('Média da porcentagem de acertos da primeira ACOLE\ncom palavras regulares e com dificuldades ortográficas')
    ax.set_xlabel('Bloco de palavras')
    ax.set_ylabel('Porcentagem de acertos')

    normal_blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO]

    difficult_blocks = [
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    categories = [ACOLE.data[block_id]['legend'] for block_id in normal_blocks]

    ax.set_ylim(0, 100)

    bar_width = 0.35
    # Calculate the positions for the bars
    bar_positions_regular = np.arange(len(categories))
    bar_positions_difficu = bar_positions_regular + bar_width

    bar_values_regular = []
    bas_std_regular = []
    for block_id in normal_blocks:
        bar_values_regular.append(np.mean(ACOLE.data[block_id]['porcentages']))
        bas_std_regular.append(np.std(ACOLE.data[block_id]['porcentages']))
    bar_values_regular = np.array(bar_values_regular)

    bar_values_difficu = []
    bar_std_difficu = []
    for block_id in difficult_blocks:
        bar_values_difficu.append(np.mean(ACOLE.data[block_id]['porcentages']))
        bar_std_difficu.append(np.std(ACOLE.data[block_id]['porcentages']))

    bar_values_difficu = np.array(bar_values_difficu)
    ax.bar(
        bar_positions_regular,
        bar_values_regular,
        width=bar_width,
        yerr=bas_std_regular,
        label='Regulares')

    ax.bar(
        bar_positions_difficu,
        bar_values_difficu,
        width=bar_width,
        yerr=bar_std_difficu,
        label='Com dificuldades ortográficas')

    plt.legend(loc='upper left')
    plt.xticks(bar_positions_regular + bar_width / 2, categories)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    plt.savefig(os.path.join(base_dir, 'figures', 'Fig17.png'), bbox_inches='tight')

if __name__ == "__main__":
    if ACOLE.cache_exists():
        ACOLE = ACOLE.load_from_file()
    else:
        populate_acole_data()
        ACOLE.save_to_file()

    # bar_plot_mean_trial_results(ACOLE.blocks)
    bar_plot_regular_difficult_groups()