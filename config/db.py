import databases
import sqlalchemy


# To run the project, you need to set the TESTING variable to False.
# To run the tests, you need to set the TESTING variable to True.
TESTING = False

DATABASE_URL = "sqlite:///./meeting_website.db"
# DATABASE_URL = "postgresql://lanterman:karmavdele@localhost/meeting_website"
# DATABASE_URL = "postgreql:///postgres:postgres@postgres_db/postgres"

TESTING_DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://lanterman:karmavdele@localhost/test"
# DATABASE_URL = "postgreql:///postgres:postgres@postgres_db/test_postgres"

metadata = sqlalchemy.MetaData()

if TESTING:
    engine = sqlalchemy.create_engine(TESTING_DATABASE_URL, connect_args={"check_same_thread": False})
    database = databases.Database(TESTING_DATABASE_URL)
else:
    engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    database = databases.Database(DATABASE_URL)
