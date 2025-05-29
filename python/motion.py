from gpiozero import MotionSensor
import time
from utils import logMotion, logPowerUsage
from cisco import noShutdown, shutdown, powerUsage

pir = MotionSensor(4)

SLEEP_TIME = 30
DEBOUNCE_TIME = 10
CARBON_INTENSITY_OF_ELECTRICITY = 0.124

lastMotionTime = None
portIsUp = False

def handleMotion(ciscoDevice, logData, powerData):
    global lastMotionTime, portIsUp
    nowTime = time.time()

    if lastMotionTime is None or (nowTime - lastMotionTime) > DEBOUNCE_TIME:
        logMotion(logData, "[MOTION DETECTED]")
        print("[MOTION DETECTED]")
        lastMotionTime = nowTime

    if not portIsUp:
        duration = noShutdown(ciscoDevice)
        time.sleep(5)
        power = powerUsage(ciscoDevice)
        if power is not None:
            logPowerUsage(powerData, duration, power, CARBON_INTENSITY_OF_ELECTRICITY)
        portIsUp = True

def handleNoMotion(ciscoDevice, logData):
    global lastMotionTime, portIsUp
    if portIsUp and lastMotionTime and (time.time() - lastMotionTime > SLEEP_TIME):
        logMotion(logData, "[SHUTTING DOWN]")
        print("[SHUTTING DOWN]")
        shutdown(ciscoDevice)
        portIsUp = False
        lastMotionTime = None