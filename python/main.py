from config import loadDetails
from utils import importCSV
from cisco import isPortUp, noShutdown
from motion import handleMotion, handleNoMotion, pir
import time
import datetime

def monitorTimes():
    now = datetime.datetime.now()
    weekday = now.weekday()
    hour = now.hour
    """if weekday >= 5:
        return True
    elif hour < 6 or hour > 20:
        return True
    else:
        return False"""
    return True

def motionLoop(ciscoDevice, logData, powerData):
    while True:
        if monitorTimes():
            if pir.motion_detected:
                handleMotion(ciscoDevice, logData, powerData)
            else:
                handleNoMotion(ciscoDevice, logData)
            time.sleep(1)

if __name__ == "__main__":
    username, password, secret = loadDetails()
    ciscoDevice = {
        'device_type': 'cisco_ios',
        'ip': '10.1.10.24',
        'username': username,
        'password': password,
        'port': 22,
        'secret': secret,
    }

    logData = importCSV("logs.csv")
    powerData = importCSV("power.csv")

    from motion import lastMotionTime, portIsUp
    portIsUp = isPortUp(ciscoDevice)
    if portIsUp:
        lastMotionTime = time.time()

    motionLoop(ciscoDevice, logData, powerData)