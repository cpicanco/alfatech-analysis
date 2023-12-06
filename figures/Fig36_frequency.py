from databases.students import students
from methods import opt, histogram, histograms

import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import matplotlib.dates as mdates

"""
    Frequência geral e por escola
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

def bar_plot_2(data, filename, labels):
    opt.set_filename(filename)
    histograms([[student.mean_days_per_week() for student in students] for students in data],
                labels,
                xlabel='Dias por semana (média)',
                ylabel='Número de estudantes',
                range=(0, 3),
                binwidth=0.08,
                bins=30)


def accumulated_frequency_plot(data, schools, filename):
    opt.set_filename(filename)
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5, 5)
    for i, (students, school) in enumerate(zip(data, schools)):
        # Create a list of datetimes from the list of strings
        dates = students.frequencies()
        dates = sorted(dates)
        # Create a list of the accumulated frequencies
        accumulated = [i for i in range(1, len(dates) + 1)]

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x', which='both', bottom=False, top=False)
        # Create a stepped plot
        ax.step(dates, accumulated, where='post', color=f'C{i}', label=school)

    # Format x-axis as dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    # Add labels and title
    plt.xlabel('Data')
    plt.ylabel('Frequência de comparecimento acumulada')

    # Rotate x-axis labels for better readability (optional)
    plt.xticks(rotation=45)

    plt.tight_layout()

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(1.3, 0.5), ncol=1)

    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()


def accumulated_relative_frequency_plot(data, schools, n_per_school, filename):
    opt.set_filename(filename)
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5, 5)
    for i, (students, school, n) in enumerate(zip(data, schools, n_per_school)):
        # Create a list of datetimes from the list of strings
        dates = students.frequencies()
        dates = sorted(dates)

        # calculate relative frequency using the number of students
        accumulated = [i/n for i in range(1, len(dates) + 1)]

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x', which='both', bottom=False, top=False)
        # Create a stepped plot
        ax.step(dates, accumulated, where='post', color=f'C{i}', label=school)

    # Format x-axis as dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    # Add labels and title
    plt.xlabel('Data')
    plt.ylabel('Frequência de comparecimento relativa acumulada')
    # Rotate x-axis labels for better readability (optional)
    plt.xticks(rotation=45)

    plt.tight_layout()
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(1.3, 0.5), ncol=1)

    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()

def plot():
    for student in students:
        student.calculate_days_per_week()
    # bar_plot(students, filename="Fig36_frequency")
    schools = sorted([k for k in students.schools(True).keys()])

    students_by_school_list = []
    for school in schools:
        filename = f'Fig36_frequency_{school}'
        students_by_school = students.by_school(school)
        students_by_school_list.append(students_by_school)
        # bar_plot(students_by_school, filename)

    accumulated_frequency_plot(students_by_school_list, schools, filename="Fig37_frequency_accumulated")
    accumulated_relative_frequency_plot(students_by_school_list, schools, [len(students) for students in students_by_school_list], filename="Fig38_relative_frequency_accumulated")

    # students_by_school_list.append(students)
    # schools.append('Todos')
    # bar_plot_2(students_by_school_list, filename="Fig36_frequency_all", labels=schools)


if __name__ == "__main__":
    plot()