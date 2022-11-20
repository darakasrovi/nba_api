from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from decouple import config

SQLALCHEMY_DATABASE_URL = "postgresql://tqpmkcmcriksac:10a8ebb5db620acbacda22cc96582fd74d147eef705cbf641ee155847085f9df@ec2-3-209-39-2.compute-1.amazonaws.com:5432/d42tgjq61pdcvl"
    # f"postgresql://{config('USERNAME')}:{config('PASSWORD')}@{config('HOST')}:{config('PORT')}/{config('DB_NAME')}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_nba_db() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)
        print("NBA DB created! :)")
    else:
        print("NBA DB exists! :)")

