from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy_utils import database_exists, create_database
from decouple import config

meta = MetaData()
url = f"mysql+pymysql://{config('USERNAME')}:{config('PASSWORD')}@{config('HOST')}/{config('DB_NAME')}"
engine = create_engine(url)


def create_nba_db() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)


students = Table(
    "teams",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('lastname', String),
)

if __name__ == "__main__":
    create_nba_db()
    print(database_exists(engine.url))
