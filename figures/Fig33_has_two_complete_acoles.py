from databases.students import students
from databases import ACOLE1, ACOLE2
from Fig30_m1_complete import bar_plot

def plot():
    # for student in students:
    #     if student.modules[0] is not None:
    #         if not student.has_m1:
    #             for s in student.modules[0].PASSO_20.data['sessions']:
    #                 if s is not None:
    #                     if s == 1:
    #                         print(student.id, s, student.has_m1, student.has_m2, student.has_m3)
    ACOLE_1 = ACOLE1.create()
    ACOLE_2 = ACOLE2.create()
    filtered_students = students.create()
    for student in students:
        if student.has_two_complete_acoles():
            acole1, acole2 = student.get_first_and_second_acoles()
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
    com estudantes que avançaram até as palavras com dificuldades ortográficas na primeira ACOLE,
    por faixa de frequência no projeto'
    """
    bar_plot(ACOLE_1, ACOLE_2, use_boxplot=False, filename='Fig34_has_two_complete_acoles')
    bar_plot(ACOLE_1, ACOLE_2, use_boxplot=True, filename='Fig34_has_two_complete_acoles')

if __name__ == "__main__":
   plot()