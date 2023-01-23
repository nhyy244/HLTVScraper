from bs4 import BeautifulSoup
import requests
from datetime import date
import time

from Player import Player

"""
    HELLO AND WELCOME TO MY HLTV SCRAPER
    THE PROGRAM IS MADE ONLY TO SCRAPE SPECIFIC DATA FROM A MATCH
    THE ONLY THING REQUIRED IS AN URL FROM THE MATCH 
    URL NEEDS TO BE THE SPECIFIC STAT PAGE FOR THE MATCH
        for example:("https://www.hltv.org/stats/matches/88459/pain-vs-case")
    WORKS FOR BO3,BO5 AND BO1 MATCHES. THE URL JUST NEEDS TO BE CHANGED
    AVAILABLE DATA FOR SCRAPING:
    
        FOR BO3,BO5: KDA, EK's, 4ks, 5ks, clutches (1v2-1v5)
        FOR INDIVIDUAL MATCHES WITHIN A BO3,BO5: KDA, EK's, 4ks, 5ks, clutches (1v2-1v5)
        FOR BO1: KDA, EK's, 4ks, 5ks, clutches (1v2-1v5)

        Individual data for players is found ONLY BETWEEN A TIME PERIOD. DEFAULT SET TO TODAYS MATCHES
            *CLUTCHES for all players from both teams ( 1v2 to 1v5 )
            *4ks
            *5ks



       #2022-04-15 TASKS:
        * Scrape 4ks and 5ks - DONE
        * Scrape clutches for every player (5 links for every player) -DONE
            * Get clutchURLS1vX for every player - DONE
            * Scrape every url for : Map and Round - DONE

       #Future TASKS:
        * Find a way to append every detail to every player - DONE
        * Refactor getPlayers4k, getPlayers5k (and MAYBE getPlayersEK) - DONE
        * Add a time parameter to the main method. matchStats(URL,mapNr, TimeFilter)
        * Add getPlayerClutches() to the Player class
        * Change the source for mapname so it works for both bo3 and bo1 matches. - DONE
        * Change EK function. EK is NOT Opening Kills. Ek's can be found here: https://www.hltv.org/stats/matches/performance/mapstatsid/139062/big-vs-mibr
            * GOT CHANGED BY HLTV THEMSELVES. OPENING KILLS IS NOW ENTRY KILLS - DONE



"""

today = date.today()
global playersTeam1
global playersTeam2

def matchStats(URL):
    global playerTimeFilterLastMonthURL
    global pageIndividualPlayer
    global soupIndividualPlayer


    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    matchStats = soup.find_all("table", class_="stats-table")
    mapName=soup.find("div",class_="match-info-box").text.strip().split("\n")[2]

    team1Name = matchStats[0].find("th", class_="st-teamname").text
    team2Name = matchStats[3].find("th", class_="st-teamname").text

    playerURLS = getPlayerURLs(URL)
    playersTeam1 = []
    playersTeam2 = []
    for i in range(0, 5):
        player1 = Player(playerURLS[i])
        player1.setPlayerTeam(team1Name)
        playersTeam1.append(player1)

    for i in range(5, 10):
        player2 = Player(playerURLS[i])
        player2.setPlayerTeam(team2Name)
        playersTeam2.append(player2)


    playerStatsTeam1 = matchStats[0].find_all("tr")
    playerStatsTeam1.pop(0)
    for i in range(len(playerStatsTeam1)):
        # finds the score
        playerKills = playerStatsTeam1[i].find("td", class_="st-kills")
        if playerKills is not None:
            playersTeam1[i].setPlayerKills(playerKills.text)
        # finds the assists
        playerAssists = playerStatsTeam1[i].find("td", class_="st-assists")
        if playerAssists is not None:
            playersTeam1[i].setPlayerAssists(playerAssists.text)

        # finds the deaths
        playerDeaths = playerStatsTeam1[i].find("td", class_="st-deaths")
        if playerDeaths is not None:
            playersTeam1[i].setPlayerDeaths(playerDeaths.text)

    playerStatsTeam2 = matchStats[3].find_all("tr")
    playerStatsTeam2.pop(0)
    for i in range(len(playerStatsTeam2)):

        # finds the score
        playerKills = playerStatsTeam2[i].find("td", class_="st-kills")
        if playerKills is not None:
            playersTeam2[i].setPlayerKills(playerKills.text)

        # finds the assists
        playerAssists = playerStatsTeam2[i].find("td", class_="st-assists")
        if playerAssists is not None:
            playersTeam2[i].setPlayerAssists(playerAssists.text)

        # finds the deaths
        playerDeaths = playerStatsTeam2[i].find("td", class_="st-deaths")
        if playerDeaths is not None:
            playersTeam2[i].setPlayerDeaths(playerDeaths.text)

    # PRINTS ALL DETAILS
    print("*********************************")
    print("KDA STATS: ", team1Name, " vs ", team2Name)
    print("MAP: ", mapName)
    print("*********************************")

    print(team1Name)
    for i in range(len(playersTeam1)):
        print(f"{playersTeam1[i].getPlayerName()}: \n "
              f"  K(headshots): {playersTeam1[i].getPlayerKills()}  "
              f"  D: {playersTeam1[i].getPlayerDeaths()}"
              f"  A: {playersTeam1[i].getPlayerAssists()}"
              f"  EK: {playersTeam1[i].getPlayerEK()}")

    print("\n")
    print(team2Name)
    for i in range(len(playersTeam2)):
        print(f"{playersTeam2[i].getPlayerName()}: \n "
              f"  K(headshots): {playersTeam2[i].getPlayerKills()}  "
              f"  D: {playersTeam2[i].getPlayerDeaths()}"
              f"  A: {playersTeam2[i].getPlayerAssists()}"
              f"  EK: {playersTeam2[i].getPlayerEK()}")
    print("")
    print("#####################CLUTCHES#####################")
    getPlayersClutches(playersTeam1,playersTeam2)
    print("")
    print("#####################4ks#####################")
    print(team1Name)
    for player in playersTeam1:
        print(player.getPlayerName() + ": " + player.getMultiKills("4k"))
    print("\n")
    print(team2Name)
    for player in playersTeam2:
        print(player.getPlayerName() + ": " + player.getMultiKills("4k"))
    print("")
    print("#####################5ks#####################")
    print(team1Name)
    for player in playersTeam1:
        print(player.getPlayerName() + ": " + player.getMultiKills("5k"))
    print("\n")
    print(team2Name)
    for player in playersTeam2:
        print(player.getPlayerName() + ": " + player.getMultiKills("5k"))



