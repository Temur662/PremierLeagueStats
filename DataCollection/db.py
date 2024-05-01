
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
"""
CREATE TABLE PremStats23_24(
    id SERIAL PRIMARY KEY,
    clubName VARCHAR(50)
    matchesPlayed VARCHAR(50),
    wins VARCHAR(50),
    losses VARCHAR(50)
    goalScored VARCHAR(50),
    goalConceded VARCHAR(50),
    cleanSheets VARCHAR(50),
)
"""
def connect_to_db():
    try:
        # Replace 'dbname', 'user', 'password', and 'host' with your database details
        connection = psycopg2.connect(
            dbname="PremStats",
            user="PremStats_owner",
            password="2lcFV4zrHdvg",
            host="ep-sweet-math-a58sz7gn.us-east-2.aws.neon.tech"
        )
        connection.autocommit = True
        print("Connected to the database successfully")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")

def insertData(dbconnection, theStats):
    cursor = dbconnection.cursor()
    query = """
    INSERT INTO premstats23_24(clubName, matchesPlayed, wins, losses, goalsScored, goalsConceded, cleanSheets)
    VALUES(%s, %s, %s, %s, %s, %s, %s);
    """
    for data in theStats:
        cursor.execute(query, (data["Club Name"], data["Matches Played"], data["Wins"], data["Losses"], data["Goals Scored"], data["Goals Conceded"], data["Clean Sheets"]))
    print("Data inserted Successfully")
"""
data = {
            "Club Name": [],
            "Matches Played": [],
            "Wins" : [],
            "Losses": [],
            "Goals Scored": [],
            "Goals Conceded" : [],
            "Clean Sheets" : [],

        }
"""

def fetchData(dbConnection):
    cursor = dbConnection.cursor(cursor_factory=RealDictCursor)
    query = "SELECT * FROM premstats23_24;"
    dataFrame = pd.read_sql_query(query, dbConnection)
    return dataFrame