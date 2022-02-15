import requests
import json

key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"

info = requests.get('https://www.thebluealliance.com/api/v3/team/frc4169/awards', headers={"X-TBA-Auth-Key": key})

json.dump(info.json(), open("blueallience/info.json", "w"), indent=2)