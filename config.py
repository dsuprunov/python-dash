from datetime import datetime
from sqlalchemy.engine import URL


DATA_CSV_FILE = './census.csv'
DATA_SQLITE_FILE = './census.db.sqlite3'

#
# SQLAlchemy
#
SQLALCHEMY_ECHO = True
SQLALCHEMY_TEMP_IMPORT_TABLE_NAME = f'temp_import_{datetime.now().strftime("%Y%m%d%H%M%S%f")}'
SQLALCHEMY_URL = URL.create(
    drivername='sqlite',
    database=DATA_SQLITE_FILE,
)
