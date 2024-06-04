"""
# you should use python env to install the following packages to avoid dependency conflicts
py -m pip install mysql-connector-python
py -m pip install SQLAlchemy
"""
from .engine import geic_db
from .students import students

from .queries import get_registration
from .queries import complete_acole, get_forwarding_trial, get_block_trials, get_step_trials
from .queries import get_step_sessions, complete_module, complete_module_from_student

from .constants import MODULO1_ID, MODULO2_ID, MODULO3_ID
from .containers import ACOLE1_Container,  ACOLE2_Container,  ACOLE3_Container
from .containers import MODULE1_Container, MODULE2_Container, MODULE3_Container

def populate_acole_data(ACOLE, registration_index=0):
    # file = open(ACOLE.filename()+'.tsv', 'w', encoding='utf-8')
    # file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS']) + '\n')
    # file.write('\t'.join(['NOME', 'ID', 'MATRICULA.ID.COMPLETAS', 'MATRICULA.ID.INCOMPLETAS', 'ENCAMINHAMENTO'])+'\n')
    with geic_db.connect() as connection:
        for student in students:
            # if student.frequency is None:
            #     student.frequency = get_frequency_from_student(connection, student.ids)
            #     student.calculate_days_per_week()

            acole_registration = get_registration(connection, ACOLE.id, student.ids)

            # complete_registrations = [r[0] for r in acole_registration if complete_acole(connection, r[0], student.id, ACOLE.id)]
            # incomplete_registrations = [r[0] for r in acole_registration if not complete_acole(connection, r[0], student.id, ACOLE.id)]
            # forwardings = [str(r[0])+'->'+str(forwarding_modules[get_forwarding_trial(connection, r[0], ACOLE.id, student.id)]) for r in acole_registration]
            # file.write('\t'.join([student.name, str(student.id), str(complete_registrations), str(incomplete_registrations), str(forwardings)])+'\n')
            if registration_index >= len(acole_registration):
                continue

            acole_registration_id = acole_registration[registration_index][0]

            student.forward_to(get_forwarding_trial(connection, acole_registration_id, ACOLE.id, student.ids))
            student.acoles.append(ACOLE.create())
            student.acoles_is_complete.append(complete_acole(connection, acole_registration_id, student.ids, ACOLE.id))
            for block, student_block in zip(ACOLE.blocks, student.acoles[-1].blocks):
                (trials, trials_len, percentage, date) = get_block_trials(connection, acole_registration_id, ACOLE.id, block.id, student.ids)
                trials_len = len(trials)
                if trials_len > 0:
                    block.date.append(date)
                    block.data['students'].append(student)
                    block.data['trials'].append(trials)
                    block.data['percentages'].append(percentage)
                    block.data['sessions'].append(1)
                    student_block.date.append(date)
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
    # file.close()

def populate_module_data(MODULE):
    # file = open(MODULE.filename()+'.tsv', 'w', encoding='utf-8')
    # file.write('\t'.join(['NOME', 'ID', 'BLOCO_NOME', 'BLOCO_ID', 'BLOCO_DATA', 'MATRICULA.ID', 'PORCENTAGEM_ACERTOS', 'TOTAL_TENTATIVAS', 'TOTAL_SESSOES']) + '\n')
    with geic_db.connect() as connection:
        for student in students:
            module1_registrations = get_registration(connection, MODULE.id, student.ids)
            if module1_registrations == []:
                continue
            print(student.name)

            if len(module1_registrations) > 0:
                complete_registrations = [r[0] for r in module1_registrations if complete_module(connection, r[0], student.ids, MODULE.id)]
                incomplete_registrations = [r[0] for r in module1_registrations if not complete_module(connection, r[0], student.ids, MODULE.id)]
                if len(complete_registrations) > 0:
                    student.set_completion(MODULE.id, True)
                    target_registrations = [complete_registrations[0]]
                else:
                    student.set_completion(MODULE.id, complete_module_from_student(connection, student.ids, MODULE.id))
                    target_registrations = [r for r in incomplete_registrations]

            if MODULE.id == MODULO1_ID:
                index = 0
                student.modules[index] = MODULE1_Container()
            elif MODULE.id == MODULO2_ID:
                index = 1
                student.modules[index] = MODULE2_Container()
            elif MODULE.id == MODULO3_ID:
                index = 2
                student.modules[index] = MODULE3_Container()

            for block, student_block in zip(MODULE.blocks, student.modules[index].blocks):
                dates = []
                if len(target_registrations) == 1:
                    rid = target_registrations[0]
                    sessions = get_step_sessions(connection, rid, MODULE.id, block.id, student.ids)

                    if block.min_trials < 0:
                        (trials, trials_len, percentage, date) = get_step_trials(connection, rid, MODULE.id, block.id, student.ids)
                    else:
                        (trials, trials_len, percentage, date) = get_block_trials(connection, rid, MODULE.id, block.id, student.ids)
                    dates.append(date)
                else:
                    trials = []
                    sessions = 0
                    for rid in target_registrations:
                        step_sessions = get_step_sessions(connection, rid, MODULE.id, block.id, student.ids)
                        if step_sessions is not None:
                            sessions += step_sessions

                        if block.min_trials < 0:
                            (t, _, percentage, date) = get_step_trials(connection, rid, MODULE.id, block.id, student.ids)
                        else:
                            (t, _, percentage, date) = get_block_trials(connection, rid, MODULE.id, block.id, student.ids)
                        trials += t
                        dates.append(date)

                trials_len = len(trials)
                if trials_len > 0:
                    block.date.extend(dates)
                    block.data['students'].append(student)
                    block.data['trials'].append(trials)
                    block.data['percentages'].append(percentage)
                    block.data['sessions'].append(sessions)
                    student_block.date.extend(dates)
                    student_block.data['students'].append(student)
                    student_block.data['trials'].append(trials)
                    student_block.data['percentages'].append(percentage)
                    student_block.data['sessions'].append(sessions)
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
    # file.close()

ACOLE1 = ACOLE1_Container()
ACOLE2 = ACOLE2_Container()
ACOLE3 = ACOLE3_Container()
MODULE1 = MODULE1_Container()
MODULE2 = MODULE2_Container()
MODULE3 = MODULE3_Container()

if students.cache_exists():
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
                students.save_to_file()
                print('Cache saved')