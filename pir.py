from gpiozero import MotionSensor
from netmiko import ConnectHandler
import time
import datetime
import pandas as pd
import re

SLEEP_TIME = 30
DEBOUNCE_TIME = 10
CARBON_INTENSITY_OF_ELECTRICITY = 0.124

logData = []
totalShutdownTime = 0
portShutdownTime = None

ciscoDevice = {
        'device_type': 'cisco_ios',
        'ip': '10.1.10.24',
        'username': 'optiadmin',
        'password': 'optiadmin',
        'port': 22,
        'secret': 'optiadmin',
    }

pir = MotionSensor(4)
lastMotionTime = None
portIsUp = False
portShutdownTime = None

def isPortUp(ciscoDevice):
    connection = ConnectHandler(**ciscoDevice)
    connection.enable()
    command = 'show interfaces gigabitethernet 1/0/25 status'
    output = connection.send_command(command)
    connection.disconnect()

    if re.search(r'Gi1/0/25\s+connected', output, re.IGNORECASE):
        return True
    else:
        return False

def shutdown(ciscoDevice):
    global portShutdownTime

    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    commands = ['interface gigabitethernet 1/0/25', 'shutdown']
    connection.send_config_set(commands)

    connection.disconnect()

    portShutdownTime = time.time()

def noShutdown(ciscoDevice):
    global portShutdownTime

    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    commands = ['interface gigabitethernet 1/0/25', 'no shutdown']
    connection.send_config_set(commands)

    duration = 0
    if portShutdownTime:
        duration = time.time() - portShutdownTime
        portShutdownTime = None

    durationHours = duration / 3600

    connection.disconnect()

    return durationHours

def powerUsage(ciscoDevice):

    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    command = 'show power inline Gi1/0/25 detail'
    powerData = connection.send_command(command)
    connection.disconnect()

    match = re.search(r'Measured at the port:\s+([\d.]+)', powerData)
    if match:
        power = (float(match.group(1))) / 1000
        return power 
    else:
        print("[ERROR] Measured Power not found")
        return None

def handleMotion(logData):
    global lastMotionTime, portIsUp
    nowTime = time.time()

    if lastMotionTime is None or (nowTime - lastMotionTime) > DEBOUNCE_TIME:
        now = datetime.datetime.now()
        logData.append(("MOTION DETECTED", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
        print("[MOTION DETECTED]:", now.strftime("%Y-%m-%d %H:%M:%S"))
        lastMotionTime = nowTime

    if not portIsUp:
        durationHours = noShutdown(ciscoDevice)
        time.sleep(5)  
        power = powerUsage(ciscoDevice)        
        if power is not None:
            logPowerUsage(powerData, durationHours, power, CARBON_INTENSITY_OF_ELECTRICITY)
        else:
            print("[ERROR] Failed to read power after port is back up. Skipping logging.")

        portIsUp = True

    logMotion(logData)

def handleNoMotion(logData):
    global lastMotionTime, portIsUp

    if portIsUp and lastMotionTime is not None:
        if (time.time() - lastMotionTime) > SLEEP_TIME:
            now = datetime.datetime.now()
            logData.append(("SHUTTING DOWN", now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
            print("[SHUTTING] no activity detected for 30 seconds:", now.strftime("%Y-%m-%d %H:%M:%S"))

            shutdown(ciscoDevice)
            portIsUp = False
            lastMotionTime = None 

    logMotion(logData)       

def motionLoop():
    while True:
        if monitorTimes():
            if pir.motion_detected:
                handleMotion(logData)
            else:
                handleNoMotion(logData)
        time.sleep(1)

def monitorTimes():
    now = datetime.datetime.now()
    weekday = now.weekday()
    hour = now.hour
    #return hour < 6 or hour > 20, weekday >= 5
    return hour > 0
    #return weekday <= 5

def logMotion(logData):
    df = pd.DataFrame(logData, columns=["Event","Date", "Time"])
    outputFile = "logs.csv"
    df.to_csv(outputFile, index=False)

def logPowerUsage(powerData, durationHours, power, CARBON_INTENSITY_OF_ELECTRICITY):
    carbonMass = power * durationHours * CARBON_INTENSITY_OF_ELECTRICITY

    powerData.append((round(durationHours, 4), round(power, 4), round(carbonMass*1000, 4)))

    df = pd.DataFrame(powerData, columns=["Time (h)", "Power (kW)", "Carbon (g)"])
    outputFile = "power.csv"
    df.to_csv(outputFile, index=False)

def importCSV():
    df = pd.read_csv("power.csv")
    powerData = df.values.tolist()
    return powerData
    
if __name__ == "__main__":
    powerData = importCSV()
    portIsUp = isPortUp(ciscoDevice)
    if portIsUp:
        lastMotionTime = time.time()
    else:
        lastMotionTime = None
    if monitorTimes():
        motionLoop()
    else:
        noShutdown(ciscoDevice)
        motionLoop()
