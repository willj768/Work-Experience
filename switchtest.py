#Switch ip: 10.1.10.24
#Switch Username: optiadmin

from netmiko import ConnectHandler

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

userInput = input("> ")
if userInput == "shutdown":
    shutdown()
elif userInput == "no shutdown":
    noShutdown()
