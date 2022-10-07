import databases
import sqlalchemy


DATABASE_URL = "sqlite:///./meeting_website.db"
# DATABASE_URL = "postgresql://lanterman:karmavdele@localhost/meeting_website"
# DATABASE_URL = "postgreql:///postgres:postgres@postgres_db/postgres"

TESTING_DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://lanterman:karmavdele@localhost/test"
# DATABASE_URL = "postgreql:///postgres:postgres@postgres_db/test_postgres"

metadata = sqlalchemy.MetaData()

# For test
engine = sqlalchemy.create_engine(TESTING_DATABASE_URL, connect_args={"check_same_thread": False})
database = databases.Database(TESTING_DATABASE_URL)

# For project
# engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# database = databases.Database(DATABASE_URL)