# Return an array of player URL
def getPlayerURLs(URL):
    playerURLS = []
    soup = getSoup(URL)
    matchStats = soup.find_all("table", class_="stats-table")
    playerStatsTeam1 = matchStats[0].find_all("tr")
    playerStatsTeam2 = matchStats[3].find_all("tr")

    for playerStats in playerStatsTeam1 + playerStatsTeam2:
        # finds all names
        playerName = playerStats.find("a")
        if playerName is not None:
            playerURLS.append("https://www.hltv.org" + playerName.get("href"))

    return playerURLS

def appendClutchURLToPlayer(playersTeam1,playersTeam2,hltvURL,dateURL):
    for player in playersTeam1+playersTeam2:
        playerName = player.getPlayerName()
        playerID = player.getPlayerID()
        for i in range(2, 6):  # I only need 1v2 to 1v5 clutches
            url1vXClutch = hltvURL + str(playerID) + "/" + "1on" + str(i) + "/" + playerName + "?" + dateURL
            player.appendClutchURL(url1vXClutch)

def scrapeClutches(playersTeam1,playersTeam2):
    indexForTeamCheck =0 #
    for player in playersTeam1 +playersTeam2:
        clutchTypeNumber=2
        print("----------------------------")
        if indexForTeamCheck % 4 ==0:
            print(player.getPlayerTeam())
            indexForTeamCheck+=1
        else:
            print(player.getPlayerTeam())
        print(player.getPlayerName())
        for clutchURL in player.getClutchURLS():
            soup = getSoup(clutchURL)
            statsTable = soup.find("table", class_="stats-table")
            time.sleep(0.5)  # TIMEOUT TO NOT GET RATE LIMITED
            clutchMapName = statsTable.find_all("div", class_="dynamic-map-name-full")
            clutchRound = statsTable.find_all("td", class_="text-center")
            print(" 1v" + str(clutchTypeNumber))
            for i in range(len(clutchMapName)):
                if clutchMapName is None:
                    print("Map :" + "none")
                else:
                    print(" Map: ", clutchMapName[i].text, ",Round: ", clutchRound[i].text)
            clutchTypeNumber+=1

def scrapeClutchesForPlayers():
    pass

def getPlayersClutches(playersTeam1,playersTeam2):  # URL IS THE MATCH URL
    hltvURL = "https://www.hltv.org/stats/players/clutches/"
    dateURL="startDate=" + today.strftime("%Y-%m-%d")+"&"+"endDate=" + today.strftime("%Y-%m-%d")
    print(dateURL)
    #dateURLFake = "startDate=" + "2022-03-15" + "&" + "endDate=" + today.strftime("%Y-%m-%d")

    #   appends clutchURL to players. clutchURL is used in scrapeClutches
    appendClutchURLToPlayer(playersTeam1,playersTeam2,hltvURL,dateURL)

    #   BEGIN SCRAPING clutches
    scrapeClutches(playersTeam1,playersTeam2)


