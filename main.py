import os

from sqlalchemy import text

from databases import geic_db, alfatech_students_ids

# Set the path to the SQL query template file
sql_query_template_file = os.path.join(os.path.dirname(__file__), 'queries', 'trials_by_student_id.sql')
print(sql_query_template_file)

# Load the SQL query from the file
with open(sql_query_template_file, 'r') as file:
    sql_query_template = file.read()

# Execute the SQL query
with geic_db.connect() as connection:
    sql_query = text(sql_query_template).bindparams(STUDENT_ID=alfatech_students_ids[0])
    result = connection.execute(sql_query)

    # Fetch and print the rows
    print(result.keys())
    # rows = result.fetchall()
    rows = result.fetchmany(10)
    for row in rows:
        print(row)