import os
import datetime

# database
from sqlalchemy import text, bindparam

from ..constants import ACOLE_BLOCK_IDS
from ..constants import MODULO1_STEP_IDS, MODULO2_STEP_IDS, MODULO3_STEP_IDS
from ..constants import MODULO1_ID, MODULO2_ID, MODULO3_ID

def template_from_name(template_name):
    sql_query_template_file = os.path.join(
        os.path.dirname(__file__), template_name +'.sql')

    # Load the SQL query from the file
    with open(sql_query_template_file, 'r', encoding='utf-8') as file:
        return file.read()

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
            # print('student_ids:' + str(student_ids),
            #     'registration_id:' + str(registration_id),
            #     'program_id:' + str(program_id),
            #     'block_id:' + str(block_id))
            print(percentage, trials_len)
            print(trials)
            raise Exception('Percentage greater than 100%')
    else:
        percentage = None
        trials_len = None
    return (trials, trials_len, percentage, date)

def query(connection, template, parameters):
    sql_text = text(template)
    for key, _ in parameters.items():
        if key == 'STUDENT_IDS' or key == 'STEP_IDS' or key == 'BLOCK_IDS':
            sql_text = sql_text.bindparams(bindparam(key, expanding=True))
    return connection.execute(sql_text, parameters).fetchall()

def get_frequency_from_student(connection, student_ids):
    template = template_from_name('frequency_from_student')
    parameters = {'STUDENT_IDS': student_ids}
    frequency = query(connection, template, parameters)
    if not frequency:
        return []
    return [f[0] for f in frequency]

def get_step_trials(connection, registration_id, program_id, step_id, student_ids):
    template = template_from_name('step_trials_from_student')
    parameters = {'REGISTRATION_ID': registration_id,
                  'PROGRAM_ID': program_id,
                  'STEP_ID': step_id,
                  'STUDENT_IDS': student_ids}
    trials_data = query(connection, template, parameters)
    return get_trials(trials_data)

def get_block_trials(connection, registration_id, program_id, block_id, student_ids):
    template = template_from_name('block_trials_from_student')
    parameters = {'REGISTRATION_ID': registration_id,
                    'PROGRAM_ID': program_id,
                    'BLOCK_ID': block_id,
                    'STUDENT_IDS': student_ids}
    trials_data = query(connection, template, parameters)
    return get_trials(trials_data)

def get_forwarding_trial(connection, acole_registration_id, acole_id, student_ids):
    template = template_from_name('module_forward_trials_from_student')
    parameters = {'PROGRAM_ID': acole_id,
                    'STUDENT_IDS': student_ids,
                    'REGISTRATION_ID': acole_registration_id}

    module_forward_trials = query(connection, template, parameters)
    return module_forward_trials[0][0] if module_forward_trials != [] else None

def get_registration(connection, program_id, student_ids):
    template = template_from_name('oldest_program_registration_from_student')
    parameters = {'PROGRAM_ID': program_id,
                  'STUDENT_IDS': student_ids}
    registration = query(connection, template, parameters)
    return registration

def get_step_sessions(connection, registration_id, program_id, step_id, student_ids):
    template = template_from_name('session_count_from_program_step')
    parameters = {
        'REGISTRATION_ID': registration_id,
        'PROGRAM_ID': program_id,
        'STEP_ID': step_id,
        'STUDENT_IDS': student_ids}
    sessions = query(connection, template, parameters)
    return sessions[0][0] if sessions != [] else None

def is_complete(result):
    if result == []:
        return False
    return False if result[0].IS_COMPLETE == 0 else True

def complete_module(connection, registration_id, student_ids, module_id):
    template = template_from_name('complete_module_from_registration')
    parameters = {
        'REGISTRATION_ID': registration_id,
        'PROGRAM_ID': module_id,
        'STUDENT_IDS': student_ids,
        'STEP_IDS': None,
        'UNIQUE_COUNT': None}
    if MODULO1_ID == module_id:
        parameters['UNIQUE_COUNT'] = len(MODULO1_STEP_IDS)
        parameters['STEP_IDS'] = MODULO1_STEP_IDS
    elif MODULO2_ID == module_id:
        parameters['UNIQUE_COUNT'] = len(MODULO2_STEP_IDS)
        parameters['STEP_IDS'] = MODULO2_STEP_IDS
    elif MODULO3_ID == module_id:
        parameters['UNIQUE_COUNT'] = len(MODULO3_STEP_IDS)
        parameters['STEP_IDS'] = MODULO3_STEP_IDS

    result = query(connection, template, parameters)
    return is_complete(result)

def complete_module_from_student(connection, student_ids, module_id):
    template = template_from_name('complete_module_from_student')
    parameters = {
        'PROGRAM_ID': module_id,
        'STUDENT_IDS': student_ids,
        'STEP_IDS': None,
        'UNIQUE_COUNT': None}
    if MODULO1_ID == module_id:
        parameters['UNIQUE_COUNT'] = len(MODULO1_STEP_IDS)
        parameters['STEP_IDS'] = MODULO1_STEP_IDS
    elif MODULO2_ID == module_id:
        parameters['UNIQUE_COUNT'] = len(MODULO2_STEP_IDS)
        parameters['STEP_IDS'] = MODULO2_STEP_IDS
    elif MODULO3_ID == module_id:
        parameters['UNIQUE_COUNT'] = len(MODULO3_STEP_IDS)
        parameters['STEP_IDS'] = MODULO3_STEP_IDS

    result = query(connection, template, parameters)
    return is_complete(result)

def complete_acole(connection, registration_id, student_ids, acole_id):
    template = template_from_name('complete_acole_from_registration')
    parameters = {
        'REGISTRATION_ID': registration_id,
        'PROGRAM_ID': acole_id,
        'STUDENT_IDS': student_ids,
        'BLOCK_IDS': ACOLE_BLOCK_IDS,
        'UNIQUE_COUNT': len(ACOLE_BLOCK_IDS)}
    result = query(connection, template, parameters)
    return is_complete(result)

def school_from_student(connection, student_ids):
    template = template_from_name('school_from_student')
    parameters = {'STUDENT_IDS': student_ids}
    school = query(connection, template, parameters)
    return school[0] if school != [] else None