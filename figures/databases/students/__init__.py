import os
import csv
from datetime import datetime

from collections import Counter
from sqlalchemy import text
import pandas as pd

from .methods import age, similarity, show_merge_choice, show_update_name
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

class School:
    def __init__(self, school_data=None):
        self.update(school_data)

    def update(self, school_data):
        if school_data is None:
            self.id = None
            self.name = None
            self.city = None
            self.state = None
        else:
            self.id = school_data.ID
            self.name = school_data.NOME
            self.city = school_data.CIDADE
            self.state = school_data.UF

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
        self.modules = [None, None, None]
        self.frequency = None
        self.__true_indices = []
        self.days_per_week = None
        self.ids = []
        self.school = School()

        if student_data is None:
            self.id = None
            self.name = None
            self.age = None
            self.birthdate = None
            self.sex = None
            self.school_year = None
        else:
            self.id = student_data.ID
            self.name = student_data.FULLNAME
            self.age = age(student_data.BIRTHDATE)
            self.birthdate = student_data.BIRTHDATE
            self.sex = student_data.SEX
            if correct_school_year is None:
                self.school_year = int(student_data.SCHOOL_YEAR.strip())
            else:
                self.school_year = int(correct_school_year.strip())

        self.ids.append(self.id)
        self.forward_to(forwarding_trial_id)

    def summary(self):
        print(f'ID: {self.id}')
        print(f'Nome: {self.name}')
        print(f'Idade: {self.age}')
        print(f'Sexo: {self.sex}')
        print(f'Ano escolar: {self.school_year}')
        print(f'Data de nascimento: {self.birthdate}')
        print(f'Acoles Completas: {self.acoles_is_complete}')
        print(f'Acoles (n): {len(self.acoles)}')
        for i, module in enumerate(self.modules):
            if module is not None:
                print(f'Módulo{i+1}: {self.is_module_complete(module.id)}')
            else:
                print(f'Módulo{i+1}: {module}')
        print(f'Frequency: {self.frequency}')
        self.calculate_days_per_week()
        print(f'Dias por semana: {self.mean_days_per_week()}')

    def merge(self, student, prompt=True):
        self.ids.append(student.id)
        if prompt:
            if student.name != self.name:
                print(f'Name: {self.name} or {student.name}?')
                self.name = show_merge_choice(self.name, student.name)
                print(f'{self.name} selected.')

            if student.sex != self.sex:
                print(f'Sex: {self.sex} or {student.sex}?')
                self.sex = show_merge_choice(self.sex, student.sex)
                print(f'{self.sex} selected.')

            if student.school_year != self.school_year:
                print(f'School Year: {self.school_year} or {student.school_year}?')
                self.school_year = int(show_merge_choice(str(self.school_year), str(student.school_year)))
                print(f'{self.school_year} selected.')

            if student.age != self.age:
                print(f'Age: {self.age} or {student.age}?')
                self.age = int(show_merge_choice(str(self.age), str(student.age)))
                print(f'{self.age} selected.')

            if student.birthdate != self.birthdate:
                print(f'Birthdate: {self.birthdate} or {student.birthdate}?')
                time_format = "%Y-%m-%d %H:%M:%S"
                date1 = self.birthdate.strftime(time_format)
                date2 = student.birthdate.strftime(time_format)
                selected = show_merge_choice(date1, date2)
                self.birthdate = datetime.strptime(selected, time_format)
                print(f'{selected} selected.')

            if student.forwarding != self.forwarding:
                print(f'Forwarding: {self.forwarding} or {student.forwarding}?')
                self.forwarding = show_merge_choice(self.forwarding, student.forwarding)
                print(f'{self.forwarding} selected.')
        else:
            self.name = student.name
            self.sex = student.sex
            self.school_year = student.school_year
            self.age = student.age
            self.birthdate = student.birthdate
            self.forwarding = student.forwarding

    def assign_school(self, school_data):
        if hasattr(self, 'school'):
            self.school.update(school_data)
        else:
            self.school = School(school_data)

    def update_name(self):
        self.name = show_update_name(self.name)

        # don't need to prompt for modules, since they can be merged safely
        # self.has_m1 = self.has_m1 or student.has_m1
        # self.has_m2 = self.has_m2 or student.has_m2
        # self.has_m3 = self.has_m3 or student.has_m3
        # self.acoles.extend(student.acoles)
        # self.acoles_is_complete.extend(student.acoles_is_complete)
        # for i, (self_module, student_module) in enumerate(zip(self.modules, student.modules)):
        #     if self_module is None:
        #         self.modules[i] = student_module
        #     elif self_module is not None and student_module is not None:
        #         self_module.merge(student_module)

        # if self.frequency is None:
        #     self.frequency = student.frequency

        # elif self.frequency is not None and student.frequency is not None:
        #     self.frequency.extend(student.frequency)

        # self.days_per_week = None
        # self.calculate_days_per_week()

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

    def is_module_complete(self, module_id):
        if module_id == MODULO1_ID:
            return self.has_m1
        elif module_id == MODULO2_ID:
            return self.has_m2
        elif module_id == MODULO3_ID:
            return self.has_m3

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

    def has_two_acoles(self):
        return len(self.acoles) > 1

    def get_first_and_last_acoles(self):
        return 0, len(self.acoles) - 1

    def get_first_and_second_acoles(self):
        return 0, 1

    def get_first_acole(self):
        return 0

    def has_two_acoles_first_incomplete(self):
        return len(self.acoles) > 1 and not self.acoles_is_complete[0]

    def similarity(self, student):
        return similarity(self.name, student.name)

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
        # black_list = [9719,9670,9898,8076,8072,10064,10053,10076,10191]
        black_list = []
        for student_data in students:
            if 'DUPLICATA DESCONSIDERAR' in student_data.FULLNAME:
                continue

            if student_data.ID in black_list:
                continue

            if student_data.ID in correct_school_years.keys():
                self.append(Student(student_data, None, correct_school_years[student_data.ID]))
            else:
                self.append(Student(student_data, None, ))

        self.merge_students_ids()

    def merge_students_ids(self):
        P1 = [9953, 10053]
        P2 = [9736, 10191]
        P3 = [10062, 10064]
        P4 = [10076, 10144]
        P5 = [10118, 10375]
        ids_to_merge = [P1, P2, P3, P4, P5]
        for ids in ids_to_merge:
            for student1, student2 in students.pairwise(ids):
                student1.merge(student2)

        # get the second id from each pair
        ids_to_remove = [ids[1] for ids in ids_to_merge]
        students.remove_ids(ids_to_remove)

    def update_names(self):
        for student in self.__students:
            student.update_name()

    def items(self):
        for student in self.__students:
            yield student

    def append(self, student):
        self.__students.append(student)

    def _student_filter(self, filter_function):
        return [student for student in self.__students if filter_function(student)]

    def summary(self):
        print('\n\nSummary:'+ self.__class__.__name__)

        print(f'Total students: {len(self)}')
        print('\nSchools:')
        for school, count in self.schools(count=True).items():
            print(f'{school}: {count}')

        # print('\nCompleted Modules:')
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

    def schools(self, count=False):
        schools = [student.school.name for student in self.items()]
        if count:
            return dict(sorted(Counter(schools).items()))
        else:
            return schools

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

    def to_data_frame(self):
        return pd.DataFrame(
            [(student.id, student.sex, student.age, student.school_year, student.mean_days_per_week()) for student in students],
            columns=['ID', 'Sexo', 'Idade', 'Ano Escolar', 'Dias por semana'])

    def by_frequency(self, range):
        return Students_Container([
            student for student in self.items() if student.mean_days_per_week() in range])

    def by_school(self, school_name):
        return Students_Container([
            student for student in self.items() if student.school.name == school_name])

    def by_age(self, age):
        return Students_Container([
            student for student in self.items() if student.age == age])

    def by_sex(self, sex):
        return Students_Container([
            student for student in self.items() if student.sex == sex])

    def by_has_acole(self):
        return Students_Container([student for student in students if len(student.acoles) > 0])

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

    def from_id(self, id):
        for student in self.items():
            if student.id == id:
                return student

    def from_ids(self, ids):
        return [student for student in self.items() for id in ids if student.id == id]

    def remove_ids(self, ids):
        self.__students = [student for student in self.items() if student.id not in ids]

    def pairwise(self, pairwise_ids):
        students = self.from_ids(pairwise_ids)
        yield students[0], students[1]

    def frequencies(self):
        result = []
        for student in self.items():
            result.extend(student.frequency)
        return result

def cache_students():
    # students.merge_students_ids()
    students.save_to_file()

if Students_Container.cache_exists():
    print('Loading Students from cache')
    students = Students_Container.load_from_file()
    # students.update_names()
    # students.save_to_file()
else:
    print('Populating Students cache')
    students = Students_Container()
    correct_school_years = read_csv(os.path.join('figures', 'databases', 'students', 'students_with_correct_school_year.tsv'))
    with geic_db.connect() as connection:
        students_template = template_from_name('students_from_alphatech')
        students.populate(connection.execute(text(students_template)).fetchall(), correct_school_years)
        students.save_to_file()