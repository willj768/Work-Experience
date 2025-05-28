from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

def importCSV():
    df = pd.read_csv("power.csv")
    return df.values.tolist()

@app.route("/api/powerTable")
def powerAPI():
    powerData = importCSV()
    return jsonify(powerData)

@app.route("/")
def home():
    powerData = importCSV()
    return render_template("script.html", powerTable=powerData)

if __name__ == "__main__":
    app.run(debug=True)
