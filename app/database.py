import psycopg2
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from. import models
import time
from psycopg2.extras import RealDictCursor
from. config import settings
sqlalchemy_database_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(sqlalchemy_database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn =psycopg2.connect(host='localhost', database='fastapi', user='postgres', password = 'Hiwot.246810', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was sucessfull!")
        break
    except Exception as error:
        print ("connnecting to database failed")
        print("Erro: ", error)
        time.sleep(2)
