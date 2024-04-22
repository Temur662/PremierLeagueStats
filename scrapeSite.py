from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd



if __name__ == "__main__":
    #Scraping Premier League website since 92/93 season
    websitePath = "https://www.premierleague.com/clubs/"
    response = requests.get(websitePath)
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

        


        for number, clubCard in enumerate(premSite.find_all("li", class_ = "club-card-wrapper")):
            data["Club Name"].append(clubCard.find("h2", class_="club-card__name").text.replace(" ", "-").replace("&", "and"))
            clubStatsURL = clubCard.find("li", class_="club-card-wrapper").find("a").href
            print(clubStatsURL)









    else:
        print("Error")
