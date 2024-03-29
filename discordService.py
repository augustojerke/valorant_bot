class discordService:

   def formatDescription(self, match):

      tab = self.__getFormatTab(match)
      mapInfo = self.__getMapInfo(match)
      winText = self.__getWinText(match)
      scoreMatch = self.__getScoreMatch(match)
      duration = self.__formatMinutes(match)
      mvpPlayer = self.__getMvpPlayer(match)

      playerMvp = match["players"][mvpPlayer]
      
      return f'''
                  \n**{scoreMatch}**
                  \n**Mapa:** {mapInfo["map"]} 
                  \n**⏱Duração:** {duration:.0f} minutos
                  \n> MVP                  
                  ```⭐ {playerMvp["name"].split('#')[0]} - {playerMvp["kills"]}/{playerMvp["deaths"]}/{playerMvp["assists"]} - Score: {playerMvp["score"]}```                                 
                  > PLACAR DE JOGADORES
                  ```
                  {tab}
                  ```                     
                  '''
   
   def __getFormatTab(self, match):
      tabText = ""
      
      playersBlue = []
      playersRed = []

      for i in range(0,10):
         if match["players"][i]["team"] == "Blue":
            playersBlue.append(match["players"][i])
         else:
            playersRed.append(match["players"][i])
      
      playersRed = sorted(playersRed, key=lambda x: x["score"])
      playersBlue = sorted(playersBlue, key=lambda x: x["score"])
      playersBlue.reverse()
      playersRed.reverse()

      for i in range (0,5):
         tabText += f"\n{playersBlue[i]['kills']}/{playersBlue[i]['deaths']}/{playersBlue[i]['assists']} - {playersBlue[i]['name'].split('#')[0]}"
      
      tabText += "\n"

      for i in range (0,5):
         tabText += f"\n{playersRed[i]['kills']}/{playersRed[i]['deaths']}/{playersRed[i]['assists']} - {playersRed[i]['name'].split('#')[0]}"

      return tabText
   
   def __getMapInfo(self, match):
      mapInfo = {}
      mapInfo["duration"] = match["map"]["duration"]
      mapInfo["map"] = match["map"]["map"]
      return mapInfo

   def getMapImage(self, match): 
      return match["map"]["mapImage"]

   def __getWinText(self, match):
      if match["teams"][0]["teamColor"] == "blue" and match["teams"][0]["wasWon"]:
         return "VITÓRIA DO TIME AZUL"
      return "VITÓRIA DO TIME VERMELHO"

   def __getScoreMatch(self, match):
      if match["teams"][0]["teamColor"] == "blue":
         return f"🔵 AZUL {match['teams'][0]['score']} X {match['teams'][1]['score']} VERMELHO 🔴"
      return f"🔵 AZUL {match['teams'][1]['score']} X {match['teams'][0]['score']} VERMELHO 🔴"
   
   def __formatMinutes(self, match):
      return float(match["map"]["duration"]) / 60000
   
   def __getMvpPlayer(self, match):
      maxPlayer = 0
      maxPlayerValueScore = int(match["players"][0]["score"])
      for i in range(0,10):
         if int(match["players"][i]["score"]) > maxPlayerValueScore:
            maxPlayer = i
            maxPlayerValueScore = int(match["players"][i]["score"])

      return maxPlayer

   def getRatiosKdr(self, match):
    text = ""
    players = match["players"]
    players = sorted(players, key=lambda x: x["kdRatio"], reverse=True)

    for i in range(0, 5):
        text += f"{players[i]['kdRatio']:.2f} - {players[i]['name'].split('#')[0]}\n"
      
    return text
   
   def getRatiosHs(self, match):
    text = ""
    players = match["players"]
    players = sorted(players, key=lambda x: x["hs"], reverse=True)

    for i in range(0, 5):
        text += f"{players[i]['hs']:.0f}% - {players[i]['name'].split('#')[0]}\n"
      
    return text
   
   def getRatiosClutches(self, match):
    text = ""
    players = match["players"]
    players = sorted(players, key=lambda x: x["clutches"], reverse=True)

    for i in range(0, 5):
        if players[i]['clutches'] != 0:
         text += f"{players[i]['clutches']} - {players[i]['name'].split('#')[0]}\n"
      
    return text
   
   def getRatiosAdr(self, match):
    text = ""
    players = match["players"]
    players = sorted(players, key=lambda x: x["adr"], reverse=True)

    for i in range(0, 5):
      text += f"{players[i]['adr']} - {players[i]['name'].split('#')[0]}\n"
      
    return text
   
   def getRatiosScore(self, match):
    text = ""
    players = match["players"]
    players = sorted(players, key=lambda x: x["score"], reverse=True)

    for i in range(0, 5):
      text += f"{players[i]['score']} - {players[i]['name'].split('#')[0]}\n"
      
    return text
   
   def getRatiosKills(self, match):
    text = ""
    players = match["players"]
    players = sorted(players, key=lambda x: x["kills"], reverse=True)

    for i in range(0, 5):
      text += f"{players[i]['kills']} - {players[i]['name'].split('#')[0]}\n"
      
    return text



      

