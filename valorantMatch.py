from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

urlLastMatches = "https://api.tracker.gg/api/v2/valorant/standard/matches/riot/GutosiN%237984?type=competitive&season=&agent=all&map=all"
urlMatchInfo = "https://api.tracker.gg/api/v2/valorant/standard/matches/"

option = Options()
option.headless = True

class valorantMatch:

    def __init__(self):
        self.driver = webdriver.Chrome(options=option)
        with open('lastMatchId.json', 'r') as arquivo:
            self.jsonData = json.load(arquivo)

    def __del__(self):
        self.driver.quit()

    def __getLastMatchId(self):
        self.driver.get(urlLastMatches)
        time.sleep(3)
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
        time.sleep(1)
        matchInfos = self.driver.find_element("xpath", "//pre")
        dictionaryMatchesInfo = json.loads(matchInfos.text)
        sumSegments = len(dictionaryMatchesInfo['data']['segments'])
        playersInfo = dictionaryMatchesInfo['data']

        players = {}
        playersList = []
        playerIndividualInfo = {}

        for i in range(0, sumSegments):
            if playersInfo['segments'][i]['type'] == "player-summary":
                name = playersInfo['segments'][i]["attributes"]["platformUserIdentifier"]
                team = playersInfo['segments'][i]["attributes"]["platformUserIdentifier"]


        print(players)


