from collections import Counter

from .students import Students_Container
from .ranges import RangeContainer
from .base_container import Base_Container
from .constants import MODULO1_ID, MODULO2_ID, MODULO3_ID

class Block:
    def __init__(self, _id, legend, code, min_trials):
        self.id = _id
        self.legend = legend
        self.base_legend = legend
        self.code = code
        self.min_trials = min_trials
        self.data = { 'students': [],
                      'trials': [],
                      'percentages': [],
                      'sessions': []}
        self.age_group = None
        self.forwarding = None
        self.sex = None
        self.completed = {'m1': None, 'm2': None, 'm3': None}
        self.frequency_range = None
        self.school = None
        self.school_year = None
        self.date = []

    def delta(self, block):
        # result = self.clone()
        self.data['deltas'] = []
        for percentages2, percentages1 in zip(self.data['percentages'], block.data['percentages']):
            if percentages2 is not None:
                if percentages1 is not None:
                    self.data['deltas'].append(percentages2 - percentages1)
                else:
                    self.data['deltas'].append(percentages2 - 0)
            else:
                self.data['deltas'].append(None)
        return self

    def clone(self):
        clone = Block(self.id, self.legend, self.code, self.min_trials)
        clone.age_group = self.age_group
        clone.forwarding = self.forwarding
        clone.sex = self.sex
        clone.completed = self.completed
        clone.frequency_range = self.frequency_range
        clone.data = self.data.copy()
        return clone

