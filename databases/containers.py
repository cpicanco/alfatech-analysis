# program
import os
import pickle
import re
from collections import Counter

from .methods import age

class Student:
    def __init__(self, student_data=None, forwarding_trial_id=None):
        forwarding_module = {
            32216 : 'Módulo 1',
            33048 : 'Módulo 2',
            33049 : 'Módulo 3'
        }

        if student_data == None:
            self.name = None
            self.id = None
            self.age = None
            self.birthdate = None
            self.sex = None
        else:
            self.name = student_data.FULLNAME
            self.id = student_data.ID
            self.age = age(student_data.BIRTHDATE)
            self.birthdate = student_data.BIRTHDATE
            self.sex = student_data.SEX

        if forwarding_trial_id is None:
            self.forwarding = None
        else:
            self.forwarding = forwarding_module[forwarding_trial_id]

class Block:
    def __init__(self, id, legend, code, min_trials):
        self.id = id
        self.legend = legend
        self.code = code
        self.min_trials = min_trials
        self.data = { 'students': [],
                      'trials': [],
                      'percentages': []}
        self.age_group = None
        self.forwarding = None
        self.sex = None

class Container:
    def __init__(self, **kwargs):
        self.blocks = []
        for key, value in kwargs.items():
            setattr(self, key, value)
            if key != 'data':
                self.blocks.append(value)
        self.id = None
        self.age_group = None
        self.forwarding = None
        self.sex = None

    @classmethod
    def filename(cls):
        pass

    def save_to_file(self):
        os.makedirs('cache', exist_ok=True)

        with open(self.filename(), 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls):
        with open(cls.filename(), 'rb') as file:
            loaded_instance = pickle.load(file)
        return loaded_instance

    @classmethod
    def cache_exists(cls):
        return os.path.exists(cls.filename())

    @classmethod
    def student_fullname(cls, student_data):
        pattern = re.compile(r'\([^)]*\)')
        return re.sub(pattern, '', student_data.FULLNAME).strip()

class ACOLE_Container(Container):
    def __init__(self, **kwargs):
        kwargs = {'LEITURA' : Block(3843, 'Leitura', 'CD', 8),
                  'DITADO_COMPOSICAO' : Block(3839, 'Ditado por composição', 'AE', 10),
                  'DITADO_MANUSCRITO' : Block(3847, 'Ditado manuscrito', 'AF', 4),
                  'LEITURA_DIFICULDADES' : Block(3240, 'Leitura*', 'CD', 20),
                  'DITADO_COMPOSICAO_DIFICULDADES' : Block(3241, 'Ditado por composição*', 'AE', 20),
                  'DITADO_MANUSCRITO_DIFICULDADES' : Block(3242, 'Ditado manuscrito*', 'AF', 20)}

        super(ACOLE_Container, self).__init__(**kwargs)
        self.id = 372
        self.age_group = None
        self.forwarding = None
        self.sex = None

    def _student_filter(self, filter_function):
        filtered_ACOLE = ACOLE_Container()
        for block, block_filtered in zip(self.blocks, filtered_ACOLE.blocks):
            for student, trials, percentage in zip(block.data['students'], block.data['trials'], block.data['percentages']):
                if student is not None and filter_function(student):
                    block_filtered.data['students'].append(student)
                    block_filtered.data['trials'].append(trials)
                    block_filtered.data['percentages'].append(percentage)
                else:
                    block_filtered.data['students'].append(None)
                    block_filtered.data['trials'].append(None)
                    block_filtered.data['percentages'].append(None)

        return filtered_ACOLE

    def students(self, filter_function=None):
        if filter_function is None:
            filter_function = lambda student: True

        for block in self.blocks:
            for student in block.data['students']:
                if student is not None and filter_function(student):
                    yield student

    def summary(self):
        print('Summary:')
        print('\nModules:')
        for module, count in self.modules(count=True).items():
            print(f'{module}: {count} data points')

        print('\nAges:')
        for age, count in self.ages(count=True).items():
            print(f'{age}: {count} data points')

        print('\nSexes:')
        for sex, count in self.sexes(count=True).items():
            print(f'{sex}: {count} data points')

    def modules(self, count=False):
        modules = []
        for student in self.students():
            modules.append(student.forwarding if student.forwarding is not None else 'None')
        if count:
            return dict(sorted(Counter(modules).items()))
        else:
            return modules

    def ages(self, count=False):
        ages = []
        for student in self.students():
            ages.append(student.age)
        if count:
            return dict(sorted(Counter(ages).items()))
        else:
            return ages

    def sexes(self, count=False):
        sexes = []
        for student in self.students():
            sexes.append(student.sex)
        if count:
            return dict(sorted(Counter(sexes).items()))
        else:
            return sexes

    def by_sex(self, sex):
        allowed_sexes = ['M', 'F']
        filter_function = {
            'M': lambda student: student.sex == 'M',
            'F': lambda student: student.sex == 'F'}

        if sex in allowed_sexes:
            filtered = self._student_filter(filter_function[sex])
            filtered.sex = sex
            for block in filtered.blocks:
                block.sex = sex
                block.age_group = self.age_group
                block.forwarding = self.forwarding
            return filtered
        else:
            raise ValueError("Invalid sex value. Accepted values are 'M' or 'F'.")

    def by_age(self, ages_array):
        filter_function = lambda student: student.age in ages_array
        filtered = self._student_filter(filter_function)
        filtered.age_group = ages_array
        for block in filtered.blocks:
            block.age_group = ages_array
            block.forwarding = self.forwarding
            block.sex = self.sex
        return filtered

    def by_forwarding(self, forwarding_id):
        filter_function = lambda student: student.forwarding == forwarding_id
        filtered = self._student_filter(filter_function)
        filtered.module = forwarding_id
        for block in filtered.blocks:
            block.forwarding = forwarding_id
            block.sex = self.sex
            block.age_group = self.age_group
        return filtered

    @classmethod
    def filename(cls):
        return os.path.join('cache', f'{cls.__name__}.pkl')