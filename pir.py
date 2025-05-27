from gpiozero import MotionSensor
from netmiko import ConnectHandler
import time
import datetime

SLEEP_TIME = 30
DEBOUNCE_TIME = 10

def shutdown():
    ciscoDevice = {
        'device_type': 'cisco_ios',
        'ip': '10.1.10.24',
        'username': 'optiadmin',
        'password': 'optiadmin',
        'port': 22,
        'secret': 'optiadmin',
    }

    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    commands = ['interface gigabitethernet 1/0/25', 'shutdown']
    connection.send_config_set(commands)

    connection.disconnect()

def noShutdown():
    ciscoDevice = {
        'device_type': 'cisco_ios',
        'ip': '10.1.10.24',
        'username': 'optiadmin',
        'password': 'optiadmin',
        'port': 22,
        'secret': 'optiadmin',
    }

    connection = ConnectHandler(**ciscoDevice)
    connection.enable()

    commands = ['interface gigabitethernet 1/0/25', 'no shutdown']
    connection.send_config_set(commands)

    connection.disconnect()

pir = MotionSensor(4)
lastMotionTime = None
portIsUp = False

while True:
    if pir.motion_detected:
        nowTime = time.time()

        if lastMotionTime is None or (nowTime - lastMotionTime) > DEBOUNCE_TIME:
            now = datetime.datetime.now()
            print("[MOTION DETECTED]:", now.strftime("%Y-%m-%d %H:%M:%S"))
            lastMotionTime = nowTime

        if not portIsUp:
            noShutdown()
            portIsUp = True
    else:
        if portIsUp and lastMotionTime is not None:
            if (time.time() - lastMotionTime) > SLEEP_TIME:
                now = datetime.datetime.now()
                print("[SHUTTING] no activity detected for 30 seconds:", now.strftime("%Y-%m-%d %H:%M:%S"))
                shutdown()
                portIsUp = False
                lastMotionTime = None

    time.sleep(1)

#log actual time of event
#check initial state of wap
#add operational hours
#log events into csv file