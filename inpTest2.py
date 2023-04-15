from time import sleep
from gpiozero import MCP3008
import socket

T = .8
P = .8
M = .8
R = .8
PI = .8

# The following documentation was used for the MCP3008 scripting:
# https://gpiozero.readthedocs.io/en/stable/api_spi.html#analog-to-digital-converters-adc

# For the Socket connection, the following guide was used:
# https://realpython.com/python-sockets/#multi-connection-client-and-server

# The mac address is simply a string of the IPV4 address of the devices WIFI chip
serverMac = 
port = 50001

# Initialize MCP3008 channels
inp1 = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp2 = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp3 = MCP3008(channel=2, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp4 = MCP3008(channel=3, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp5 = MCP3008(channel=4, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverMac, port))
while 1:
    # string1 is simply the string values, it can be ommitted in this iteration
    # Ommitting this hardly saves time, this is still incredibly fast and 
    # runs into queue concatenation.
    # string1 = str(inp1.value) + "," + str(inp2.value) + "," + str(inp3.value) + "," + str(inp4.value) + "," + str(inp5.value) + ","
    
    # If statements to determine a "press". Threshold values are found through testing
    # This takes some of the time burden off of the server side
    if inp1.value < T:
        Tpress = 1
    else:
        Tpress = 0

    if inp2.value < P:
        Ppress = 1
    else:
        Ppress = 0

    if inp3.value < M:
        Mpress = 1
    else:
        Mpress = 0

    if inp4.value < R:
        Rpress = 1
    else:
        Rpress = 0

    if inp5.value < PI:
        Pipress = 1
    else:
        Pipress = 0

    # print(string1)
    # text = str(string1)
    # The comma at the end is what handles the queue concatenation.
    # The function getState of blueServer.py will take only the first five values, 
    # after splitting by ",". Therefore, adding the comma will make concatenated values handled.
    state = str(Tpress) + "," + str(Ppress) + "," + str(Mpress) + "," + str(Rpress) + "," + str(Pipress) + ","
    print(state)
    s.send(bytes(state, 'UTF-8'))
    sleep(.02)