class Container(Base_Container):
    def __init__(self, **kwargs):
        self.steps = []
        self.blocks = []
        self.id = None
        self.age_group = None
        self.forwarding = None
        self.sex = None
        self.completed = {'m1': None, 'm2': None, 'm3': None}
        self.frequency_range = None
        self.school = None
        self.school_year = None

    def _filter(self, filter_function, filtered):
        for block, block_filtered in zip(self.blocks, filtered.blocks):
            block_filtered.completed = block.completed
            block_filtered.forwarding = block.forwarding
            block_filtered.sex = block.sex
            block_filtered.age_group = block.age_group
            block_filtered.school = block.school
            block_filtered.school_year = block.school_year
            block_filtered.frequency_range = block.frequency_range
            for student, trials, percentage, sessions in zip(block.data['students'], block.data['trials'], block.data['percentages'], block.data['sessions']):
                if student is not None and filter_function(student):
                    block_filtered.data['students'].append(student)
                    block_filtered.data['trials'].append(trials)
                    block_filtered.data['percentages'].append(percentage)
                    block_filtered.data['sessions'].append(sessions)
                else:
                    block_filtered.data['students'].append(None)
                    block_filtered.data['trials'].append(None)
                    block_filtered.data['percentages'].append(None)
                    block_filtered.data['sessions'].append(None)
        return filtered

    def clone(self):
        clone = self.create()
        clone.steps = self.steps
        clone.blocks = self.blocks
        clone.id = self.id
        clone.age_group = self.age_group
        clone.forwarding = self.forwarding
        clone.sex = self.sex
        clone.completed = self.completed.copy()
        clone.frequency_range = self.frequency_range
        for block, block_clone in zip(self.blocks, clone.blocks):
            for key, data in block.data.items():
                block_clone.data[key] = data.copy()

    def students(self, filter_function=None):
        if filter_function is None:
            filter_function = lambda student: True

        for block in self.blocks:
            for student in block.data['students']:
                if student is not None and filter_function(student):
                    yield student

    def summary(self):
        # print('\n\nSummary:'+ self.__class__.__name__)

        # print('\nStudents: ')
        # for block in self.blocks:
        #     students = Students_Container(students=[s for s in block.data["students"] if s is not None])
        #     print(f'{block.legend}: {len(students)}')
        #     students.summary()

        # print('\nStudents data points: ')
        # students = Students_Container(students=[s for s in self.blocks[0].data["students"] if s is not None])
        # students.summary_by_frequency(self.frequency_range)
        # for block in self.blocks:
        #     print(f'{block.legend}: {len([s for s in block.data["students"] if s is not None])}')

        # print('\nCompleted Modules:')
        # for completed, count in self.completions(count=True).items():
        #     print(f'{completed}: {count} data points')

        # print('\nForwarding Modules:')
        # for module, count in self.modules(count=True).items():
        #     print(f'{module}: {count} data points')

        print('\nAges:')
        for age, count in self.ages(count=True).items():
            print(f'{age}: {count} data points')

        print('\nSexes:')
        for sex, count in self.sexes(count=True).items():
            print(f'{sex}: {count} data points')

        print('\nSchool Years:')
        for school_year, count in self.school_years(count=True).items():
            print(f'{school_year}: {count} data points')

        print('\nSchools:')
        for school, count in self.schools(count=True).items():
            print(f'{school}: {count} data points')

    def completions(self, count=False):
        completed_modules = []
        for student in self.students():
            if student.has_m1 is None:
                completed_modules.append('m1_None')
            elif student.has_m1:
                completed_modules.append('m1_complete')
            else:
                completed_modules.append('m1_incomplete')

            if student.has_m2 is None:
                completed_modules.append('m2_None')
            elif student.has_m2:
                completed_modules.append('m2_complete')
            else:
                completed_modules.append('m2_incomplete')

            if student.has_m3 is None:
                completed_modules.append('m3_None')
            elif student.has_m3:
                completed_modules.append('m3_complete')
            else:
                completed_modules.append('m3_incomplete')

        if count:
            return dict(sorted(Counter(completed_modules).items()))
        else:
            return completed_modules

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

    def school_years(self, count=False):
        school_years = []
        for student in self.students():
            school_years.append(student.school_year)
        if count:
            return dict(sorted(Counter(school_years).items()))
        else:
            return school_years

    def schools(self, count=False):
        schools = []
        for student in self.students():
            schools.append(student.school.name)
        if count:
            return dict(sorted(Counter(schools).items()))
        else:
            return schools

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
            return filtered
        else:
            raise ValueError("Invalid sex value. Accepted values are 'M' or 'F'.")

    def by_age(self, ages_array):
        filter_function = lambda student: student.age in ages_array
        filtered = self._student_filter(filter_function)
        filtered.age_group = ages_array
        for block in filtered.blocks:
            block.age_group = ages_array
        return filtered

    def by_forwarding(self, forwarding_id):
        filter_function = lambda student: student.forwarding == forwarding_id
        filtered = self._student_filter(filter_function)
        filtered.module = forwarding_id
        for block in filtered.blocks:
            block.forwarding = forwarding_id
        return filtered

    def by_school_year(self, school_year):
        filter_function = lambda student: student.school_year == school_year
        filtered = self._student_filter(filter_function)
        filtered.school_year = school_year
        for block in filtered.blocks:
            block.school_year = school_year
        return filtered

    def by_module_completion(self, module, completed):
        filter_function = lambda student: getattr(student, f'has_m{module}') == completed
        filtered = self._student_filter(filter_function)
        filtered.completed[f'm{module}'] = completed
        for block in filtered.blocks:
            block.completed[f'm{module}'] = completed
        return filtered

    def by_school(self, school):
        filter_function = lambda student: student.school.name == school
        filtered = self._student_filter(filter_function)
        filtered.school = school
        for block in filtered.blocks:
            block.school = school
        return filtered

    def by_frequency(self, frequency_range):
        filter_function = lambda student: student.mean_days_per_week() in frequency_range
        filtered = self._student_filter(filter_function)
        filtered.frequency_range = frequency_range
        for block in filtered.blocks:
            block.frequency_range = frequency_range
        return filtered

    def days_per_week(self):
        students = Students_Container(students=[s for s in self.blocks[0].data["students"] if s is not None])
        return students.days_per_week()

    def custom_range(self, custom_intervals):
        return RangeContainer(custom_intervals)

    def _student_filter(self, filter_function):
        return self._filter(filter_function, self.create())


class ACOLE_Container(Container):
    def __init__(self, **kwargs):
        super(ACOLE_Container, self).__init__(**kwargs)
        blocks = {'LEITURA' : Block(3843, 'Leitura', 'CD', 8),
                  'DITADO_COMPOSICAO' : Block(3839, 'Ditado por composição', 'AE', 10),
                  'DITADO_MANUSCRITO' : Block(3847, 'Ditado manuscrito', 'AF', 4),
                  'LEITURA_DIFICULDADES' : Block(3240, 'Leitura*', 'CD', 20),
                  'DITADO_COMPOSICAO_DIFICULDADES' : Block(3241, 'Ditado por composição*', 'AE', 20),
                  'DITADO_MANUSCRITO_DIFICULDADES' : Block(3242, 'Ditado manuscrito*', 'AF', 20)}

        for key, value in blocks.items():
            setattr(self, key, value)
            self.blocks.append(value)

        self.id = 372

