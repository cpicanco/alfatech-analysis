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
from sqlalchemy import text

from .engine import geic_db
from .students import students
from .queries import template_from_name
from .containers import ACOLE_Container, MODULE1_Container, MODULE2_Container, MODULE3_Container

def get_trials(trials_data):
    if trials_data == []:
        date = datetime.datetime(1900, 1, 1)
    else:
        date = trials_data[0].DATA_EXECUCAO_INICIO

    trials = [1 if trial.RESULTADO < 1 else 0 for trial in trials_data]
    trials_len = len(trials)
    if trials_len > 0:
        percentage = sum(trials)*100.0/trials_len
        if percentage > 100:
            print('student_id:' + str(student_id),
                'registration_id:' + str(registration_id),
                'program_id:' + str(program_id),
                'block_id:' + str(block_id))
            print(percentage, trials_len)
            print(trials)
            raise Exception('Porcentagem maior que 100%')
    else:
        percentage = None
        trials_len = None
    return (trials, trials_len, percentage, date)

def get_step_trials(connection, registration_id, program_id, step_id, student_id):
    trials_template = template_from_name('step_trials_from_student')
    trials_data = connection.execute(text(trials_template).bindparams(
        REGISTRATION_ID=registration_id,
        PROGRAM_ID=program_id,
        STEP_ID=step_id,
        STUDENT_ID=student_id)).fetchall()
    return get_trials(trials_data)

def get_block_trials(connection, registration_id, program_id, block_id, student_id):
    trials_template = template_from_name('block_trials_from_student')
    trials_data = connection.execute(text(trials_template).bindparams(
        REGISTRATION_ID=registration_id,
        PROGRAM_ID=program_id,
        BLOCK_ID=block_id,
        STUDENT_ID=student_id)).fetchall()
    return get_trials(trials_data)

def get_forwarding_trial(connection, acole_registration_id, acole_id, student_id):
    module_forward_trials_template = template_from_name('module_forward_trials_from_student')
    module_forward_trials = connection.execute(text(module_forward_trials_template).bindparams(
        PROGRAM_ID=acole_id,
        STUDENT_ID=student_id,
        REGISTRATION_ID=acole_registration_id)).fetchall()
    return module_forward_trials[0][0] if module_forward_trials != [] else None

def get_registration(connection, program_id, student_id):
    registration_template = template_from_name('oldest_program_registration_from_student')
    registration = connection.execute(text(registration_template).bindparams(
        PROGRAM_ID=program_id,
        STUDENT_ID=student_id)).fetchall()
    return registration

def get_step_sessions(connection, registration_id, program_id, step_id, student_id):
    sessions_template = template_from_name('session_count_from_program_step')
    sessions = connection.execute(text(sessions_template).bindparams(
        REGISTRATION_ID=registration_id,
        PROGRAM_ID=program_id,
        STEP_ID=step_id,
        STUDENT_ID=student_id)).fetchall()
    return sessions[0][0] if sessions != [] else None

def complete_module(connection, registration_id, student_id, module_id):
    if MODULE1_Container().id == module_id:
        sessions_template = template_from_name('complete_module1_from_registration')
    elif MODULE2_Container().id == module_id:
        sessions_template = template_from_name('complete_module2_from_registration')
    elif MODULE3_Container().id == module_id:
        sessions_template = template_from_name('complete_module3_from_registration')

    result = connection.execute(text(sessions_template).bindparams(
        REGISTRATION_ID=registration_id,
        PROGRAM_ID=module_id,
        STUDENT_ID=student_id)).fetchall()
    if result == []:
        return False
    return False if result[0].IS_COMPLETE == 0 else True

def complete_module_from_student(connection, student_id, module_id):
    if MODULE1_Container().id == module_id:
        sessions_template = template_from_name('complete_module1_from_student')
    elif MODULE2_Container().id == module_id:
        sessions_template = template_from_name('complete_module2_from_student')
    elif MODULE3_Container().id == module_id:
        sessions_template = template_from_name('complete_module3_from_student')

    result = connection.execute(text(sessions_template).bindparams(
        PROGRAM_ID=module_id,
        STUDENT_ID=student_id)).fetchall()
    if result == []:
        return False
    return False if result[0].IS_COMPLETE == 0 else True



