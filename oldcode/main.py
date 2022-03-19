import requests
import json
import os

os.system('rm *.json')

key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"

urls = {
  'matches' : 'https://www.thebluealliance.com/api/v3/event/2022marea/matches',
  'teams' : 'https://www.thebluealliance.com/api/v3/event/2022marea/teams',
  '4169' : 'https://www.thebluealliance.com/api/v3/team/frc4169/events'
}

for url in urls:
  info = requests.get(urls[url], headers={"X-TBA-Auth-Key": key})

  with open(url + '.json', "w") as file:
    json.dump(info.json(), file, indent=2)