class ACOLE1_Container(ACOLE_Container):
    def __init__(self, **kwargs):
        super(ACOLE1_Container, self).__init__(**kwargs)

class ACOLE2_Container(ACOLE_Container):
    def __init__(self, **kwargs):
        super(ACOLE2_Container, self).__init__(**kwargs)

class ACOLE3_Container(ACOLE_Container):
    def __init__(self, **kwargs):
        super(ACOLE3_Container, self).__init__(**kwargs)


class MODULE1_Container(Container):
    def __init__(self, **kwargs):
        super(MODULE1_Container, self).__init__(**kwargs)
        blocks = {
            'PASSO_01' : Block(375, 'Passo 1', '', -1),
            'PASSO_02' : Block(395, 'Passo 2', '', -1),
            'PASSO_03' : Block(412, 'Passo 3', '', -1),
            'PASSO_04' : Block(419, 'Passo 4', '', -1),
            'PASSO_05' : Block(425, 'Passo 5', '', -1),
            'PASSO_06' : Block(400, 'Passo 6', '', -1),
            'PASSO_07' : Block(413, 'Passo 7', '', -1),
            'PASSO_08' : Block(431, 'Passo 8', '', -1),
            'PASSO_09' : Block(437, 'Passo 9', '', -1),
            'PASSO_10' : Block(312, 'Passo 10', '', -1),
            'PASSO_11' : Block(319, 'Passo 11', '', -1),
            'PASSO_12' : Block(324, 'Passo 12', '', -1),
            'PASSO_13' : Block(499, 'Passo 13', '', -1),
            'PASSO_14' : Block(327, 'Passo 14', '', -1),
            'PASSO_15' : Block(352, 'Passo 15', '', -1),
            'PASSO_16' : Block(358, 'Passo 16', '', -1),
            'PASSO_17' : Block(364, 'Passo 17', '', -1),
            'PASSO_18' : Block(511, 'Passo 18', '', -1),
            'PASSO_19' : Block(549, 'Passo 19', '', -1),
            'PASSO_20' : Block(552, 'Passo 20', '', -1),
            'EXTAI' : Block(1458, 'Leitura A', 'CD', 0),
            'EXTBI' : Block(1521, 'Leitura B', 'CD', 0),
            'EXTCI' : Block(1461, 'Ditado manuscrito', 'AE', 0),
            'EXTDI' : Block(1459, 'Ditado por composição', 'AF', 0),
            'EXTAF' : Block(1464, 'Leitura A*', 'CD', 0),
            'EXTBF' : Block(1465, 'Leitura B*', 'CD', 0),
            'EXTCF' : Block(1466, 'Ditado manuscrito*', 'AE', 0),
            'EXTDF' : Block(1589, 'Ditado por composição*', 'AF', 0)}
        for key, value in blocks.items():
            setattr(self, key, value)
            self.blocks.append(value)

        self.id = MODULO1_ID
        self.name = 'Módulo 1'

    def _student_filter(self, filter_function):
        return self._filter(filter_function, MODULE1_Container())

    def by_completion(self, completed):
        return self.by_module_completion(1, completed)


