from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
import time
import json

urlLastMatches = "https://api.tracker.gg/api/v2/valorant/standard/matches/riot/GutosiN%237984?type=competitive&season=&agent=all&map=all"
urlMatchInfo = "https://api.tracker.gg/api/v2/valorant/standard/matches/"


opt = FirefoxOptions()
opt.add_argument("--headless")
opt.binary_location = '/geckodriver-v0.34.0-win32/geckodriver'

class valorantMatch:

    def __init__(self):
        self.driver = webdriver.Firefox(options=opt)
        with open('lastMatchId.json', 'r') as arquivo:
            self.jsonData = json.load(arquivo)

    def __del__(self):
        self.driver.quit()

    def __getLastMatchId(self):
        self.driver.get(urlLastMatches)
        time.sleep(3)
        jsonDataPageButton = self.driver.find_element("xpath", "//nav[@class='tabs-navigation']//ul//li[2]")
        jsonDataPageButton.click()
        jsonDataPage = self.driver.find_element("xpath", "//pre")
        dictionaryMatches = json.loads(jsonDataPage.text)
        return dictionaryMatches['data']['matches'][0]['attributes']['id']
    
    def isLastMatchNew(self):              
        lastMatchSaved = self.jsonData["lastMatchId"]
        lastMatchNow = self.__getLastMatchId()
        if str(lastMatchSaved) != str(lastMatchNow):
            self.__saveLastMatch(str(lastMatchNow))
            return True
        return False
    
    def __saveLastMatch(self, lastMatchId):
        self.jsonData["lastMatchId"] = lastMatchId
        with open('lastMatchId.json', 'w') as arquivo:
            json.dump(self.jsonData, arquivo)

    def __getLastMatchSaved(self):
        return self.jsonData["lastMatchId"]

    def getMatchInfo(self):
        url = urlMatchInfo + str(self.__getLastMatchSaved())
        self.driver.get(url)
        time.sleep(3)
        jsonDataPageButton = self.driver.find_element("xpath", "//nav[@class='tabs-navigation']//ul//li[2]")
        jsonDataPageButton.click()
        matchInfos = self.driver.find_element("xpath", "//pre")
        dictionaryMatchesInfo = json.loads(matchInfos.text)
        sumSegments = len(dictionaryMatchesInfo['data']['segments'])
        playersInfo = dictionaryMatchesInfo['data']

        matchSummary = {}

        playersList = []
        for i in range(0, sumSegments):
            if playersInfo['segments'][i]['type'] == "player-summary":
                playerIndividualInfo = {}
                playerIndividualInfo = self.__setPlayersValues(playersInfo, i)                
                playersList.append(playerIndividualInfo)

        matchSummary["players"] = playersList

        teamsList = []
        for i in range (0, 2):
            teamsInfo = {}
            teamsInfo = self.__setTeamsValues(playersInfo, i)
            teamsList.append(teamsInfo)
        
        matchSummary["teams"] = teamsList

        mapInfo = {}
        mapInfo["map"] = playersInfo["metadata"]["mapName"]
        mapInfo["mapImage"] = playersInfo["metadata"]["mapImageUrl"]
        mapInfo["duration"] = playersInfo["metadata"]["duration"]

        matchSummary["map"] = mapInfo

        return matchSummary
    
    def __setPlayersValues(self, playersInfo, index):
        playerIndividualInfo = {}
        name = playersInfo['segments'][index]["attributes"]["platformUserIdentifier"]
        team = playersInfo['segments'][index]["metadata"]["teamId"]
        agent = playersInfo['segments'][index]["metadata"]["agentName"]
        kills = playersInfo['segments'][index]["stats"]["kills"]["value"]
        deaths = playersInfo['segments'][index]["stats"]["deaths"]["value"]
        assists = playersInfo['segments'][index]["stats"]["assists"]["value"]
        kdRatio = float(playersInfo['segments'][index]["stats"]["kdRatio"]["value"])
        adr = float(playersInfo['segments'][index]["stats"]["damagePerRound"]["displayValue"])
        hs = playersInfo['segments'][index]["stats"]["hsAccuracy"]["value"]
        clutches = int(playersInfo['segments'][index]["stats"]["clutches"]["value"])
        score = int(playersInfo['segments'][index]["stats"]["scorePerRound"]["displayValue"])
        playerIndividualInfo["name"] = name
        playerIndividualInfo["team"] = team
        playerIndividualInfo["agent"] = agent
        playerIndividualInfo["kills"] = kills
        playerIndividualInfo["deaths"] = deaths
        playerIndividualInfo["assists"] = assists
        playerIndividualInfo["kdRatio"] = kdRatio
        playerIndividualInfo["adr"] = adr
        playerIndividualInfo["hs"] = hs
        playerIndividualInfo["clutches"] = clutches
        playerIndividualInfo["score"] = score
        return playerIndividualInfo
    
    def __setTeamsValues(self, teamsInfo, index):
        teamsNewInfo = {}
        teamColor = teamsInfo['segments'][index]["attributes"]["teamId"]
        hasWon = teamsInfo['segments'][index]["metadata"]["hasWon"]
        score = teamsInfo['segments'][index]["stats"]["roundsWon"]["value"]
        teamsNewInfo["teamColor"] = teamColor
        teamsNewInfo["hasWon"] = hasWon
        teamsNewInfo["score"] = score

        return teamsNewInfo




