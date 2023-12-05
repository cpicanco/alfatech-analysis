from databases.students import students
from databases import MODULE1
from Fig24_m1_steps import bar_plot

"""
Número médio de sessões dos passos do módulo 1
completo e incompleto
"""
def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig24_m1_passos_{school}'
        MODULE1_by_school = MODULE1.by_school(school)
        bar_plot(MODULE1_by_school, filename)

if __name__ == "__main__":
    plot()