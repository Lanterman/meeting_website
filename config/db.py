import databases
import sqlalchemy


DATABASE_URL = "sqlite:///./meeting_website.db"
# DATABASE_URL = "postgresql://lanterman:karmavdele@localhost/meeting_website"
# DATABASE_URL = "postgreql:///postgres:postgres@postgres_db/postgres"

metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
database = databases.Database(DATABASE_URL)
