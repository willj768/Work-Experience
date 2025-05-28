from gpiozero import MotionSensor
from netmiko import ConnectHandler
import time
import datetime

SLEEP_TIME = 30
DEBOUNCE_TIME = 10

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

def shutdown(ciscoDevice):
    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    commands = ['interface gigabitethernet 1/0/25', 'shutdown']
    connection.send_config_set(commands)

    connection.disconnect()

def noShutdown(ciscoDevice):
    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    commands = ['interface gigabitethernet 1/0/25', 'no shutdown']
    connection.send_config_set(commands)

    connection.disconnect()

def handleMotion():
    global lastMotionTime, portIsUp
    nowTime = time.time()

    if lastMotionTime is None or (nowTime - lastMotionTime) > DEBOUNCE_TIME:
        now = datetime.datetime.now()
        print("[MOTION DETECTED]:", now.strftime("%Y-%m-%d %H:%M:%S"))
        lastMotionTime = nowTime

    if not portIsUp:
        noShutdown(ciscoDevice)
        portIsUp = True

def handleNoMotion():
    global lastMotionTime, portIsUp

    if portIsUp and lastMotionTime is not None:
        if (time.time() - lastMotionTime) > SLEEP_TIME:
            now = datetime.datetime.now()
            print("[SHUTTING] no activity detected for 30 seconds:", now.strftime("%Y-%m-%d %H:%M:%S"))
            shutdown(ciscoDevice)
            portIsUp = False
            lastMotionTime = None        

def motionLoop():
    while True:
        if pir.motion_detected:
            handleMotion()
        else:
            handleNoMotion()
        time.sleep(1)

def monitorTimes():
    now = datetime.datetime.now()
    return now.hour < 6 or now.hour > 20
    #return now.hour > 0
    
if __name__ == "__main__":
    if monitorTimes():
        motionLoop()
    else:
        noShutdown(ciscoDevice)

#log actual time of event
#add operational hours
#log events into csv file
#calculate power saved and carbon footprint
#add more ports