class MODULE2_Container(Container):
    def __init__(self, **kwargs):
        super(MODULE2_Container, self).__init__(**kwargs)
        blocks = {
            'PASSO_01' : Block(2375, 'Passo 1 (Ç)', '', -1),
            'PASSO_02' : Block(2215, 'Passo 2 (Ç)', '', -1),
            'PASSO_03' : Block(2294, 'Passo 3 (Ç)', '', -1),
            'PASSO_04' : Block(2295, 'Passo 4 (Ç)', '', -1),
            'PASSO_05' : Block(2296, 'Passo 1 (CE-CI)', '', -1),
            'PASSO_06' : Block(2297, 'Passo 2 (CE-CI)', '', -1),
            'PASSO_07' : Block(2298, 'Passo 3 (CE-CI)', '', -1),
            'PASSO_08' : Block(2299, 'Passo 4 (CE-CI)', '', -1),
            'PASSO_09' : Block(2300, 'Passo 1 (LH)', '', -1),
            'PASSO_10' : Block(2301, 'Passo 2 (LH)', '', -1),
            'PASSO_11' : Block(2302, 'Passo 3 (LH)', '', -1),
            'PASSO_12' : Block(2303, 'Passo 4 (LH)', '', -1),
            'PASSO_13' : Block(2304, 'Passo 1 (NH)', '', -1),
            'PASSO_14' : Block(2305, 'Passo 2 (NH)', '', -1),
            'PASSO_15' : Block(2306, 'Passo 3 (NH)', '', -1),
            'PASSO_16' : Block(2307, 'Passo 4 (NH)', '', -1),
            'PASSO_17' : Block(2308, 'Passo 1 (LH)', '', -1),
            'PASSO_18' : Block(2309, 'Passo 2 (LH)', '', -1),
            'PASSO_19' : Block(2310, 'Passo 3 (LH)', '', -1),
            'PASSO_20' : Block(2311, 'Passo 4 (LH)', '', -1),
            'PASSO_21' : Block(2312, 'Passo 1 (GE-GEI)', '', -1),
            'PASSO_22' : Block(2313, 'Passo 2 (GE-GI)', '', -1),
            'PASSO_23' : Block(2314, 'Passo 3 (GE-GI)', '', -1),
            'PASSO_24' : Block(2315, 'Passo 4 (GE-GI)', '', -1),
            'PASSO_25' : Block(2316, 'Passo 1 (VRC)', '', -1),
            'PASSO_26' : Block(2317, 'Passo 2 (VRC)', '', -1),
            'PASSO_27' : Block(2318, 'Passo 3 (VRC)', '', -1),
            'PASSO_28' : Block(2319, 'Passo 4 (VRC)', '', -1),
            'PASSO_29' : Block(2320, 'Passo 1 (VSC)', '', -1),
            'PASSO_30' : Block(2321, 'Passo 2 (VSC)', '', -1),
            'PASSO_31' : Block(2322, 'Passo 3 (VSC)', '', -1),
            'PASSO_32' : Block(2323, 'Passo 4 (VSC)', '', -1),
            'PASSO_33' : Block(2324, 'Passo 1 (VNC)', '', -1),
            'PASSO_34' : Block(2325, 'Passo 2 (VNC)', '', -1),
            'PASSO_35' : Block(2326, 'Passo 3 (VNC)', '', -1),
            'PASSO_36' : Block(2327, 'Passo 4 (VNC)', '', -1),
            'PASSO_37' : Block(2328, 'Passo 1 (VLC)', '', -1),
            'PASSO_38' : Block(2329, 'Passo 2 (VLC)', '', -1),
            'PASSO_39' : Block(2330, 'Passo 3 (VLC)', '', -1),
            'PASSO_40' : Block(2331, 'Passo 4 (VLC)', '', -1),
            'PASSO_41' : Block(2332, 'Passo 1 (Rbrando)', '', -1),
            'PASSO_42' : Block(2824, 'Passo 2 (Rbrando)', '', -1),
            'PASSO_43' : Block(2334, 'Passo 3 (Rbrando)', '', -1),
            'PASSO_44' : Block(2335, 'Passo 4 (Rbrando)', '', -1),
            'PASSO_45' : Block(2336, 'Passo 1 (RR)', '', -1),
            'PASSO_46' : Block(2337, 'Passo 2 (RR)', '', -1),
            'PASSO_47' : Block(2338, 'Passo 3 (RR)', '', -1),
            'PASSO_48' : Block(2825, 'Passo 4 (RR)', '', -1),
            'PASSO_49' : Block(2340, 'Passo 1 (S=Z)', '', -1),
            'PASSO_50' : Block(2341, 'Passo 2 (S=Z)', '', -1),
            'PASSO_51' : Block(2342, 'Passo 3 (S=Z)', '', -1),
            'PASSO_52' : Block(2343, 'Passo 4 (S=Z)', '', -1),
            'PASSO_53' : Block(2344, 'Passo 1 (SS)', '', -1),
            'PASSO_54' : Block(2345, 'Passo 2 (SS)', '', -1),
            'PASSO_55' : Block(2837, 'Passo 3 (SS)', '', -1),
            'PASSO_56' : Block(2347, 'Passo 4 (SS)', '', -1),
            'PASSO_57' : Block(2348, 'Passo 1 (CRV)', '', -1),
            'PASSO_58' : Block(2349, 'Passo 2 (CRV)', '', -1),
            'PASSO_59' : Block(2350, 'Passo 3 (CRV)', '', -1),
            'PASSO_60' : Block(2351, 'Passo 4 (CRV)', '', -1),
            'PASSO_61' : Block(2352, 'Passo 1 (CLV)', '', -1),
            'PASSO_62' : Block(2353, 'Passo 2 (CLV)', '', -1),
            'PASSO_63' : Block(2354, 'Passo 3 (CLV)', '', -1),
            'PASSO_64' : Block(2355, 'Passo 4 (CLV)', '', -1),
            'PASSO_65' : Block(2356, 'Passo 1 (QUE-QUI)', '', -1),
            'PASSO_66' : Block(2357, 'Passo 2 (QUE-QUI)', '', -1),
            'PASSO_67' : Block(2358, 'Passo 3 (QUE-QUI)', '', -1),
            'PASSO_68' : Block(2359, 'Passo 4 (QUE-QUI)', '', -1),
            'PASSO_69' : Block(2360, 'Passo 1 (Ã-ÃO)', '', -1),
            'PASSO_70' : Block(2361, 'Passo 2 (Ã-ÃO)', '', -1),
            'PASSO_71' : Block(2362, 'Passo 3 (Ã-ÃO)', '', -1),
            'PASSO_72' : Block(2363, 'Passo 4 (Ã-ÃO)', '', -1),
            'PASSO_73' : Block(2364, 'Passo 1 (XIS)', '', -1),
            'PASSO_74' : Block(2365, 'Passo 2 (XIS)', '', -1),
            'PASSO_75' : Block(2839, 'Passo 3 (XIS)', '', -1),
            'PASSO_76' : Block(2367, 'Passo 4 (XIS)', '', -1),
            'PASSO_77' : Block(2368, 'Passo 1 (GUE-GUI)', '', -1),
            'PASSO_78' : Block(2369, 'Passo 2 (GUE-GUI)', '', -1),
            'PASSO_79' : Block(2370, 'Passo 3 (GUE-GUI)', '', -1),
            'PASSO_80' : Block(2371, 'Passo 4 (GUE-GUI)', '', -1),
            'DITADO_COMPOSICAO_01' : Block(2049, 'MLEG 1', 'AE', 0),
            'DITADO_COMPOSICAO_02' : Block(2051, 'MLEG 2', 'AE', 0),
            'DITADO_COMPOSICAO_03' : Block(3809, 'MLEG 3', 'AE', 0),
            'DITADO_COMPOSICAO_04' : Block(5089, 'MLEG 4', 'AE', 0),
            'DITADO_COMPOSICAO_05' : Block(2057, 'MLEG 5', 'AE', 0),
            'DITADO_COMPOSICAO_06' : Block(2059, 'MLEG 6', 'AE', 0),
            'DITADO_COMPOSICAO_07' : Block(2061, 'MLEG 7', 'AE', 0),
            'DITADO_COMPOSICAO_08' : Block(2063, 'MLEG 8', 'AE', 0),
            'DITADO_COMPOSICAO_09' : Block(2066, 'MLEG 9', 'AE', 0),
            'DITADO_COMPOSICAO_10' : Block(3811, 'MLEG 10', 'AE', 0),
            'DITADO_COMPOSICAO_11' : Block(2071, 'MLEG 11', 'AE', 0),
            'DITADO_COMPOSICAO_12' : Block(5090, 'MLEG 12', 'AE', 0),
            'DITADO_COMPOSICAO_13' : Block(5092, 'MLEG 13', 'AE', 0),
            'DITADO_COMPOSICAO_14' : Block(5093, 'MLEG 14', 'AE', 0),
            'DITADO_COMPOSICAO_15' : Block(5094, 'MLEG 15', 'AE', 0),
            'DITADO_COMPOSICAO_16' : Block(5095, 'MLEG 16', 'AE', 0),
            'DITADO_COMPOSICAO_17' : Block(5096, 'MLEG 17', 'AE', 0),
            'DITADO_COMPOSICAO_18' : Block(3570, 'MLEG 18', 'AE', 0),
            'DITADO_COMPOSICAO_19' : Block(3571, 'MLEG 19', 'AE', 0),
            'DITADO_COMPOSICAO_20' : Block(3572, 'MLEG 20', 'AE', 0),
            'DITADO_COMPOSICAO_21' : Block(3573, 'MLEG 21', 'AE', 0)}

        for key, value in blocks.items():
            setattr(self, key, value)
            self.blocks.append(value)

        self.id = MODULO2_ID
        self.name = 'Módulo 2'

    def _student_filter(self, filter_function):
        return self._filter(filter_function, MODULE2_Container())

    def by_completion(self, completed):
        return self.by_module_completion(2, completed)


