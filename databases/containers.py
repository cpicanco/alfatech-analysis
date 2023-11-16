# program
import os
import pickle
import re
# import age from methods

class Container:
    def __init__(self, **kwargs):
        self.blocks = []
        for key, value in kwargs.items():
            setattr(self, key, value)
            if key != 'data':
                self.blocks.append(value)

        if 'data' in kwargs:
            self.data = kwargs['data']
        else:
            self.data = self._base_data()

    def _base_data(self):
        data = {}
        for block in self.blocks:
            data[block] = {
                'legend': '',
                'students': [],
                'trials': [],
                'percentages': []
            }
        return data

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
        kwargs = {'LEITURA' : 3843,
                'DITADO_COMPOSICAO' : 3839,
                'DITADO_MANUSCRITO' : 3847,
                'LEITURA_DIFICULDADES' : 3240,
                'DITADO_COMPOSICAO_DIFICULDADES' : 3241,
                'DITADO_MANUSCRITO_DIFICULDADES' : 3242}
        super(ACOLE_Container, self).__init__(**kwargs)
        self.ID = 372
        self.data[self.LEITURA]['legend'] = 'Leitura'
        self.data[self.DITADO_COMPOSICAO]['legend'] = 'Ditado por composição'
        self.data[self.DITADO_MANUSCRITO]['legend'] = 'Ditado manuscrito'
        self.data[self.LEITURA_DIFICULDADES]['legend'] = 'Leitura*'
        self.data[self.DITADO_COMPOSICAO_DIFICULDADES]['legend'] = 'Ditado por composição*'
        self.data[self.DITADO_MANUSCRITO_DIFICULDADES]['legend'] = 'Ditado manuscrito*'

    # return a copy of self.data with male students only
    def _student_filter(self, filter_function):
        data = self._base_data()
        for block in self.blocks:
            for student, trials, percentage in zip(self.data[block]['students'], self.data[block]['trials'], self.data[block]['porcentages']):
                if filter_function(student):
                    data[block]['students'].append(student)
                    data[block]['trials'].append(trials)
                    data[block]['percentages'].append(percentage)
                else:
                    data[block]['students'].append(None)
                    data[block]['trials'].append(None)
                    data[block]['percentages'].append(None)

        return ACOLE_Container(data=data)

    def by_sex(self, sex):
        filter_function = {
            'M': lambda student: student.SEX == 'M',
            'F': lambda student: student.SEX == 'F'}

        if sex in filter.keys():
            return self._student_filter(filter_function[sex])
        else:
            raise ValueError("Invalid sex value. Accepted values are 'M' or 'F'.")

    # def by_age(student, ages_array):
    #     filter_function = lambda student: age(student.BIRTHDATE) in ages_array
    #     return self._student_filter(filter_function)

    def by_forward_module_id(student, module):
        filter_function = lambda student: student.MODULE == module
        return self._student_filter(filter_function)

    @classmethod
    def filename(cls):
        return os.path.join('cache', f'{cls.__name__}.pkl')