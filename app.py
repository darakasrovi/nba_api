import json

from flask import Flask, Response
from sqlalchemy.orm import sessionmaker
from api.models import engine, teams, players, quick_stats, career_stats

app = Flask(__name__)
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
def index():
    return Response(json.dumps({"message": "welcome to the nba api!",
                                "for": "dsci 511 - data acquisition and preprocessing"}),
                    status=200,
                    mimetype="application/json")


@app.route("/teams")
def get_all_nba_teams():
    teams_ = session.query(teams).all()
    data = [dict(zip(teams.columns.keys(), team)) for team in teams_]
    return Response(json.dumps({"teams": data}), status=200, mimetype="application/json")


@app.route("/roster/<int:team_id>")
def get_roster(team_id: int):
    players_ = session \
        .query(players) \
        .filter_by(team_id=team_id) \
        .all()

    if players_:
        data = [dict(zip(players.columns.keys(), player)) for player in players_]
        return Response(json.dumps({"players": data}), status=200, mimetype="application/json")
    return Response("Record not found", status=400)


@app.route("/player/<int:player_id>")
def get_player_info(player_id: int):
    player = session \
        .query(players, quick_stats) \
        .filter(players.c.player_id == player_id and players.c.player_id == quick_stats.c.player_id) \
        .first()

    table_columns = list(players.columns.keys()) + list(quick_stats.columns.keys())
    if player:
        data = dict(zip(table_columns, player))
        return Response(json.dumps({"player": data}), status=200, mimetype="application/json")
    return Response("Record not found", status=400)


@app.route("/player/careerstats/<int:player_id>")
def get_player_career_stats(player_id: int):
    players_ = session \
        .query(players, career_stats) \
        .filter(players.c.player_id == player_id and players.c.player_id == career_stats.c.player_id) \
        .all()

    table_columns = list(players.columns.keys()) + list(career_stats.columns.keys())
    if players_:
        data = [dict(zip(table_columns, player)) for player in players_]
        return Response(json.dumps({"player": data}), status=200, mimetype="application/json")
    return Response("Record not found", status=400)


if __name__ == "__main__":
    app.run()
