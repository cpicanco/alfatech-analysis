# program
import os
import pickle
import re

class Container:
    def __init__(self, **kwargs):
        self.blocks = []
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.blocks.append(value)
        self.data = {}
        for block in self.blocks:
            self.data[block] = {
                'legend': '',
                'students': [],
                'trials': [],
                'porcentages': []
            }

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

    @classmethod
    def filename(cls):
        return os.path.join('cache', f'{cls.__name__}.pkl')