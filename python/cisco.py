from netmiko import ConnectHandler
import re
import time

portShutdownTime = None

def connect(ciscoDevice):
    connection = ConnectHandler(**ciscoDevice)
    connection.enable()
    return connection

def isPortUp(ciscoDevice):
    connection = connect(ciscoDevice)
    output = connection.send_command('show interfaces gigabitethernet 1/0/25 status')
    connection.disconnect()
    return bool(re.search(r'Gi1/0/25\s+connected', output, re.IGNORECASE))

def shutdown(ciscoDevice):
    global portShutdownTime
    connection = connect(ciscoDevice)
    connection.send_config_set(['interface gigabitethernet 1/0/25', 'shutdown'])
    connection.disconnect()
    portShutdownTime = time.time()

def noShutdown(ciscoDevice):
    global portShutdownTime
    connection = connect(ciscoDevice)
    connection.send_config_set(['interface gigabitethernet 1/0/25', 'no shutdown'])
    connection.disconnect()
    
    if portShutdownTime:
        duration = time.time() - portShutdownTime
        portShutdownTime = None
        return duration / 3600
    return 0

def powerUsage(ciscoDevice):
    connection = connect(ciscoDevice)
    output = connection.send_command('show power inline Gi1/0/25 detail')
    connection.disconnect()
    match = re.search(r'Measured at the port:\s*([\d.]+)', output)
    return float(match.group(1)) / 1000 if match else None