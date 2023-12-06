from databases.students import students
from methods import opt, histogram, histograms

import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import matplotlib.dates as mdates

"""
    Distribuição da frequência geral e por escola.
"""
def bar_plot(students, filename, use_boxplot=False):
    opt.set_filename(filename)
    if use_boxplot:
        print("Not implemented")
        return
    else:
        histogram([student.mean_days_per_week() for student in students],
                  '',
                  xlabel='Dias por semana (média)',
                  ylabel='Número de estudantes',
                  range=(0, 3),
                  binwidth=0.08,
                  bins=30)


"""
    Distribuição de frequência por escola e geral.
    A média de cada distribuição é mostrada com uma linha tracejada vertical.
"""
def bar_plot_2(data, filename, labels):
    opt.set_filename(filename)
    histograms([[student.mean_days_per_week() for student in students] for students in data],
                labels,
                xlabel='Dias por semana (média)',
                ylabel='Número de estudantes',
                range=(0, 3),
                binwidth=0.08,
                bins=30)

# def accumulated_frequency_plot(data, schools, filename):
#     opt.set_filename(filename)
#     fig, ax = plt.subplots(1, 1)
#     fig.set_size_inches(5, 5)
#     for i, (students, school) in enumerate(zip(data, schools)):
#         # Create a list of datetimes from the list of strings
#         dates = students.frequencies()
#         dates = sorted(dates)
#         # Create a list of the accumulated frequencies
#         accumulated = [i for i in range(1, len(dates) + 1)]

#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['bottom'].set_visible(False)
#         # ax.tick_params(axis='x', which='both', bottom=False, top=False)
#         # Create a stepped plot
#         ax.step(dates, accumulated, where='post', color=f'C{i}', label=school)

#     # Format x-axis as dates
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
#     plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

#     # Add labels and title
#     plt.xlabel('Data')
#     plt.ylabel('Frequência de comparecimento acumulada')

#     # Rotate x-axis labels for better readability (optional)
#     plt.xticks(rotation=45)

#     plt.tight_layout()

#     handles, labels = ax.get_legend_handles_labels()
#     fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(1.3, 0.5), ncol=1)

#     plt.savefig(opt.output_path(), bbox_inches='tight')
#     plt.close()

"""
    Frequência de comparecimento acumulada, em dias.
    Absoluta à esquerda e relativa à direita.

    A medida relativa é calculada dividindo-se o número de dias
    pelo número de estudantes atendimento em cada escola.

"""
def frequency_plot(data, schools, n_per_school, filename):
    opt.set_filename(filename)
    fig, axes = plt.subplots(1, 2)
    fig.set_size_inches(12, 5)

    axes[0].set_ylabel('Frequência absoluta de comparecimento acumulada')
    axes[1].set_ylabel('Frequência relativa de comparecimento acumulada')

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # rotate x labels
        ax.tick_params(axis='x', which='both', bottom=True, top=False, labelrotation=45)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())

    for i, (students, school, n) in enumerate(zip(data, schools, n_per_school)):
        # Create a list of datetimes from the list of strings
        dates = students.frequencies()
        dates = sorted(dates)

        accumulated_absolute = [i for i in range(1, len(dates) + 1)]

        # calculate relative frequency using the number of students
        accumulated = [i/n for i in range(1, len(dates) + 1)]

        # Create a stepped plot
        axes[0].step(dates, accumulated_absolute, where='post', color=f'C{i}', label=school)
        axes[1].step(dates, accumulated, where='post', color=f'C{i}', label=school)

    # Add x and y labels in the middle of figure
    fig.text(0.5, -0.02, 'Data de comparecimento (em dias)', ha='center', va='center', fontsize=12)

    plt.tight_layout()
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.065, 1.0), ncol=1)

    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()

def plot():
    for student in students:
        student.calculate_days_per_week()
    bar_plot(students, filename="Fig36_frequency")
    schools = sorted([k for k in students.schools(True).keys()])

    students_by_school_list = []
    for school in schools:
        filename = f'Fig36_frequency_{school}'
        students_by_school = students.by_school(school)
        students_by_school_list.append(students_by_school)
        bar_plot(students_by_school, filename)

    # accumulated_frequency_plot(students_by_school_list, schools, filename="Fig37_frequency_accumulated")
    frequency_plot(students_by_school_list, schools, [len(students) for students in students_by_school_list], filename="Fig38_relative_frequency_accumulated")

    students_by_school_list.append(students)
    schools.append('Todos')
    bar_plot_2(students_by_school_list, filename="Fig36_frequency_all", labels=schools)


if __name__ == "__main__":
    plot()