from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

def importCSV():
    df = pd.read_csv("power.csv")
    totalCarbon = df["Carbon (g)"].sum()
    totalTime = df["Time Saved (h)"].sum()
    meanPower = df["Power (kW)"].mean()
    totalCarbon = round(totalCarbon, 4)
    totalTime = round(totalTime, 4)
    meanPower = round(meanPower, 4)
    return df.values.tolist(), totalCarbon, totalTime, meanPower

@app.route("/api/powerTable")
def powerAPI():
    powerData, totalCarbon, totalTime, meanPower = importCSV()
    return jsonify(powerData, totalCarbon, totalTime, meanPower)

@app.route("/")
def home():
    powerData, totalCarbon, totalTime, meanPower = importCSV()
    return render_template("script.html", powerTable=powerData, totalCarbon=totalCarbon, totalTime=totalTime, meanPower=meanPower)

if __name__ == "__main__":
    app.run(debug=True)
    