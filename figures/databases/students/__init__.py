import os
import csv
import math

from collections import Counter
from sqlalchemy import text
import pandas as pd
import numpy as np

from ..ranges import RangeContainer
from ..methods import age
from ..queries import template_from_name
from ..engine import geic_db
from ..base_container import Base_Container
from ..constants import MODULO1_ID, MODULO2_ID, MODULO3_ID

def read_csv(file_path):
    data_dict = {}
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            data_dict[row['ID']] = row['ANO']
    return data_dict

class Student:
    def __init__(self, student_data=None, forwarding_trial_id=None, correct_school_year=None):
        self.forwarding_modules = {
            32216 : 'Módulo 1',
            33048 : 'Módulo 2',
            33049 : 'Módulo 3',
            None : None
        }
        self.has_m1 = None
        self.has_m2 = None
        self.has_m3 = None
        self.acoles_is_complete = []
        self.acoles = []
        self.modules = []
        self.frequency = None
        self.__true_indices = []
        self.days_per_week = None

        if student_data is None:
            self.name = None
            self.id = None
            self.age = None
            self.birthdate = None
            self.sex = None
            self.school_year = None
        else:
            self.name = student_data.FULLNAME
            self.id = student_data.ID
            self.age = age(student_data.BIRTHDATE)
            self.birthdate = student_data.BIRTHDATE
            self.sex = student_data.SEX
            if correct_school_year is None:
                self.school_year = int(student_data.SCHOOL_YEAR.strip())
            else:
                self.school_year = int(correct_school_year.strip())

        self.forward_to(forwarding_trial_id)

    def forward_to(self, module_id):
        self.forwarding = self.forwarding_modules[module_id]

    def set_completion(self, module_id, completion):
        if completion is None:
            raise ValueError('Completion cannot be None')
        if module_id == MODULO1_ID:
            self.has_m1 = completion
        elif module_id == MODULO2_ID:
            self.has_m2 = completion
        elif module_id == MODULO3_ID:
            self.has_m3 = completion

    def calculate_days_per_week(self):
        if self.days_per_week is None:
            if self.frequency is not None:
                df = pd.DataFrame({'date': self.frequency})
                df['date_string'] = df['date'].dt.strftime('%Y-%m-%d')
                df = df.drop_duplicates(subset=['date_string'])

                # Extract year and week from the original DataFrame
                df['year'] = df['date'].dt.year
                df['week'] = df['date'].dt.isocalendar().week

                # Group by year and week, calculate count
                result = df.groupby(['week']).size().reset_index(name='count')

                # Find the minimum and maximum dates
                min_week = result['week'].min()
                max_week = result['week'].max()

                # Generate a range of weeks based on the number of weeks
                week_range = pd.DataFrame(
                    [(week,) for week in range(min_week, max_week + 1)],
                    columns=['week']
                )

                # Merge the result with the dynamically generated weeks and fill NaN with zero
                result = pd.merge(week_range, result, on=['week'], how='left').fillna(0)
                self.days_per_week = result

    def mean_days_per_week(self):
        return self.days_per_week['count'].sum()/len(self.days_per_week)

    def has_two_complete_acoles(self):
        self.__true_indices = [i for i, value in enumerate(self.acoles_is_complete) if value]
        return len(self.__true_indices) > 1

    def get_complete_acoles(self):
        return self.__true_indices[0], self.__true_indices[1]

