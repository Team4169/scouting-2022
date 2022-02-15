from flask import Flask, render_template, request
import calculator
import sqlite3
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadteam', methods=['POST'])
def uploadteam():
    score = calculator.getPitScore(request.form.to_dict())
    num = request.form.get('team-number')
    db = sqlite3.connect('db.sqlite3')
    res = db.execute("SELECT * FROM team WHERE team_number = ?", (num,))
    print(res)
    return "ok"

if __name__ == '__main__':
    app.run()