def getSoup(URLSpecific):
    page = requests.get(URLSpecific)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

'''
    *Monster method for scraping the Ek's the "original" way.. before HLTV Changed.
def getPlayersEks(URL):
    if URL.__contains__("mapstatsid"):
        matchID = URL.split("/")[6]
        matchTeams = URL.split("/")[7]
        URLEK="https://www.hltv.org/stats/matches/"+"performance/"+"mapstatsid/"+matchID+"/"+matchTeams
    else:
        matchID = URL.split("/")[5]
        matchTeams = URL.split("/")[6]
        URLEK="https://www.hltv.org/stats/matches/"+"performance/"+matchID+"/"+matchTeams

    #BEGIN SCRAPING
    page = requests.get(URLEK)
    soup = BeautifulSoup(page.content, "html.parser")
    killMatrixContent=soup.find("div",id="FIRST_KILL-content")
    rows=killMatrixContent.find_all("tr")
    playerNamesTeam1=[]
    playerNamesTeam2=[]
    Team1EKS=[]
    Team2EKS=[]
    Team1EKSNamesDict={}
    Team2EKSNamesDict={}
    allRowsResults=[]
    for i in range(1,len(rows)):
        PlayerEk=rows[i].find_all("td")
        for j in range(1,len(PlayerEk)):
            PlayerEKTeam1=PlayerEk[j].text.split(":")
            allRowsResults.append(PlayerEKTeam1)

    #appends names in order of the matrix from hltv.
    for player in killMatrixContent.find_all("td",class_="team2"): # THIS IS CORRECT
        playerNamesTeam1.append(player.text)
    for player in killMatrixContent.find_all("td",class_="team1"): # THIS IS CORRECT
        playerNamesTeam2.append(player.text)

    #Finds EK for all players from TEAM1. Total of 25 eks. Sum for every 5 objects is EKs for every other player.
    for row in range(0,len(allRowsResults)):
        for col in range(0,len(allRowsResults[row]),2):
            Team1EKS.append(allRowsResults[row][col])

    #Finds EK for all players from TEAM2. Total of 25 eks. Sum for every 5 objects is EKs for every other player.
    for row in range(0,len(allRowsResults)):
        for col in range(1,len(allRowsResults[row]),2):
            Team2EKS.append(allRowsResults[row][col])

    Team1EKSnew =[]
    #Makes a list consisting of tuples of 5, each matching eks of a player in order of the matrix.
    for i in range(0,len(Team1EKS),5):
        Team1EKSnew.append(Team1EKS[i:i+5])
    #converts from string to int
    for i in range(len(Team1EKSnew)):
        for j in range(len(Team1EKSnew[i])):
            Team1EKSnew[i][j]=int(Team1EKSnew[i][j])
    print("int Team1EKSNEW:",Team1EKSnew)
    #append  to dict [playerName: EK]
    for i in range(len(Team1EKSnew)) :
        Team1EKSNamesDict[playerNamesTeam1[i]]=sum(Team1EKSnew[i])

    #EKS for TEAM2
    Team2EKSOrderd=[]
    for i in range(0,5):
        for j in range(i,len(Team2EKS),5):
            Team2EKSOrderd.append(Team2EKS[j])

    Team2EKSnew =[]
    for i in range(0,len(Team2EKSOrderd),5):
        Team2EKSnew.append(Team2EKSOrderd[i:i+5])
    #converts from string to int
    for i in range(len(Team2EKSnew)):
        for j in range(len(Team2EKSnew[i])):
            Team2EKSnew[i][j]=int(Team2EKSnew[i][j])
    print("int Team2EKSNEW:",Team2EKSnew)
    #append  to dict [playerName: EK]
    for i in range(len(Team1EKSnew)) :
        Team2EKSNamesDict[playerNamesTeam2[i]]=sum(Team2EKSnew[i])


    print(Team1EKSNamesDict)
    print(Team2EKSNamesDict)

    return Team1EKSNamesDict,Team2EKSNamesDict'''



################### TESTING OMRÅDE ############################################
def  main():
    matchStats("https://www.hltv.org/stats/matches/93987/g2-vs-natus-vincere")
    # matchStats("https://www.hltv.org/stats/matches/mapstatsid/140861/natus-vincere-vs-faze")
    # getPlayersEks("https://www.hltv.org/stats/matches/mapstatsid/140861/natus-vincere-vs-faze")
    # matchStats("https://www.hltv.org/stats/matches/mapstatsid/149751/g2-vs-natus-vincere")
    #getPlayersEks("https://www.hltv.org/stats/matches/93987/g2-vs-natus-vincere")if __name__ == "__matchStats__":¨

if __name__ == "__main__":
    main()






