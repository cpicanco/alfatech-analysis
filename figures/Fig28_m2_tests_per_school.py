from databases.students import students
from Fig28_m2_tests import bar_plot

def plot():
    """
    Porcentagem média de acertos na ACOLE inicial
    testes de Módulo 2 (completo) e ACOLE final
    """
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig28_m2_testes_{school}'
        students_by_school = students.by_school(school)
        bar_plot(students_by_school, use_boxplot=False, filename=filename)
        bar_plot(students_by_school, use_boxplot=True,  filename=filename)

if __name__ == "__main__":
    plot()