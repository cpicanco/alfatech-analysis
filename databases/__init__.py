"""
# you should use python env to install the following packages to avoid dependency conflicts
py -m pip install mysql-connector-python
py -m pip install SQLAlchemy
"""
# python
import os
import sys
import datetime

# database
from sqlalchemy import create_engine, text

from .queries import template_from_name
from .containers import ACOLE_Container, Student

geic_db = create_engine('mysql+mysqlconnector://root:@localhost/geic', echo=False)

# project
ALPHATEC = 132

MODULE1 = 143
MODULE2 = 377
MODULE3 = 383

def populate_acole_data(ACOLE):
    # get template files
    students_template = template_from_name('students_from_alphatech')
    oldest_acole_template = template_from_name('oldest_program_registration_from_student')
    trials_template = template_from_name('trials_from_student')
    module_forward_trials_template = template_from_name('module_forward_trials_from_student')

    with open(ACOLE.filename()+'.tsv', 'w', encoding='utf8') as file:
        file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS']) + '\n')
        # populate ACOLE data
        with geic_db.connect() as connection:
            students = connection.execute(text(students_template)).fetchall()
            for student_data in students:
                if 'DUPLICATA DESCONSIDERAR' in student_data.FULLNAME:
                    continue

                student = student_data.ID

                # get oldest acole registration
                acole_registration_template = text(oldest_acole_template).bindparams(
                    PROGRAM_ID=ACOLE.id,
                    STUDENT_ID=student)
                acole_registration_query = connection.execute(acole_registration_template)
                acole_registration = acole_registration_query.fetchall()
                # print('registration:', acole_registration)
                if acole_registration == []:
                    continue
                acole_registration_id = acole_registration[0][0]

                # get forward trials for student
                module_forward_trials = connection.execute(text(module_forward_trials_template).bindparams(
                    PROGRAM_ID=ACOLE.id,
                    STUDENT_ID=student,
                    REGISTRATION_ID=acole_registration_id)).fetchall()
                # print('trial/registration:', module_forward_trials)
                forwarding = module_forward_trials[0][0] if module_forward_trials != [] else None
                def get_trials(block_id):
                    trials = connection.execute(text(trials_template).bindparams(
                        PROGRAM_ID=ACOLE.id,
                        STUDENT_ID=student,
                        REGISTRATION_ID=acole_registration_id,
                        BLOCK_ID=block_id)).fetchall()
                    if trials == []:
                        date = datetime.datetime(1900, 1, 1)
                    else:
                        date = trials[0].DATA_EXECUCAO_INICIO

                    return ([1 if trial.RESULTADO < 1 else 0 for trial in trials], date)

                for block in ACOLE.blocks:
                    (trials, date) = get_trials(block.id)
                    trials_len = len(trials)
                    if trials_len > 0:
                        block.data['students'].append(Student(student_data, forwarding))
                        percentage = sum(trials)*100.0/trials_len
                        if percentage > 100:
                            print(ACOLE.student_fullname(student_data) + '(ID:' + str(student) + ')' + ' - ',
                                block.legend + '(ID:' + str(acole_registration_id) + ')',
                                percentage, trials_len)
                            print(trials)
                            raise Exception('Porcentagem maior que 100%')

                        block.data['trials'].append(trials)
                        block.data['percentages'].append(percentage)
                    else:
                        percentage = None
                        trials_len = None
                    info = '\t'.join([
                        ACOLE.student_fullname(student_data),
                        str(student),
                        block.legend,
                        str(block.id),
                        date.strftime('%d/%m/%Y'),
                        str(acole_registration_id),
                        str(percentage),
                        str(trials_len)])
                    # print(info)
                    file.write(info + '\n')

ACOLE = ACOLE_Container()

if ACOLE.cache_exists():
    print('Loading from cache')
    ACOLE = ACOLE.load_from_file()
else:
    print('Populating cache')
    populate_acole_data()
    ACOLE.save_to_file()