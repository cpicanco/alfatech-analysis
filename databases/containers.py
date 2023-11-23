# program
import os
import pickle
import re
from collections import Counter

from .methods import age
# from methods import age

class Student:
    def __init__(self, **kwargs):
        self.name = None
        self.id = None
        self.age = None
        self.birthdate = None

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
        self.module = None
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
        self.module = None
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
        self.module = None
        self.sex = None

    # return a copy of self.data with male students only
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
                    p = Student()
                    p.id = student.ID
                    p.name = self.student_fullname(student)
                    p.birthdate = student.BIRTHDATE
                    p.age = age(student.BIRTHDATE)
                    p.sex = student.SEX
                    yield p

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
            'M': lambda student: student.SEX == 'M',
            'F': lambda student: student.SEX == 'F'}

        if sex in allowed_sexes:
            filtered = self._student_filter(filter_function[sex])
            filtered.sex = sex
            for block in filtered.blocks:
                block.sex = sex
                block.age_group = self.age_group
                block.module = self.module
            return filtered
        else:
            raise ValueError("Invalid sex value. Accepted values are 'M' or 'F'.")

    def by_age(self, ages_array):
        filter_function = lambda student: age(student.BIRTHDATE) in ages_array
        filtered = self._student_filter(filter_function)
        filtered.age_group = ages_array
        for block in filtered.blocks:
            block.age_group = ages_array
            block.module = self.module
            block.sex = self.sex
        return filtered

    def by_forward_module_id(self, module):
        filter_function = lambda student: student.MODULE == module
        filtered = self._student_filter(filter_function)
        filtered.module = module
        for block in filtered.blocks:
            block.module = module
            block.sex = self.sex
            block.age_group = self.age_group
        return filtered

    @classmethod
    def filename(cls):
        return os.path.join('cache', f'{cls.__name__}.pkl')

if __name__ == "__main__":
    ACOLE = ACOLE_Container()
    for block in ACOLE.blocks:
        print(block.id, block.data)