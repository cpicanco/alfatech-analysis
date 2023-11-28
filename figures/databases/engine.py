"""
# you should use python env to install the following packages to avoid dependency conflicts
py -m pip install mysql-connector-python
py -m pip install SQLAlchemy
"""
from sqlalchemy import create_engine

geic_db = create_engine('mysql+mysqlconnector://root:@localhost/geic', echo=False)