class Students_Container(Base_Container):
    def __init__(self, students = [], **kwargs):
        super(Students_Container, self).__init__(**kwargs)
        self.__students = students

    def __len__(self):
        return len(self.__students)

    def __getitem__(self, index):
        return self.__students[index]

    @classmethod
    def filename(cls):
        return os.path.join('cache', f'{cls.__name__}.pkl')

    def populate(self, students, correct_school_years):
        for student_data in students:
            if 'DUPLICATA DESCONSIDERAR' in student_data.FULLNAME:
                continue

            if student_data.ID in correct_school_years.keys():
                self.append(Student(student_data, None, correct_school_years[student_data.ID]))
            else:
                self.append(Student(student_data, None, ))

    def items(self):
        for student in self.__students:
            yield student

    def append(self, student):
        self.__students.append(student)

    def _student_filter(self, filter_function):
        return [student for student in self.__students if filter_function(student)]

    def summary(self):
        print('\n\nSummary:'+ self.__class__.__name__)
        print('\nCompleted Modules:')
        print(f'Total de alunos: {len(self)}')
        # print(f'Com Módulo 1 completo: {len(self._student_filter(lambda student: student.has_m1 == True))}')
        # print(f'Com Módulo 1 incompleto: {len(self._student_filter(lambda student: student.has_m1 == False))}')
        # print(f'Com Módulo 1 desconhecido: {len(self._student_filter(lambda student: student.has_m1 is None))}')
        # print(f'Com Módulo 2 completo: {len(self._student_filter(lambda student: student.has_m2 == True))}')
        # print(f'Com Módulo 2 incompleto: {len(self._student_filter(lambda student: student.has_m2 == False))}')
        # print(f'Com Módulo 2 desconhecido: {len(self._student_filter(lambda student: student.has_m2 is None))}')
        # print(f'Com Módulo 3 completo: {len(self._student_filter(lambda student: student.has_m3 == True))}')
        # print(f'Com Módulo 3 incompleto: {len(self._student_filter(lambda student: student.has_m3 == False))}')
        # print(f'Com Módulo 3 desconhecido: {len(self._student_filter(lambda student: student.has_m3 is None))}')
        # print(f'Com Módulo 1 e 2 completo: {len(self._student_filter(lambda student: student.has_m1 and student.has_m2))}')
        # print(f'Com Módulo 1 e 2 incompleto: {len(self._student_filter(lambda student: student.has_m1 == False and student.has_m2 == False))}')
        # print(f'Com Módulo 1 e 2 desconhecido: {len(self._student_filter(lambda student: student.has_m1 is None and student.has_m2 is None))}')
        # print(f'Com Módulo 1 e 3 completo: {len(self._student_filter(lambda student: student.has_m1 and student.has_m3))}')
        # print(f'Com Módulo 1 e 3 incompleto: {len(self._student_filter(lambda student: student.has_m1 == False and student.has_m3 == False))}')
        # print(f'Com Módulo 1 e 3 desconhecido: {len(self._student_filter(lambda student: student.has_m1 is None and student.has_m3 is None))}')
        # print(f'Com Módulo 2 e 3 completo: {len(self._student_filter(lambda student: student.has_m2 and student.has_m3))}')
        # print(f'Com Módulo 2 e 3 incompleto: {len(self._student_filter(lambda student: student.has_m2 == False and student.has_m3 == False))}')
        # print(f'Com Módulo 2 e 3 desconhecido: {len(self._student_filter(lambda student: student.has_m2 is None and student.has_m3 is None))}')
        # print(f'Com Módulo 1, 2, e 3 completo: {len(self._student_filter(lambda student: student.has_m1 and student.has_m2 and student.has_m3))}')
        # print(f'Com Módulo 1, 2, e 3 incompleto: {len(self._student_filter(lambda student: student.has_m1 == False and student.has_m2 == False and student.has_m3 == False))}')
        # print(f'Com Módulo 1, 2, e 3 desconhecido: {len(self._student_filter(lambda student: student.has_m1 is None and student.has_m2 is None and student.has_m3 is None))}')

        # print('\nModule Forwarding:')
        # for module, count in self.forwardings(count=True).items():
        #     print(f'{module}: {count}')

        # print('\nAges:')
        # for age, count in self.ages(count=True).items():
        #     print(f'{age}: {count}')

        # print('\nSexes:')
        # for sex, count in self.sexes(count=True).items():
        #     print(f'{sex}: {count}')

        # print('\nSchool Years:')
        # for school_year, count in self.school_years(count=True).items():
        #     print(f'{school_year}: {count}')

    def forwardings(self, count=False):
        forwardings = [student.forwarding if student.forwarding is not None else 'None' for student in self.items()]
        if count:
            return dict(sorted(Counter(forwardings).items()))
        else:
            return forwardings

    def ages(self, count=False):
        ages = [student.age for student in self.items()]
        if count:
            return dict(sorted(Counter(ages).items()))
        else:
            return ages

    def sexes(self, count=False):
        sexes = [student.sex for student in self.items()]
        if count:
            return dict(sorted(Counter(sexes).items()))
        else:
            return sexes

    def school_years(self, count=False):
        school_years = [student.school_year for student in self.items()]
        if count:
            return dict(sorted(Counter(school_years).items()))
        else:
            return school_years

    def days_per_week(self):
        return pd.DataFrame(
                [(student.mean_days_per_week(),) for student in students],
                columns=['mean_days_per_week'])

    def by_frequency(self, range):
        return Students_Container([
            student for student in self.items() if student.mean_days_per_week() in range])

    def summary_by_frequency(self, range=None, ranges=None):
        # print('\nDays per week:')
        df = self.days_per_week()

        if ranges is not None:
            # ranges = RangeContainer([v[0] for v in np.linspace(df.min(), df.max(), 7)])
            print('\nStudents by frequency:')
            for r in ranges:
                print(f'{r.as_list()}: {len(self.by_frequency(r))}')

        if range is not None:
            # print('\nStudents by frequency:')
            print(f'{range.as_list()}: {len(self.by_frequency(range))}')


if Students_Container.cache_exists():
    print('Loading Students from cache')
    students = Students_Container.load_from_file()
else:
    print('Populating Students cache')
    students = Students_Container()
    correct_school_years = read_csv(os.path.join('databases', 'students', 'students_with_correct_school_year.tsv'))
    with geic_db.connect() as connection:
        students_template = template_from_name('students_from_alphatech')
        students.populate(connection.execute(text(students_template)).fetchall(), correct_school_years)

def cache_students():
    students.save_to_file()