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
from .students import students, cache_students
from .queries import template_from_name

from .containers import ACOLE1_Container,  ACOLE2_Container,  ACOLE3_Container
from .containers import MODULE1_Container, MODULE2_Container, MODULE3_Container

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

def get_frequency_from_student(connection, student_id):
    frequency_template = template_from_name('frequency_from_student')
    frequency = connection.execute(text(frequency_template).bindparams(
        STUDENT_ID=student_id)).fetchall()
    return [f[0] for f in frequency if frequency != []]

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

def complete_acole(connection, registration_id, student_id, acole_id):
    sessions_template = template_from_name('complete_acole_from_registration')
    result = connection.execute(text(sessions_template).bindparams(
        REGISTRATION_ID=registration_id,
        PROGRAM_ID=acole_id,
        STUDENT_ID=student_id)).fetchall()
    if result == []:
        return False
    return False if result[0].IS_COMPLETE == 0 else True


def populate_acole_data(ACOLE, registration_index=0):
    forwarding_modules = {
        32216 : 'Módulo 1',
        33048 : 'Módulo 2',
        33049 : 'Módulo 3',
        None : None
    }
    with open(ACOLE.filename()+'.tsv', 'w', encoding='utf-8') as file:
        # file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS']) + '\n')
        # file.write('\t'.join(['NOME', 'ID', 'MATRICULA.ID.COMPLETAS', 'MATRICULA.ID.INCOMPLETAS', 'ENCAMINHAMENTO'])+'\n')
        with geic_db.connect() as connection:
            for student in students:
                if student.frequency is None:
                    student.frequency = get_frequency_from_student(connection, student.id)
                    student.calculate_days_per_week()

                acole_registration = get_registration(connection, ACOLE.id, student.id)

                # complete_registrations = [r[0] for r in acole_registration if complete_acole(connection, r[0], student.id, ACOLE.id)]
                # incomplete_registrations = [r[0] for r in acole_registration if not complete_acole(connection, r[0], student.id, ACOLE.id)]
                # forwardings = [str(r[0])+'->'+str(forwarding_modules[get_forwarding_trial(connection, r[0], ACOLE.id, student.id)]) for r in acole_registration]
                # file.write('\t'.join([student.name, str(student.id), str(complete_registrations), str(incomplete_registrations), str(forwardings)])+'\n')
                if registration_index >= len(acole_registration):
                    continue

                acole_registration_id = acole_registration[registration_index][0]

                student.forward_to(get_forwarding_trial(connection, acole_registration_id, ACOLE.id, student.id))
                student.acoles.append(ACOLE.create())
                student.acoles_is_complete.append(complete_acole(connection, acole_registration_id, student.id, ACOLE.id))
                for block, student_block in zip(ACOLE.blocks, student.acoles[-1].blocks):
                    (trials, trials_len, percentage, date) = get_block_trials(connection, acole_registration_id, ACOLE.id, block.id, student.id)
                    trials_len = len(trials)
                    if trials_len > 0:
                        block.data['students'].append(student)
                        block.data['trials'].append(trials)
                        block.data['percentages'].append(percentage)
                        block.data['sessions'].append(1)
                        student_block.data['students'].append(student)
                        student_block.data['trials'].append(trials)
                        student_block.data['percentages'].append(percentage)
                        student_block.data['sessions'].append(1)
                    else:
                        percentage = None
                        trials_len = None
                    # info = '\t'.join([
                    #     student.name,
                    #     str(student.id),
                    #     block.legend,
                    #     str(block.id),
                    #     date.strftime('%d/%m/%Y'),
                    #     str(acole_registration_id),
                    #     str(percentage),
                    #     str(trials_len)])
                    # print(info)
                    # file.write(info + '\n')

def populate_module_data(MODULE):
    with open(MODULE.filename()+'.tsv', 'w', encoding='utf-8') as file:
        # file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS', 'TOTAL_SESSOES']) + '\n')
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

                student.modules.append(MODULE.create())
                for block, student_block in zip(MODULE.blocks, student.modules[-1].blocks):
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
                        student_block.data['students'].append(student)
                        student_block.data['trials'].append(trials)
                        student_block.data['percentages'].append(percentage)
                        block.data['sessions'].append(sessions)
                    else:
                        percentage = None
                        trials_len = None
                        sessions = None

                    # info = '\t'.join([
                    #     student.name,
                    #     str(student.id),
                    #     block.legend,
                    #     str(block.id),
                    #     date.strftime('%d/%m/%Y'),
                    #     str(target_registrations),
                    #     str(percentage),
                    #     str(trials_len),
                    #     str(sessions)])
                    # # print(info)
                    # file.write(info + '\n')

ACOLE1 = ACOLE1_Container()
ACOLE2 = ACOLE2_Container()
ACOLE3 = ACOLE3_Container()
MODULE1 = MODULE1_Container()
MODULE2 = MODULE2_Container()
MODULE3 = MODULE3_Container()

for i, ACOLE in enumerate([ACOLE1, ACOLE2, ACOLE3]):
    if ACOLE.cache_exists():
        print(f'Loading ACOLE {i + 1} from cache')
        if i == 0:
            ACOLE1 = ACOLE.load_from_file()
        elif i == 1:
            ACOLE2 = ACOLE.load_from_file()
        elif i == 2:
            ACOLE3 = ACOLE.load_from_file()

    else:
        print(f'Populating ACOLE {i + 1} cache')
        if i == 0:
            populate_acole_data(ACOLE1, i)
        elif i == 1:
            populate_acole_data(ACOLE2, i)
        elif i == 2:
            populate_acole_data(ACOLE3, i)

for i, MODULE in enumerate([MODULE1, MODULE2, MODULE3]):
    if MODULE.cache_exists():
        print(f'Loading MODULE {i+1} ({MODULE.id}) from cache')
        if i == 0:
            MODULE1 = MODULE.load_from_file()
        elif i == 1:
            MODULE2 = MODULE.load_from_file()
        elif i == 2:
            MODULE3 = MODULE.load_from_file()
    else:
        print(f'Populating MODULE {i+1} ({MODULE.id}) cache')
        if i == 0:
            populate_module_data(MODULE1)
        elif i == 1:
            populate_module_data(MODULE2)
        elif i == 2:
            populate_module_data(MODULE3)
            ACOLE1.save_to_file()
            ACOLE2.save_to_file()
            ACOLE3.save_to_file()
            MODULE1.save_to_file()
            MODULE2.save_to_file()
            MODULE3.save_to_file()
            cache_students()
            print('Cache saved')