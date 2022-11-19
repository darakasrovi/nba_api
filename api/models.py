from sqlalchemy import Column, Integer, String, Numeric, DateTime
from .database import Base


class Team(Base):
    __tablename__ = "teams"
    team_id = Column("team_id", Integer, primary_key=True, nullable=False)
    division = Column("division", String)
    team = Column("team", String)


class Player(Base):
    __tablename__ = "players"

    player_id = Column("player_id", Integer, primary_key=True)
    team_id = Column("team_id", Integer)
    season = Column("season", Integer)
    player = Column("player", String)
    num = Column("num", Integer)
    position = Column("position", String)
    height = Column("height", Numeric)
    weight = Column("weight", Numeric)
    birth_date = Column("birth_date", DateTime)
    age = Column("age", Integer)
    exp = Column("exp", String)
    school = Column("school", String)


class QuickStat(Base):
    __tablename__ = "quickstats"

    player_id = Column("player_id", Integer, primary_key=True)
    ppg = Column("ppg", Numeric)
    rpg = Column("rpg", Numeric)
    apg = Column("apg", Numeric)
    pie = Column("pie", Numeric)


class CareerStat(Base):
    __tablename__ = "careerstats"

    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False)
    season = Column("season", String)
    team = Column("team", String)
    age = Column("age", Integer)
    gp = Column("gp", Integer)
    gs = Column("gs", Integer)
    min = Column("min", Integer)
    pts = Column("pts", Integer)
    fgm = Column("fgm", Integer)
    fga = Column("fga", Integer)
    fg_percentage = Column("fg%", Integer)
    three_pm = Column("3pm", Integer)
    three_pa = Column("3pa", Integer)
    three_p_percentage = Column("3p%", Numeric)
    ftm = Column("ftm", Integer)
    fta = Column("fta", Integer)
    ft_percentage = Column("ft%", Numeric)
    oreb = Column("oreb", Integer)
    dreb = Column("dreb", Integer)
    reb = Column("reb", Integer)
    ast = Column("ast", Integer)
    stl = Column("stl", Integer)
    blk = Column("blk", Integer)
    tov = Column("tov", Integer)
    pf = Column("pf", Integer)
    player_id = Column("player_id", Integer)
