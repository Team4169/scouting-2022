import requests
import json
import os
import datetime
import pytz

os.system('rm *.json')

key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"

urls = {
  'da_matches' : 'https://www.thebluealliance.com/api/v3/team/frc4169/event/2022marea/matches',
  'rankings' : 'https://www.thebluealliance.com/api/v3/event/2022marea/rankings'
}

for url in urls:
  info = requests.get(urls[url], headers={"X-TBA-Auth-Key": key})

  with open(url + '.json', "w") as file:
    json.dump(info.json(), file, indent=2)

url = 'https://www.thebluealliance.com/api/v3/team/frc4169/event/2022marea/matches'
headers = {'X-TBA-Auth-Key': key}

r = requests.get(url, headers=headers)
matches = r.json()

url = 'https://www.thebluealliance.com/api/v3/event/2022marea/rankings'

r = requests.get(url, headers=headers)
rankings = r.json()

def rank(team):
  for i in rankings["rankings"]:
    if str(i['team_key']) == team:
      return str(i['rank'])
      break

def format(unix):
  unix = datetime.datetime.fromtimestamp(unix)
  return unix.astimezone(pytz.timezone('US/Eastern')).strftime("%H:%M:%S on %D")

def teammates(data, x):
  if x == True:
    return data["alliances"]["blue"]["team_keys"]
  else:
    return data["alliances"]["red"]["team_keys"]

matchinfo = []
for i in matches:
  if 'frc4169' in teammates(i, True):
    da_bois = teammates(i, True)
    poopyheads = teammates(i, False)
  else:
    da_bois = teammates(i, False)
    poopyheads = teammates(i, True)
  match_number = i["match_number"]
  time = format(i["predicted_time"])

  our_ranking = []
  their_ranking = []
  
  for i in range(len(da_bois)):
    our_ranking.append(rank(da_bois[i]))

  for i in range(len(poopyheads)):
    their_ranking.append(rank(poopyheads[i]))

  matchinfo.append([match_number, time, da_bois, our_ranking, poopyheads, their_ranking])

matchnumbers = []
for match in matchinfo:
  matchnumbers.append(match[0])
matchnumbers.sort()

matchinfosorted = []
for num in matchnumbers:
  for match in matchinfo:
    if match[0] == num:
      matchinfosorted.append(match)
      break

for match in matchinfosorted:
  print('Match: #' + str(match[0]))
  print('Round starts at', match[1])
  print('da bois:', match[2])
  print('Rankings:', match[3])
  print('los poopyheads:', match[4])
  print('Rankings:', match[5])
  print('-------------------------------------------------')