class MODULE3_Container(Container):
    def __init__(self, **kwargs):
        super(MODULE3_Container, self).__init__(**kwargs)
        blocks = {
            'LIVRO_01' : Block(1988, 'Regina e o mágico', 'M3', -1),
            'LIVRO_02' : Block(1989, 'O caracol viajante', 'M3', -1),
            'LIVRO_03' : Block(1990, 'O peru de peruca', 'M3', -1),
            'LIVRO_04' : Block(1991, 'A foca famosa', 'M3', -1),
            'LIVRO_05' : Block(1992, 'O menino e o muro', 'M3', -1),
            'LIVRO_06' : Block(1993, 'A onça e a anta', 'M3', -1),
            'LIVRO_07' : Block(1994, 'O macaco medroso', 'M3', -1),
            'LIVRO_08' : Block(1995, 'O sonho da vaca', 'M3', -1),
            'LIVRO_09' : Block(1996, 'A arara cantora', 'M3', -1),
            'LIVRO_10' : Block(1997, 'O barulho fantasma', 'M3', -1),
            'LIVRO_11' : Block(1998, 'O peixe pixote', 'M3', -1),
            'LIVRO_12' : Block(1999, 'Um palhaço diferente', 'M3', -1),
            'LIVRO_13' : Block(2000, 'A festa encrencada', 'M3', -1),
            'LIVRO_14' : Block(2001, 'O susto do periquito', 'M3', -1),
            'LIVRO_15' : Block(2002, 'O mistério da lua', 'M3', -1),

            'BLOCO_01' : Block(3224, 'Regina e o mágico', 'M3', 0),
            'BLOCO_02' : Block(3246, 'O caracol viajante', 'M3', 0),
            'BLOCO_03' : Block(3247, 'O peru de peruca', 'M3', 0),
            'BLOCO_04' : Block(3257, 'A foca famosa', 'M3', 0),
            'BLOCO_05' : Block(3483, 'O menino e o muro', 'M3', 0),
            'BLOCO_06' : Block(3484, 'A onça e a anta', 'M3', 0),
            'BLOCO_07' : Block(3485, 'O macaco medroso', 'M3', 0),
            'BLOCO_08' : Block(3490, 'O sonho da vaca', 'M3', 0),
            'BLOCO_09' : Block(3493, 'A arara cantora', 'M3', 0),
            'BLOCO_10' : Block(2792, 'O barulho fantasma', 'M3', 0),
            'BLOCO_11' : Block(3502, 'O peixe pixote', 'M3', 0),
            'BLOCO_12' : Block(3512, 'Um palhaço diferente', 'M3', 0),
            'BLOCO_13' : Block(3518, 'A festa encrencada', 'M3', 0),
            'BLOCO_14' : Block(3497, 'O susto do periquito', 'M3', 0),
            'BLOCO_15' : Block(3498, 'O mistério da lua', 'M3', 0)}
        for key, value in blocks.items():
            setattr(self, key, value)
            self.blocks.append(value)

        self.id = MODULO3_ID
        self.name = 'Módulo 3'

    def _student_filter(self, filter_function):
          return self._filter(filter_function, MODULE3_Container())

    def by_completion(self, completed):
        return self.by_module_completion(3, completed)
