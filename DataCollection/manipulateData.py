from db import fetchData, connect_to_db
import matplotlib.pyplot as plt
import numpy as np
def getData():
    connection = connect_to_db()
    data = fetchData(connection)
    return data

def compareTeams(dataFrame,team1, team2):
    team1Stats = dataFrame.loc[ dataFrame["clubname"] == team1, :]
    team2Stats = dataFrame.loc[ dataFrame["clubname"] == team2, :]
    # AVG Wins
    team1AvgWinRate = round((team1Stats["wins"] / team1Stats["matchesplayed"]), 2)
    team2AvgWinRate = round((team2Stats["wins"] / team2Stats["matchesplayed"]), 2)
    #AVG goals scores
    team1AvgGoalsPerGame = team1Stats["goalsscored"] / team1Stats["matchesplayed"]
    team2AvgGoalsPerGame = team2Stats["goalsscored"] / team2Stats["matchesplayed"]
    #AVG goals conceded
    team1AvgGoalsConPerGame = team1Stats["goalsconceded"] / team1Stats["matchesplayed"]
    team2AvgGoalsConPerGame = team2Stats["goalsconceded"] / team2Stats["matchesplayed"]
    #AVG clean sheets 
    team1AvgCleanPerGame = team1Stats["cleansheets"] / team1Stats["matchesplayed"]
    team2AvgCleanPerGame = team2Stats["cleansheets"] / team2Stats["matchesplayed"]
    data = {
        f"{team1Stats['clubname'].values[0]}":{
            "Avg Win Rate": team1AvgWinRate.values[0],
            "Avg Goal": round(team1AvgGoalsPerGame.values[0],2 ),
            "Avg Goals Conceded":  round(team1AvgGoalsConPerGame.values[0], 2),
            "Avg Clean Sheets": round(team1AvgCleanPerGame.values[0], 2)
        },
        f"{team2Stats['clubname'].values[0]}" :{
            "Avg Win Rate": team2AvgWinRate.values[0],
            "Avg Goal": round(team2AvgGoalsPerGame.values[0], 2),
            "Avg Goals Conceded":  round(team2AvgGoalsConPerGame.values[0], 2),
            "Avg Clean Sheets": round(team2AvgCleanPerGame.values[0], 2)
        }
    }
    barWidth = 0.35
    categories = ["Avg Win Rate", "Avg Goal", "Avg Goals Conceded", "Avg Clean Sheets"]
    positions = np.arange(len(categories))
    fig, ax = plt.subplots()
    team1 = ax.bar(positions - barWidth/2 ,data[team1Stats["clubname"].values[0]].values(), barWidth, label = team1Stats["clubname"].values[0], color="red", edgecolor="black")
    for stat in team1:
        height = stat.get_height()
        ax.annotate("{}".format(height), 
        xy=(stat.get_x() + stat.get_width() / 2, height),
        xytext = (0, 3),
        textcoords = "offset points",
        ha = "center", va = "bottom")
    team2 = ax.bar(positions + barWidth/2 ,data[team2Stats["clubname"].values[0]].values(), barWidth, label = team2Stats["clubname"].values[0], color="blue",edgecolor="black")
    for stat in team2:
        height = stat.get_height()
        ax.annotate("{}".format(height), 
        xy=(stat.get_x() + stat.get_width() / 2, height),
        xytext = (0, 3),
        textcoords = "offset points",
        ha = "center", va = "bottom")
    ax.set_xlabel("Categories")
    ax.set_ylabel("Values")
    ax.set_title ( f"{team1Stats['clubname'].values[0]}  vs {team2Stats['clubname'].values[0]}" )
    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.legend()
    return fig
    
def getBestPerformingTeam(dataFrame):
    bestPerfomer = None
    topAvgWinRate = dataFrame["wins"][0] / dataFrame["matchesplayed"][0]
    for i in range(1, len(dataFrame)):
        teamsAvgWinRate = dataFrame["wins"][i] / dataFrame["matchesplayed"][i]
        if teamsAvgWinRate > topAvgWinRate:
            topAvgWinRate = teamsAvgWinRate
            bestPerfomer = dataFrame["clubname"][i] 
    return bestPerfomer

def getWorstPerfomingTeam(dataFrame):
    worstPerformer = None
    worstAvgWinRate = dataFrame["wins"][0] / dataFrame["matchesplayed"][0]
    for i in range(1, len(dataFrame)):
        teamsAvgWinRate = dataFrame["wins"][i] / dataFrame["matchesplayed"][i]
        if teamsAvgWinRate < worstAvgWinRate:
            worstAvgWinRate = teamsAvgWinRate
            worstPerformer = dataFrame["clubname"][i] 
    return worstPerformer


def getClubMatchOutcomes(dataFrame, club):
    labels = ["Wins", "Losses"]
    wins = dataFrame.loc[dataFrame["clubname"] == club, "wins"].values[0]
    losses = dataFrame.loc[dataFrame["clubname"] == club, "losses"].values[0]
    
    fig, ax = plt.subplots()
    ax.pie([wins,losses], labels=labels,autopct='%1.1f%%')
    ax.set_title(club)
    return fig


if __name__ == "__main__":
    data = getData()
    getClubMatchOutcomes(data, "Arsenal")