from databases import MODULE1, ACOLE1, ACOLE2
from databases.students import students
from Fig27_m1_tests import do_plot

def plot():
    """
    Porcentagem média de acertos na ACOLE inicial
    testes de Módulo 1 e ACOLE final'
    """
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig27_m1_testes_{school}'
        ACOLE1_by_school = ACOLE1.by_school(school)
        MODULE1_by_school = MODULE1.by_school(school)
        ACOLE2_by_school = ACOLE2.by_school(school)
        do_plot(ACOLE1_by_school, MODULE1_by_school, ACOLE2_by_school, use_boxplot=False, filename=filename)
        do_plot(ACOLE1_by_school, MODULE1_by_school, ACOLE2_by_school, use_boxplot=True,  filename=filename)


if __name__ == "__main__":
    plot()