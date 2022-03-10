from flask import Flask, render_template, request, redirect
import calculator, bluealliance
import sqlite3
#from tabulate import tabulate

app = Flask(__name__)

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
    num, name = bluealliance.pullInfo()
    return redirect('/')


@app.route('/upload', methods=['POST'])
def upload():
    num = request.form.get('number')
    name = request.form.get('name')
    score = request.form.get('score')
    comments = request.form.get('comments')
    db = sqlite3.connect('db.sqlite3')
    cur = db.cursor()
    if cur.execute("SELECT COUNT(*) FROM teams WHERE number=?", (num,)).fetchone()[0] == 0:
        cur.execute("INSERT INTO teams (name, number, pscore, comments) VALUES (?,?,?,?,?)", (name, num, score, comments))
    else:
        cur.execute("UPDATE teams SET pscore=?, comments=? WHERE number=?", (score, comments, num))
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
