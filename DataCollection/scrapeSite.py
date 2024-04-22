from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
website = "https://www.premierleague.com"


if __name__ == "__main__":
    #Scraping Premier League website since 92/93 season
    websitePath = "https://www.premierleague.com/clubs/"
    response = requests.get(websitePath, timeout=10)
    if response.status_code == 200:
        #If i get successful get request
        premSite = response.text
        premSite = BeautifulSoup(premSite, "html.parser")        
        #Data i want to hold
        data = {
            "Club Name": [],
            "Matches Played": [],
            "Wins" : [],
            "Losses": [],
            "Goals Scored": [],
            "Goals Conceded" : [],
            "Clean Sheets" : [],

        }

        


        for clubCard in premSite.find_all("li", class_ = "club-card-wrapper"):
            # Get Club name
            data["Club Name"].append(clubCard.find("h2", class_="club-card__name").text.replace(" ", "-").replace("&", "and"))
            # Get the club link
            clubStatsURL = clubCard.find("a").get("href")
            statsPageResponse = requests.get(website+clubStatsURL.replace("overview", "stats"), timeout=10)
            #
            if statsPageResponse.status_code == 200:
                statsPageResponse = statsPageResponse.text
                statsPage = BeautifulSoup(statsPageResponse, "html.parser")
                data["Matches Played"].append( int( statsPage.find("span", class_="allStatContainer js-all-stat-container statmatches_played").text.strip().replace(",","")) )
                data["Wins"].append( int( statsPage.find("span", class_="allStatContainer js-all-stat-container statwins").text.strip().replace(",","")) ) 
                data["Losses"].append( int( statsPage.find("span", class_="allStatContainer js-all-stat-container statlosses").text.strip().replace(",","")) ) 
                data["Goals Scored"].append( int( statsPage.find("span", class_="allStatContainer js-all-stat-container statgoals").text.strip().replace(",","")) )
                data["Goals Conceded"].append( int( statsPage.find("span", class_="allStatContainer js-all-stat-container statgoals_conceded").text.strip().replace(",","")) )
                data["Clean Sheets"].append( int(statsPage.find("span", class_="allStatContainer js-all-stat-container statclean_sheet").text.strip().replace(",","")) )

        data = pd.DataFrame(data)

        print(data)



        

    else:
        print("Error")
