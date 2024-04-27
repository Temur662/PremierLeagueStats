from bs4 import BeautifulSoup
import os
import requests
import psycopg2 as psy
from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from db import connect_to_db, insertData, fetchData
#from extensions import proxies
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import time
website = "https://www.premierleague.com"




def scrapeWebSite():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    options.page_load_strategy = "none"

    driver = webdriver.Chrome()

    driver.implicitly_wait(5)
    #Scraping premiet leageu stats website for 23/24 season
    websitePath = "https://www.premierleague.com/clubs/"
    response = requests.get(websitePath)
    if response.status_code == 200:
        #If i get successful get request
        premSite = response.text
        premSite = BeautifulSoup(premSite, "html.parser")        
        #Data i want to hold
        data = []

        for clubCard in premSite.find_all("li", class_ = "club-card-wrapper"):
            # Get Club name
            #data["Club Name"].append(clubCard.find("h2", class_="club-card__name").text.replace(" ", "-").replace("&", "and"))
            # Get the club link
            clubStatsURL = clubCard.find("a").get("href")
            clubStatsURL = website+clubStatsURL.replace("overview", "stats")
            print(clubStatsURL)
            driver.get(clubStatsURL)
            time.sleep(10)
            statsPageResponse = BeautifulSoup(driver.page_source, "html.parser")
            if statsPageResponse:
                clubName = statsPageResponse.find("h2", class_="club-header__team-name").text
                print(clubName)
                statsPage = statsPageResponse.findAll("div", class_="all-stats__top-stat-container")
                matchesPlayed = 0
                wins = 0
                losses = 0
                goalsScored = 0
                goalsConceded = 0
                cleanSheets = 0
                for stats in statsPage:
                    if stats.find("span", class_="allStatContainer js-all-stat-container statmatches_played"):
                        matchesPlayed = int( stats.find("span", class_="allStatContainer js-all-stat-container statmatches_played").text.strip().replace(",","")) 
                    if stats.find("span", class_="allStatContainer js-all-stat-container statwins"):
                        wins = int( stats.find("span", class_="allStatContainer js-all-stat-container statwins").text.strip().replace(",","") ) 
                    if stats.find("span", class_="allStatContainer js-all-stat-container statlosses"):
                        losses = int( stats.find("span", class_="allStatContainer js-all-stat-container statlosses").text.strip().replace(",","")) 
                    if stats.find("span", class_="allStatContainer js-all-stat-container statgoals"):
                        goalsScored =  int( stats.find("span", class_="allStatContainer js-all-stat-container statgoals").text.strip().replace(",","")) 
                    if stats.find("span", class_="allStatContainer js-all-stat-container statgoals_conceded"):
                        goalsConceded = int( stats.find("span", class_="allStatContainer js-all-stat-container statgoals_conceded").text.strip().replace(",","")) 
                    if stats.find("span", class_="allStatContainer js-all-stat-container statclean_sheet"):
                        cleanSheets =  int(stats.find("span", class_="allStatContainer js-all-stat-container statclean_sheet").text.strip().replace(",","")) 
                    if matchesPlayed and wins and losses and goalsScored and goalsConceded and cleanSheets:
                        data.append( {"Club Name" : clubName, "Matches Played" : matchesPlayed, "Wins" : wins, "Losses" : losses, "Goals Scored" : goalsScored, "Goals Conceded" : goalsConceded, "Clean Sheets" : cleanSheets} )
        return data
    else:
        print("Error")




if __name__ == "__main__":
    db_connection = connect_to_db()
    data = scrapeWebSite()
    print(data)
    insertData(db_connection, data)
    fetchData(dbConnection=db_connection)
