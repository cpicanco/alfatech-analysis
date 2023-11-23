# python modules
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
        file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS']) + '\n')
        # populate ACOLE data
        with geic_db.connect() as connection:
            students = connection.execute(text(students_template)).fetchall()
            for student_data in students:
                if 'DUPLICATA DESCONSIDERAR' in student_data.FULLNAME:
                    continue

                student = student_data.ID

                acole_registration_template = text(oldest_acole_template).bindparams(
                    STUDENT_ID=student,
                    PROGRAM_ID=ACOLE.id)
                acole_registration_query = connection.execute(acole_registration_template)
                acole_registration = acole_registration_query.fetchall()
                if acole_registration == []:
                    continue
                acole_registration_id = acole_registration[0][0]

                def get_trials(block_id):
                    trials = connection.execute(text(trials_template).bindparams(
                        PROGRAM_ID=ACOLE.id,
                        STUDENT_ID=student,
                        REGISTRATION_ID=acole_registration_id,
                        BLOCK_ID=block_id)).fetchall()
                    if trials == []:
                        date = datetime.datetime(1900, 1, 1)
                    else:
                        date = trials[0].DATA_EXECUCAO_INICIO

                    return ([1 if trial.RESULTADO < 1 else 0 for trial in trials], date)

                for block in ACOLE.blocks:
                    (trials, date) = get_trials(block.id)
                    trials_len = len(trials)
                    if trials_len > 0:
                        block.data['students'].append(student_data)
                        percentage = sum(trials)*100.0/trials_len
                        if percentage > 100:
                            print(ACOLE.student_fullname(student_data) + '(ID:' + str(student) + ')' + ' - ',
                                block.legend + '(ID:' + str(acole_registration_id) + ')',
                                percentage, trials_len)
                            print(trials)
                            raise Exception('Porcentagem maior que 100%')

                        block.data['trials'].append(trials)
                        block.data['percentages'].append(percentage)
                    else:
                        percentage = None
                        trials_len = None
                    info = '\t'.join([
                        ACOLE.student_fullname(student_data),
                        str(student),
                        block.legend,
                        str(block.id),
                        date.strftime('%d/%m/%Y'),
                        str(acole_registration_id),
                        str(percentage),
                        str(trials_len)])
                    # print(info)
                    file.write(info + '\n')

def percentages_from_block(block):
    percentages = block.data['percentages']
    percentages = [p for p in percentages if p is not None]
    if len(percentages) > 0:
        bar_value = np.mean(percentages)
        std_dev = np.std(percentages)
    else:
        bar_value = np.nan
        std_dev = np.nan

    return bar_value, std_dev

def mean_porcentage_from_blocks(blocks):
    bar_values = []
    bar_std = []
    for block in blocks:
        bar_value, bar_std_value = percentages_from_block(block)
        bar_values.append(bar_value)
        bar_std.append(bar_std_value)
    return bar_values, bar_std

def min_max_values_from_blocks(blocks):
    bar_values = []
    bar_min = []
    bar_max = []
    for block in blocks:
        percentages = block.data['percentages']
        percentages = [p for p in percentages if p is not None]
        if len(percentages) > 0:
            bar_value = np.mean(percentages)
            bar_min.append(np.min(bar_value))
            bar_max.append(np.max(bar_value))
        else:
            bar_value = np.nan
            bar_min.append(np.nan)
            bar_max.append(np.nan)
        bar_values.append(bar_value)
    return bar_values, bar_min, bar_max

# def plot_blocks_b(ax, blocks, title):
#     bar_positions = np.arange(len(blocks))

#     bar_values, bar_min, bar_max = min_max_values_from_blocks(blocks)

#     ax.set_title(title)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     ax.tick_params(axis='x', which='both', bottom=False, top=False)

#     # Plotting the range between min and max
#     ax.fill_between(bar_positions, bar_min, bar_max, color='lightgray', alpha=0.5, label='Range')

#     # Plotting a line at the mean value
#     ax.plot(bar_positions, bar_values, marker='o', linestyle='-', color='black', label='Mean')

#     ax.set_xticks(bar_positions)
#     ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n') for block in blocks])

