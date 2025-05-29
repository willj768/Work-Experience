from flask import Flask, render_template, jsonify, request
import pandas as pd
import math

app = Flask(__name__, template_folder="../templates", static_folder="../static")
LOGS_PER_PAGE = 15

def importCSV():
    df = pd.read_csv("power.csv")
    totalCarbon = df["Carbon (g)"].sum()
    totalTime = df["Time Saved (h)"].sum()
    meanPower = df["Power (kW)"].mean()
    totalCarbon = round(totalCarbon, 4)
    totalTime = round(totalTime, 4)
    meanPower = round(meanPower, 4)
    return df, totalCarbon, totalTime, meanPower

@app.route("/api/powerTable")
def powerAPI():
    df, totalCarbon, totalTime, meanPower = importCSV()
    return jsonify(df, totalCarbon, totalTime, meanPower)

@app.route("/")
def home():
    page = request.args.get("page", default=1, type=int)
    df, totalCarbon, totalTime, meanPower = importCSV()

    totalEntries = len(df)
    totalPages = math.ceil(totalEntries / LOGS_PER_PAGE)

    start = (page - 1) * LOGS_PER_PAGE
    end = start + LOGS_PER_PAGE
    pageData = df.iloc[start:end].values.tolist()

    return render_template("script.html", powerTable=pageData, totalCarbon=totalCarbon, totalTime=totalTime, meanPower=meanPower, currentPage=page, totalPages=totalPages)

if __name__ == "__main__":
    app.run(debug=True)
    