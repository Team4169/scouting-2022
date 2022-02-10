import requests
import json
import os

key = os.environ['bluealliencekey']

urls = {
  'file1' : 'https://www.thebluealliance.com/api/v3/team/frc4169/event/2019marea/matches',
  'file2' : 'https://www.thebluealliance.com/api/v3/event/2019marea/matches'
}

for url in urls:
  info = requests.get(urls[url], headers={"X-TBA-Auth-Key": key})

  json.dump(info.json(), open('blueallience/' + url + '.json', "w"), indent=2)