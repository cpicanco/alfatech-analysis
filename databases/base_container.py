import os
import pickle
import re
from abc import ABC, abstractmethod

class Base_Container(ABC):
    def __init__(self, **kwargs):
        pass

    @classmethod
    def filename(cls):
        return f'cache/{cls.__name__}.pkl'

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

    @abstractmethod
    def _student_filter(self, filter_function):
        pass