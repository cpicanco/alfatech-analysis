from databases.students import students
from databases import MODULE2
from Fig25_m2_steps import bar_plot

"""
Número médio de sessões dos passos do Módulo 2
completo e incompleto'
"""

def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig25_m2_passos_{school}'
        MODULE2_by_school = MODULE2.by_school(school)
        bar_plot(MODULE2_by_school, filename)

if __name__ == "__main__":
    plot()