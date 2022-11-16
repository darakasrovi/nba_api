import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, Numeric, DateTime
from sqlalchemy_utils import database_exists, create_database
from decouple import config
import pandas as pd

meta = MetaData()
url = f"mysql+pymysql://{config('USERNAME')}:{config('PASSWORD')}@{config('HOST')}/{config('DB_NAME')}"
engine = create_engine(url)


def create_nba_db() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)


teams = Table(
    "Teams", meta,
    Column("division", String(16)),
    Column("team_id", Integer, primary_key=True),
    Column("team", String(16))
)


players = Table(
    "Players", meta,
    Column("player_id", Integer, primary_key=True),
    Column("team_id", Integer),
    Column("season", Integer),
    Column("player", String(16)),
    Column("num", Integer),
    Column("position", String(16)),
    Column("height", Numeric),
    Column("weight", Numeric),
    Column("birth_date", DateTime),
    Column("age", Integer),
    Column("exp", String(16)),
    Column("school", String(16))
)


quick_stats = Table(
    "QuickStats", meta,
    Column("player_id", Integer, primary_key=True),
    Column("ppg", Numeric),
    Column("rpg", Numeric),
    Column("apg", Numeric),
    Column("pie", Numeric)
)


career_stats = Table(
    "CareerStats", meta,
    Column("season", String(16)),
    Column("team", String(16)),
    Column("age", Integer),
    Column("gp", Integer),
    Column("gs", Integer),
    Column("min", Integer),
    Column("pts", Integer),
    Column("fgm", Integer),
    Column("fga", Integer),
    Column("fg%", Integer),
    Column("3pm", Integer),
    Column("3pa", Integer),
    Column("3p%", Numeric),
    Column("ftm", Integer),
    Column("fta", Integer),
    Column("ft%", Numeric),
    Column("oreb", Integer),
    Column("dreb", Integer),
    Column("reb", Integer),
    Column("ast", Integer),
    Column("stl", Integer),
    Column("blk", Integer),
    Column("tov", Integer),
    Column("pf", Integer),
    Column("player_id", Integer)
)


if __name__ == "__main__":
    create_nba_db()
    print(database_exists(engine.url))
    meta.create_all(engine)

    # Read in the dataframe
    teams = pd.read_csv(os.path.join("..", "data", "teams.csv"))
    players = pd.read_csv(os.path.join("..", "data", "players.csv"))
    player_quick_stats = pd.read_csv(os.path.join("..", "data", "player_quick_stats.csv"))
    player_career_stats = pd.read_csv(os.path.join("..", "data", "player_info.csv"))

    # Write dataframes to MySQL dbs
    teams.to_sql("Teams", engine, index=False, if_exists="replace")
    players.to_sql("Players", engine, index=False, if_exists="replace")
    player_quick_stats.to_sql("QuickStats", engine, index=False, if_exists="replace")
    player_career_stats.to_sql("CareerStats", engine, index=False, if_exists="replace")