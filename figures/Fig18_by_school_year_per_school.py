from databases.students import students
from databases import ACOLE1
from Fig18_by_school_year import bar_plot

def plot():
    """
    Porcentagem média de acertos da primeira ACOLE
    com palavras regulares e com dificuldades ortográficas, por ano escolar
    """
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        ACOLE1_by_school = ACOLE1.by_school(school)
        bar_plot(ACOLE1_by_school, f'Fig18_ano_escolar_{school}')

if __name__ == "__main__":
    plot()