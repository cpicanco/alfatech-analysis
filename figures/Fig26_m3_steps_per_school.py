from databases.students import students
from databases import MODULE3
from Fig26_m3_steps import bar_plot

"""
Número médio de sessões dos passos do módulo 3
completo e incompleto'
"""

def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        filename = f'Fig26_m3_passos_{school}'
        MODULE3_by_school = MODULE3.by_school(school)
        bar_plot(MODULE3_by_school, filename)

if __name__ == "__main__":
    plot()