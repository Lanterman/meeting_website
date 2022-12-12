import os
import databases
import sqlalchemy

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# To run the project, you need to set the TESTING variable to False.
# To run the tests, you need to set the TESTING variable to True.
TESTING = False

DATABASE_URL = os.environ.get("DOC_DATABASE_URL", os.environ["DATABASE_URL"])

TESTING_DATABASE_URL = os.environ.get("DOC_TESTING_DATABASE_URL", os.environ["TESTING_DATABASE_URL"])

metadata = sqlalchemy.MetaData()

# connect_args={"check_same_thread": False} only use with sqlite
if TESTING:
    engine = sqlalchemy.create_engine(TESTING_DATABASE_URL, connect_args={"check_same_thread": False})
    database = databases.Database(TESTING_DATABASE_URL)
else:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    database = databases.Database(DATABASE_URL)
