import requests, json, math
key = "e895huOQC8MTwe7FquKed5VVelPk1ocpE0455a2mVUWViaRupTH8N1ZEGoUMW7eU"


def avg(l):
    return sum(l) / len(l)


def getTeams(match):
    url = "https://www.thebluealliance.com/api/v3/event/" + match + "/teams"
    headers = {'X-TBA-Auth-Key': key}
    r = requests.get(url, headers=headers)
    data = r.json()
    teams = []
    for d in data:
        teams.append({
            'name': d['nickname'],
            'number': d['team_number'],
        })

    return teams

def scoreFromMatchForTeam(pos, sb):
    climbIndex = {
        "None": 0,
        "Low": 1,
        "Mid": 2,
        "High": 3,
        "Traversal": 4
    }
    taxiIndex = {
        "Yes": 1,
        "No": 0
    }
    return {
        'auto_cargo': sb["autoCargoPoints"],
        "auto_taxi": taxiIndex[sb["taxiRobot" + str(pos + 1)]],
        "endgame": climbIndex[sb["endgameRobot" + str(pos + 1)]], # No climb: 0, low: 1, med: 2, high: 3 traversal: 4
        "teleop_cargo": sb["teleopCargoPoints"]
    }

def scoreTeam(team, matches):
    key = 'frc' + str(team["number"])
    data = []

    for match in matches:
        if key in match['alliances']['red']['team_keys']:
            pos = match['alliances']['red']['team_keys'].index(key)
            data.append(scoreFromMatchForTeam(pos, match['score_breakdown']['red']))
        elif key in match['alliances']['blue']['team_keys']:
            pos = match['alliances']['blue']['team_keys'].index(key)
            data.append(scoreFromMatchForTeam(pos, match['score_breakdown']['blue']))

    auto_cargo = []
    auto_taxi = []
    endgame = []
    teleop_cargo = []
    for d in data:
        auto_cargo.append(d['auto_cargo'])
        auto_taxi.append(d['auto_taxi'])
        endgame.append(d['endgame'])
        teleop_cargo.append(d['teleop_cargo'])

    auto_cargo = avg(auto_cargo) # Points earned from cargo during auto on average
    auto_taxi = avg(auto_taxi) # Average taxi score. 2 = moved every auto
    endgame = math.ceil(avg(endgame))
    teleop_cargo = avg(teleop_cargo)

    score = (auto_cargo * 0.75) + teleop_cargo + (5 * endgame)
    if auto_taxi < 1.75:
        score *= 0.75
    return round(score)


def scoreForTeams(t, match):
    teams = t
    url = "https://www.thebluealliance.com/api/v3/event/" + match + "/matches"
    headers = {'X-TBA-Auth-Key': key}
    r = requests.get(url, headers=headers)
    matches = r.json()

    for i in range(len(teams)):
        team = teams[i]
        teams[i]["score"] = scoreTeam(team, matches)
    return teams


def scrape(match):
    teams = getTeams(match)
    return scoreForTeams(teams, match)