from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.settings.settings import DATABASE_SETTINGS
from sqlalchemy_utils import database_exists, create_database


# creating the engine
engine = create_engine(url=DATABASE_SETTINGS["URL"])

# Ensure database exists
if not database_exists(engine.url):
    create_database(engine.url)

# creating the db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declare a mapping Base class
Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