#     # Annotate each bar with its min and max values
#     for pos, min_val, max_val in zip(bar_positions, bar_min, bar_max):
#         ax.text(pos, max_val + 2, f'{max_val:.1f}%', ha='center', color='black')
#         ax.text(pos, min_val - 2, f'{min_val:.1f}%', ha='center', color='black')

def boxplot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    data = [[p for p in block.data['percentages'] if p is not None] for block in blocks]
    boxprops = dict(linewidth=2, color='black')
    medianprops = dict(linewidth=2, color='black')

    bp = ax.boxplot(data, positions=bar_positions, widths=0.6, showfliers=False, boxprops=boxprops, medianprops=medianprops)

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n') for block in blocks])

    # Annotate mean, min, and max for each block
    for i, box in enumerate(bp['boxes']):
        pos = bar_positions[i]
        mean_val = np.mean(data[i])
        min_val = np.min(data[i])
        max_val = np.max(data[i])

        ax.text(pos, 95 , f'M={mean_val:.1f}%', ha='center', color='black')
        ax.text(pos, min_val - 5, f'{min_val:.1f}%', ha='center', color='black')
        ax.text(pos, max_val + 2, f'{max_val:.1f}%', ha='center', color='black')

def statistics_from_blocks(blocks):
    bar_values, bar_stds, bar_lengths, bar_medians = [], [], [], []
    for block in blocks:
        value, std = percentages_from_block(block)
        bar_values.append(value)
        bar_stds.append(std)
        bar_lengths.append(len([p for p in block.data['percentages'] if p is not None]))
        bar_medians.append(np.median(block.data['percentages']))
    return bar_values, bar_stds, bar_lengths, bar_medians

def plot_blocks(ax, blocks, title):
    bar_positions = np.arange(len(blocks))

    bar_values, bar_stds, bar_lengths, bar_medians = statistics_from_blocks(blocks)

    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

    bars = ax.bar(bar_positions, bar_values)

    ax.set_xticks(bar_positions)
    ax.set_xticklabels([block.legend.replace('Ditado ', 'Ditado\n') for block in blocks])

     # Annotate mean and sigma on top of each column
    for bar, value, position, std, blen, bme in zip(bars, bar_values, bar_positions, bar_stds, bar_lengths, bar_medians):
        x_pos = bar.get_x() + bar.get_width() / 2
        y_pos = value + 20
        ax.text(x_pos, y_pos, f'{value:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 5, f'Me = {bme:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 10, f'σ = {std:.1f}', ha='center', color='black')
        ax.text(x_pos, y_pos - 15, f'n = {blen}', ha='center', color='black')


def bar_plot_regular_difficult_groups(ACOLE):
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.set_size_inches(8, 5)
    fig.set_dpi(100)
    fig.suptitle('Média da porcentagem de acertos da primeira ACOLE\ncom palavras regulares e com dificuldades ortográficas')

    # Group 1 - Regular Blocks
    normal_blocks = [
        ACOLE.LEITURA,
        ACOLE.DITADO_COMPOSICAO,
        ACOLE.DITADO_MANUSCRITO]

    plot_blocks(axs[0], normal_blocks, 'Palavras regulares')

    # Group 2 - Difficult Blocks
    difficult_blocks = [
        ACOLE.LEITURA_DIFICULDADES,
        ACOLE.DITADO_COMPOSICAO_DIFICULDADES,
        ACOLE.DITADO_MANUSCRITO_DIFICULDADES]

    plot_blocks(axs[1], difficult_blocks, 'Palavras com\ndificuldades ortográficas')

    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, 'figures', 'Fig17.png'), bbox_inches='tight')

if __name__ == "__main__":
    if ACOLE.cache_exists():
        print('Loading from cache')
        ACOLE = ACOLE.load_from_file()
    else:
        print('Populating cache')
        populate_acole_data()
        ACOLE.save_to_file()

    # bar_plot_regular_difficult_groups(ACOLE)
    # ages_count = ACOLE.ages(count=True)

    # sorted_ages_count = dict(sorted(ages_count.items()))

    # for age, count in sorted_ages_count.items():
    #     print(f"Age {age}: {count} data points")


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

    A = [ACOLE.by_age(ages) for ages in [[7, 8], [9], [10], [11], [12], [13, 14, 15, 19]]]
    for data in A:
        for block in data.blocks:
            print(block.legend, len(block.data['percentages']))


