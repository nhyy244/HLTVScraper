from bs4 import BeautifulSoup
import requests
from datetime import date
import time
from selenium import webdriver


_today = date.today() # "private" field

class Player:
    def __init__(self,playerURL):
        self.playerURL = playerURL
        urlSplit = self.playerURL.split("/")
        self.playerName = urlSplit[-1] #name is the last of URL (from left to right)
        self.playerID= int(urlSplit[-2]) #ID is the second last of URL (from  left  to right)
        self.playerURL = playerURL
        self.playerTeam = ""
        self.kills =""
        self.deaths =""
        self.assists = ""
        self.clutchURLS =[]
        self.hltvURL = "https://www.hltv.org/stats/players/individual/"
        self.todayDateURL = "startDate=" + _today.strftime("%Y-%m-%d") + "&" + "endDate=" + _today.strftime("%Y-%m-%d")

    def getPlayerName(self):
        return self.playerName

    def getPlayerTeam(self):
        return self.playerTeam

    def getPlayerID(self):
        return self.playerID

    def getPlayerURL(self):
        return self.playerURL

    def getPlayerKills(self):
        return self.kills

    def getPlayerDeaths(self):
        return self.deaths

    def getPlayerAssists(self):
        return self.assists

    def getClutchURLS(self):
        return self.clutchURLS

    def getSoup(self,URLSpecific):
        #page = requests.get(URLSpecific)
        dr = webdriver.Chrome()
        dr.get(URLSpecific)
        soup = BeautifulSoup(dr.page_source)
        return soup

    def setPlayerKills(self, kills):
        self.kills = kills

    def setPlayerDeaths(self, deaths):
        self.deaths = deaths

    def setPlayerAssists(self, assists):
        self.assists = assists

    def setPlayerTeam(self,team):
        self.playerTeam=team


    def appendClutchURL(self,url):
        self.clutchURLS.append(url)



    # Gets EKs for player
    def getPlayerEK(self):

        #dateURLFake= "startDate=" + "2022-03-15"+"&"+"endDate=" + today.strftime("%Y-%m-%d")
        #playerName = self.getPlayerName()
        #playerID = self.getPlayerID()
        urlEK = self.hltvURL + str(self.playerID) + "/" + self.playerName + "?" + self.todayDateURL
        #print(urlEK)

        #   BEGIN SCRAPING EK
        soup = self.getSoup(urlEK)
        overallStatsCol = soup.find_all("div", class_="stats-rows")
        time.sleep(1)
        standardBoxEk = overallStatsCol[0].find_all("div", class_="standard-box")
        playersEK = standardBoxEk[1].find_all("span")[1].text

        return playersEK

    #4ks and 5ks
    def getMultiKills(self,multiKillType):
        multiKill = ""

        urlMultiKills = self.hltvURL + str(self.playerID) + "/" + self.playerName + "?" + self.todayDateURL

        #   BEGIN SCRAPING EK
        soup = self.getSoup(urlMultiKills)
        overallStatsCol = soup.find_all("div", class_="stats-rows")
        time.sleep(1) 
        standardBoxEk = overallStatsCol[1].find_all("div", class_="standard-box")
        if multiKillType == "4k":
            multiKill += standardBoxEk[0].find_all("span")[-3].text
        elif multiKillType == "5k":
            multiKill += standardBoxEk[0].find_all("span")[-1].text

        return multiKill









