import os

from fastapi import FastAPI, status, HTTPException
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
import pandas as pd

from api.database import get_db, create_nba_db, engine
from api import models

app = FastAPI()

# Create NBA database
create_nba_db()

# Read in the dataframe
teams = pd.read_csv(os.path.join("data", "teams.csv"))
players = pd.read_csv(os.path.join("data", "players.csv"))
player_quick_stats = pd.read_csv(os.path.join("data", "player_quick_stats.csv"))
player_career_stats = pd.read_csv(os.path.join("data", "player_info.csv"))
player_career_stats.reset_index(inplace=True)
player_career_stats.rename(columns={"index": "id"}, inplace=True)

# Write dataframes to MySQL dbs
teams.to_sql("teams", engine, index=False, if_exists="replace")
players.to_sql("players", engine, index=False, if_exists="replace")
player_quick_stats.to_sql("quickstats", engine, index=False, if_exists="replace")
player_career_stats.to_sql("careerstats", engine, if_exists="replace")


@app.get("/")
async def root():
    return {"message": "welcome to the nba api! for dsci 511 - data acquisition and preprocessing"}


@app.get("/teams")
async def get_all_nba_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams


@app.get("/roster/{team_id}")
async def get_roster(team_id: int, db: Session = Depends(get_db)):
    roster = db \
        .query(models.Player) \
        .filter(models.Player.team_id == team_id) \
        .all()

    if not roster:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"team with id: {team_id} was not found"
        )
    return roster


@app.get("/player/{player_id}")
async def get_player_info(player_id: int, db: Session = Depends(get_db)):
    player = db \
        .query(models.Player) \
        .filter(models.Player.player_id == player_id) \
        .first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"player with id: {player_id} was not found"
        )

    return player


@app.get("/player/quickstats/{player_id}")
async def get_player_quick_stats(player_id: int, db: Session = Depends(get_db)):
    player = db \
        .query(models.QuickStat) \
        .filter(models.QuickStat.player_id == player_id) \
        .first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"player with id: {player_id} was not found"
        )

    return player


@app.get("/player/careerstats/{player_id}")
async def get_player_career_stats(player_id: int, db: Session = Depends(get_db)):
    players = db \
        .query(models.CareerStat) \
        .join(models.Player, models.Player.player_id == models.CareerStat.player_id) \
        .filter(models.Player.player_id == player_id) \
        .all()

    if not players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"player with id: {player_id} was not found"
        )
    return players