def populate_acole_data(ACOLE):
    with open(ACOLE.filename()+'.tsv', 'w', encoding='utf-8') as file:
        file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS']) + '\n')
        # populate ACOLE data
        with geic_db.connect() as connection:
            for student in students:
                # get oldest program's registration
                acole_registration = get_registration(connection, ACOLE.id, student.id)

                if acole_registration == []:
                    continue
                acole_registration_id = acole_registration[0][0]

                student.forward_to(get_forwarding_trial(connection, acole_registration_id, ACOLE.id, student.id))

                for block in ACOLE.blocks:
                    (trials, trials_len, percentage, date) = get_block_trials(connection, acole_registration_id, ACOLE.id, block.id, student.id)
                    trials_len = len(trials)
                    if trials_len > 0:
                        block.data['students'].append(student)
                        block.data['trials'].append(trials)
                        block.data['percentages'].append(percentage)
                    else:
                        percentage = None
                        trials_len = None
                    info = '\t'.join([
                        student.name,
                        str(student.id),
                        block.legend,
                        str(block.id),
                        date.strftime('%d/%m/%Y'),
                        str(acole_registration_id),
                        str(percentage),
                        str(trials_len)])
                    # print(info)
                    file.write(info + '\n')

def populate_module_data(MODULE):
    with open(MODULE.filename()+'.tsv', 'w', encoding='utf-8') as file:
        file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS', 'TOTAL_SESSOES']) + '\n')
        with geic_db.connect() as connection:
            for student in students:
                module1_registrations = get_registration(connection, MODULE.id, student.id)
                if module1_registrations == []:
                    continue
                print(student.name)

                if len(module1_registrations) > 0:
                    complete_registrations = [r[0] for r in module1_registrations if complete_module(connection, r[0], student.id, MODULE.id)]
                    incomplete_registrations = [r[0] for r in module1_registrations if not complete_module(connection, r[0], student.id, MODULE.id)]
                    if len(complete_registrations) > 0:
                        student.set_completion(MODULE.id, True)
                        target_registrations = [complete_registrations[0]]
                    else:
                        student.set_completion(MODULE.id, complete_module_from_student(connection, student.id, MODULE.id))
                        target_registrations = [r for r in incomplete_registrations]

                # get forward trials for student
                for block in MODULE.blocks:
                    if len(target_registrations) == 1:
                        rid = target_registrations[0]
                        sessions = get_step_sessions(connection, rid, MODULE.id, block.id, student.id)

                        if block.min_trials < 0:
                            (trials, trials_len, percentage, date) = get_step_trials(connection, rid, MODULE.id, block.id, student.id)
                        else:
                            (trials, trials_len, percentage, date) = get_block_trials(connection, rid, MODULE.id, block.id, student.id)

                    else:
                        trials = []
                        sessions = 0
                        for rid in target_registrations:
                            step_sessions = get_step_sessions(connection, rid, MODULE.id, block.id, student.id)
                            if step_sessions is not None:
                                sessions += step_sessions

                            if block.min_trials < 0:
                                (t, _, _, date) = get_step_trials(connection, rid, MODULE.id, block.id, student.id)
                            else:
                                (t, _, _, date) = get_block_trials(connection, rid, MODULE.id, block.id, student.id)
                            trials += t

                    trials_len = len(trials)
                    if trials_len > 0:
                        block.data['students'].append(student)
                        block.data['trials'].append(trials)
                        block.data['percentages'].append(percentage)
                        block.data['sessions'].append(sessions)
                    else:
                        percentage = None
                        trials_len = None
                        sessions = None

                    info = '\t'.join([
                        student.name,
                        str(student.id),
                        block.legend,
                        str(block.id),
                        date.strftime('%d/%m/%Y'),
                        str(target_registrations),
                        str(percentage),
                        str(trials_len),
                        str(sessions)])
                    # print(info)
                    file.write(info + '\n')

if ACOLE_Container.cache_exists():
    print('Loading ACOLE from cache')
    ACOLE = ACOLE_Container.load_from_file()
else:
    print('Populating ACOLE cache')
    ACOLE = ACOLE_Container()
    populate_acole_data(ACOLE)
    ACOLE.save_to_file()

if MODULE1_Container.cache_exists():
    print('Loading MODULE 1 from cache')
    MODULE1 = MODULE1_Container.load_from_file()
else:
    print('Populating MODULE 1 cache')
    MODULE1 = MODULE1_Container()
    populate_module_data(MODULE1)
    MODULE1.save_to_file()

if MODULE2_Container.cache_exists():
    print('Loading MODULE 2 from cache')
    MODULE2 = MODULE2_Container.load_from_file()
else:
    print('Populating MODULE 2 cache')
    MODULE2 = MODULE2_Container()
    populate_module_data(MODULE2)
    MODULE2.save_to_file()

if MODULE3_Container.cache_exists():
    print('Loading MODULE 3 from cache')
    MODULE3 = MODULE3_Container.load_from_file()
else:
    print('Populating MODULE 3 cache')
    MODULE3 = MODULE3_Container()
    populate_module_data(MODULE3)
    MODULE3.save_to_file()