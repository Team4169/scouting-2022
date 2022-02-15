from flask import Flask, render_template, request
import calculator
import sqlite3
from tabulate import tabulate

app = Flask(__name__)
dataTable=[["test", "test", "test", "test", "test"]]

@app.route('/')
def index():
    example = "INSERT INTO teams VALUES{}".format("(" + ",".join(dataTable[0]) + ")")
    print(example)
    return render_template('index.html', table_html=tabulate(dataTable, tablefmt='html'))


@app.route('/uploadteam', methods=['POST'])
def uploadteam():
    score = calculator.getPitScore(request.form.to_dict())
    num = request.form.get('team-number')
    db = sqlite3.connect('db.sqlite3')
    example = "INSERT INTO teams VALUES{}".format("(" + ",".join(dataTable[0]) + ")")
    print(example)
    res = db.execute("SELECT * FROM teams ORDER BY number", (num, ))
    print(res)
    return "ok"

@app.route('/upload', methods=['GET','POST'])
def upload():
  if request.method == 'POST':
    form = request.form
    dataTable.append([form.get("number"), form.get("name"), form.get("match"), form.get("pit"), form.get("comment")])
    print(dataTable)
    return render_template('index.html', table_html=tabulate(dataTable, tablefmt='html'))
  else:
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
