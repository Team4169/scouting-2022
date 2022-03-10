import json
import requests
import numpy as np

def pullInfo():

  """  
  height = 90
  for row in range(1,height+1):
    spaces = " "*(height-1)  #gets the spaces at the beginning
    hashTags = "#"*row #get the first hashtags
    hashTags2 = "#"*row #gets the last hashtags
    
    print(spaces + hashTags + "  " + hashTags2) #prints each row together
    
    height -= 1
  """

  key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"
  comp_teams = requests.get("https://www.thebluealliance.com/api/v3/event/2022nhgrs/teams", headers={"X-TBA-Auth-Key": key}).json()

  json.dump(comp_teams, open('calcfiles/comp_teams.json', 'w'), indent=2)

  teamnums = []
  teamname = []
  for team in comp_teams:
    teamnums.append(team['team_number'])
    teamname.append(team['nickname']) 

  teamscore = []

  for team in teamnums:
    teamscore.append(getPitScore(team))
  
  return teamnums, teamname, teamscore

def getStats(team):
  
  key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"
  team_stats = requests.get("https://www.thebluealliance.com/api/v3/team/frc" + str(team) + "/event/2022nhgrs/matches", headers={"X-TBA-Auth-Key": key}).json()
  json.dump(team_stats, open('calcfiles/team_' + str(team) + '.json', 'w'), indent=2)
  
  return team_stats
  
def getPitScore(team):
  stats = getStats(team)
  points = []
  for i, score in enumerate(stats):
    if 'frc' + str(team) in str(stats[i]["alliances"]["blue"]["team_keys"]):
      points.append(int(stats[i]["alliances"]["blue"]['score']))
    if 'frc' + str(team) in str(stats[i]["alliances"]["red"]["team_keys"]):
      points.append(int(stats[i]["alliances"]["red"]["score"]))

  return np.mean(points)