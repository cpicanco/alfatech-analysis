from databases.students import students
from databases import ACOLE1, ACOLE2

from Fig30_m1_complete import bar_plot


def plot():
    ACOLE_1 = ACOLE1.create()
    ACOLE_2 = ACOLE2.create()
    filtered_students = students.create()

    for student in students:
        if student.has_two_acoles_first_incomplete():
            acole1, acole2 = student.get_first_and_last_acoles()
            if student.has_m2:
                filtered_students.append(student)
                for block, student_block in zip(ACOLE_1.blocks, student.acoles[acole1].blocks):
                    for key, data in student_block.data.items():
                        if len(data) > 0:
                            block.data[key].append(data[0])

                for block, student_block in zip(ACOLE_2.blocks, student.acoles[acole2].blocks):
                    for key, data in student_block.data.items():
                        if len(data) > 0:
                            block.data[key].append(data[0])
        """
    Diferença entre a porcentagem de acertos na ACOLE final e inicial,
    completas, de estudantes com Módulo 2 completo,
    com estudantes que avançaram até as palavras com dificuldades ortográficas na primeira ACOLE,
    or faixa de frequência no projeto
    """
    bar_plot(ACOLE_1, ACOLE_2, use_boxplot=False, filename='Fig31_m2_completo_primeira_acole_incompleta')
    bar_plot(ACOLE_1, ACOLE_2, use_boxplot=True, filename='Fig31_m2_completo_primeira_acole_incompleta')

if __name__ == "__main__":
   plot()