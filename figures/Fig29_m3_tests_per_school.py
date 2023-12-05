from databases.students import students
from Fig29_m3_tests import bar_plot


def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig29_m3_tests_{school}'
        students_by_school = students.by_school(school)
        bar_plot(students_by_school, use_boxplot=False, filename=filename)
        bar_plot(students_by_school, use_boxplot=True,  filename=filename)

if __name__ == "__main__":
    plot()