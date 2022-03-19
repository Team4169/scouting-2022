from flask import Flask, render_template, request, redirect
import sqlite3
from scrape import scrape
import json

app = Flask(__name__)

# test matches: 2022nhgrs, 2022ctwat, 2022melew
MATCH = "2022nhgrs"

@app.route('/')
def index():
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    teams = cur.execute("SELECT name,number,pscore,mscore, comments, pscore+mscore AS tscore FROM teams ORDER BY tscore DESC").fetchall()
    cur.close()
    data = []
    i = 1
    for team in teams:
        data.append({
            'name': team[0],
            'number': team[1],
            'pit': team[2],
            'match': team[3],
            'comments': team[4],
            'rank': i,
        })
        i+=1

    print(teams)
    return render_template('index.html', data=data)

@app.route('/pull', methods=['GET'])
def pull():
    teams = scrape(MATCH)
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    for team in teams:
        if cur.execute("SELECT COUNT(*) FROM teams WHERE number=?", (team['number'],)).fetchone()[0] > 0:
            cur.execute("UPDATE teams SET mscore=?, name=? WHERE number=?", (team['score'], team["name"], team['number']))
        else:
            cur.execute("INSERT INTO teams (name, number, mscore) VALUES (?,?,?)", (team['name'], team['number'], team['score']))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    data = json.loads(request.form.to_dict().keys()[0])
    num = data['number']
    score = data['score']
    comments = data['comments']
    # num = request.form.get('number')
    # score = request.form.get('score')
    # comments = request.form.get('comments')
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    if cur.execute("SELECT COUNT(*) FROM teams WHERE number=?", (num,)).fetchone()[0] > 0:
        cur.execute("UPDATE teams SET pscore=?, comments=? WHERE number=?", (score, comments, num))
    else:
        cur.execute("INSERT INTO teams (number, pscore, comments) VALUES (?,?,?)", (num, score, comments))
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)