import pandas as pd

from databases.students import students
from methods import opt
"""
    Tabela 1
    Número de alunos com a primeira ACOLE, por escola
"""

def table1():
    # exclude = [10064]
    # for student in students.by_has_acole():
    #     if student.id == 10064:
    #         print('wrong')

    data_dict = students.by_has_acole().schools(True)
    data_list = [{'Escola': key, 'n': value, '%': (value / sum(data_dict.values())) * 100} for key, value in data_dict.items()]

    df = pd.DataFrame(data_list)

    # Calculate total values
    total_n = df['n'].sum()
    total_percentage = df['%'].sum()

    # Append a total row to the DataFrame
    df.loc[len(df)] = ['Total', total_n, total_percentage]
    df = df.sort_values(by='n')

    opt.set_filename('tabela1')
    opt.cd('tables')
    opt.extension = '.xlsx'
    df.to_excel(opt.output_path(), index=False)
    print(df)

"""
    Tabela 2
    Número de alunos com a primeira ACOLE,
    por idade e gênero
"""

def table2():
    df = students.by_has_acole().to_data_frame()
    df = df.groupby(['Idade', 'Sexo']).size().reset_index(name='n')
    df['%'] = (df['n'] / df['n'].sum()) * 100

    # Calculate total values
    total_n = df['n'].sum()
    total_percentage = df['%'].sum()

    # Create a DataFrame for the total row
    total_row = pd.DataFrame({'Idade': ['Total'], 'Sexo': [''], 'n': [total_n], '%': [total_percentage]})

    # Concatenate the original DataFrame with the total row DataFrame
    df = pd.concat([df, total_row], ignore_index=True)
    # df = df.sort_values(by='n')
    opt.set_filename('tabela2')
    opt.cd('tables')
    opt.extension = '.xlsx'
    df.to_excel(opt.output_path(), index=False)
    print(df)

if __name__ == "__main__":
    table2()