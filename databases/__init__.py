"""
# you should use python env to install the following packages to avoid dependency conflicts
py -m pip install mysql-connector-python
py -m pip install SQLAlchemy
"""

from sqlalchemy import create_engine

# from containers import ACOLE_Container
from .containers import ACOLE_Container

geic_db = create_engine('mysql+mysqlconnector://root:@localhost/geic', echo=False)

# project
ALPHATEC = 132

ACOLE = ACOLE_Container()
MODULO_1 = 143
MODULO_2 = 377
MODULO_3 = 383

if __name__ == "__main__":
    # ACOLE.data = 45
    ACOLE.save_to_file()

    TESTE = ACOLE_Container.load_from_file()
    print(TESTE.data)