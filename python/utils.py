import pandas as pd
import datetime

def importCSV(fileName):
    df = pd.read_csv(fileName)
    return df.values.tolist()

def exportCSV(data, fileName, columns):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(fileName, index=False)

def logPowerUsage(powerData, durationHours, power, CARBON_INTENSITY_OF_ELECTRICITY=0.124):
        now = datetime.datetime.now()
        carbonMass = power * durationHours * CARBON_INTENSITY_OF_ELECTRICITY * 1000
        powerData.append((now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), round(durationHours, 4), round(power, 4), round(carbonMass, 4)))
        exportCSV(powerData, "power.csv", ["Date", "Time", "Time Saved (h)", "Power (kW)", "Carbon (g)"])

def logMotion(logData, event):
    now = datetime.datetime.now()
    logData.append((event, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
    exportCSV(logData, "logs.csv", ["Event", "Date", "Time"])