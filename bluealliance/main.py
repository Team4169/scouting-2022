import requests
import json
import os

os.system('rm *.json')

key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"

urls = {
  # 'file1' : 'https://www.thebluealliance.com/api/v3/team/frc4169/event/2019marea/matches',
  # 'file2' : 'https://www.thebluealliance.com/api/v3/event/2019marea/matches',
  # 'pregional' : 'https://www.thebluealliance.com/api/v3/event/2022ispr/matches',
  'week0' : 'https://www.thebluealliance.com/api/v3/event/2022week0/matches',
  'teams' : 'https://www.thebluealliance.com/api/v3/event/2022week0/teams'
  # 'allcomps' : 'https://www.thebluealliance.com/api/v3/events/2022'
}

for url in urls:
  info = requests.get(urls[url], headers={"X-TBA-Auth-Key": key})

  with open(url + '.json', "w") as file:
    json.dump(info.json(), file, indent=2)

  teams = 