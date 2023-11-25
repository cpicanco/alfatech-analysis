import os

def template_from_name(template_name):
    sql_query_template_file = os.path.join(
        os.path.dirname(__file__), template_name +'.sql')

    # Load the SQL query from the file
    with open(sql_query_template_file, 'r', encoding='utf-8') as file:
        return file.read()