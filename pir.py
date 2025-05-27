from gpiozero import MotionSensor
from netmiko import ConnectHandler
import time
import datetime

now = datetime.datetime.now()

SLEEP_TIME = 30

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

while True:
    pir.wait_for_motion()
    print("Motion Detected: ",now.strftime("%Y-%m-%d %H:%M:%S"))
    noShutdown()
    time.sleep(SLEEP_TIME)
    pir.wait_for_no_motion()
    print("Shutting Switch Port: ",now.strftime("%Y-%m-%d %H:%M:%S"))
    shutdown()

#log actual time of event
#check initial state of wap
#add operational hours
#log events into csv file