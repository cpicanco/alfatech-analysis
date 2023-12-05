from databases.students import students
from databases import ACOLE1
from Fig20_forwarding_school_year import bar_plot

"""
Porcentagem média de acertos da primeira ACOLE
com palavras regulares e com dificuldades ortográficas,
por idade e encaminhamento'
"""

def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        ACOLE1_by_school = ACOLE1.by_school(school)
        bar_plot(ACOLE1_by_school, f'Fig20_ano_escolar_encaminhamento_{school}')

if __name__ == "__main__":
    plot()
