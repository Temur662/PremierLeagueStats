from flask import Flask,jsonify, request, send_file
import sys
import io
sys.path.append("..")
import matplotlib
matplotlib.use("agg")
import psycopg2
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from manipulateData import compareTeams, getBestPerformingTeam, getWorstPerfomingTeam, getData, getClubMatchOutcomes
from db import connect_to_db
load_dotenv()

premApp = Flask(__name__)

def loadData():
    conection = connect_to_db()
    cur = conection.cursor()
    cur.execute("""
        SELECT id, clubname, matchesplayed, wins, losses, goalsscored, goalsconceded, cleansheets FROM premstats23_24
    """)
    data = cur.fetchall()
    cur.close()
    conection.close()
    return data

@premApp.route("/")
def hello():
    return "<p> Hello </p>"


@premApp.route("/stats", methods = ["GET"])
def getPremStats():
    data = loadData()
    columns = ["id", "clubname", "matchesplayed", "wins", "losses", "goalsscored", "cleansheets"]
    result = [dict(zip(columns, row)) for row in data]

    return jsonify(result)

@premApp.route("/compareTeams", methods = ["GET"])
def compare():
    data = getData()
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")
    fig = compareTeams(data, team1, team2)
    buf = io.BytesIO()
    fig.savefig(buf, format ="png")
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")
    
@premApp.route("/bestTeam", methods = ["GET"])
def getBestTeam():
    data = getData()
    team = getBestPerformingTeam(data)
    connection = connect_to_db()
    cur = connection.cursor()
    cur.execute(f""" 
    SELECT clubname, matchesplayed, wins, losses, goalsscored, goalsconceded, cleansheets
    FROM premstats23_24
    WHERE clubname = '{team}'            
    """)
    teamData = cur.fetchall()
    cur.close()
    connection.close()
    cols = ["clubname", "matchesplayed", "wins", "losses", "goalsscored", "cleansheets"]
    result = [dict(zip(cols, data)) for data in teamData]
    return jsonify(result)


@premApp.route("/worstTeam", methods = ["GET"])
def getWorst():
    data = getData()
    team = getWorstPerfomingTeam(data)
    connection = connect_to_db()
    cur = connection.cursor()
    cur.execute(f""" 
    SELECT clubname, matchesplayed, wins, losses, goalsscored, goalsconceded, cleansheets
    FROM premstats23_24
    WHERE clubname = '{team}'            
    """)
    teamData = cur.fetchall()
    cur.close()
    connection.close()
    cols = ["clubname", "matchesplayed", "wins", "losses", "goalsscored", "cleansheets"]
    result = [dict(zip(cols, data)) for data in teamData]
    return jsonify(result)

@premApp.route("/clubMatchOutcomes", methods=["GET"])
def getMatchOutComes():
        data = getData()
        club = request.args.get("club")
        fig = getClubMatchOutcomes(data, club)
        buf = io.BytesIO()
        fig.savefig(buf, format ="png")
        plt.close(fig)
        buf.seek(0)
        return send_file(buf, mimetype="image/png")
    
if __name__ == '__main__':
    premApp.run(host='0.0.0.0', port=10000, debug=True)