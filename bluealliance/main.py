import requests
import json
import os

os.system('rm *.json')

key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"

urls = {
  'teams' : 'https://www.thebluealliance.com/api/v3/event/2022nhgrs/teams',
  'matches' : 'https://www.thebluealliance.com/api/v3/event/2022nhgrs/matches',
  'team_151' : 'https://www.thebluealliance.com/api/v3/team/frc151/event/2022nhgrs/matches'
}

for url in urls:
  info = requests.get(urls[url], headers={"X-TBA-Auth-Key": key})

  with open(url + '.json', "w") as file:
    json.dump(info.json(), file, indent=2)