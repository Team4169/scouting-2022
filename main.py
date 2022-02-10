import requests
import json
import os

key = os.environ['bluealliencekey']

info = requests.get('https://www.thebluealliance.com/api/v3/team/frc4169/awards', headers={"X-TBA-Auth-Key": key})

json.dump(info.json(), open("blueallience/info.json", "w"), indent=2)