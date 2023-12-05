from databases.students import students
from databases import ACOLE1
from Fig18_by_sex import bar_plot

"""
    Porcentagem média de acertos da primeira ACOLE
    com palavras regulares e com dificuldades ortográficas, por ano escolar
"""
def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig18_sexo_{school}'
        ACOLE1_by_school = ACOLE1.by_school(school)
        bar_plot(ACOLE1_by_school, filename)

if __name__ == "__main__":
    plot()