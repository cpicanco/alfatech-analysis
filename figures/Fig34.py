from databases.students import students
from databases import ACOLE1, ACOLE2
from Fig30 import bar_plot

def plot():
    # ACOLE_1 = ACOLE1.create()
    # ACOLE_2 = ACOLE2.create()
    # filtered_students = students.create()

    for student in students:
        if len(student.modules) > 0:
            for module in student.modules:
                for block in module.blocks:
                    # print(block.data['sessions'])
                    for s in block.data['sessions']:
                        if s is not None:
                            if s > 5:
                                print(student.id, s, student.has_m1, student.has_m2, student.has_m3)

    # for student in students:
    #     if student.has_two_acoles():
    #         acole1, acole2 = student.get_first_and_second_acoles()
    #         if len(student.modules) > 0:
    #             filtered_students.append(student)
    #             for block, student_block in zip(ACOLE_1.blocks, student.acoles[acole1].blocks):
    #                 for key, data in student_block.data.items():
    #                     if len(data) > 0:
    #                         block.data[key].append(data[0])

    #             for block, student_block in zip(ACOLE_2.blocks, student.acoles[acole2].blocks):
    #                 for key, data in student_block.data.items():
    #                     if len(data) > 0:
    #                         block.data[key].append(data[0])

    # """
    # Diferença entre a porcentagem de acertos na ACOLE final e inicial,
    # com estudantes que avançaram até as palavras com dificuldades ortográficas na primeira ACOLE,
    # por faixa de frequência no projeto'
    # """
    # bar_plot(ACOLE_1, ACOLE_2, use_boxplot=False, filename='Fig34')
    # bar_plot(ACOLE_1, ACOLE_2, use_boxplot=True, filename='Fig34')

if __name__ == "__main__":
   plot()