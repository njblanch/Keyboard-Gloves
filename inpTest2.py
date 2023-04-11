from time import sleep
from gpiozero import MCP3008
import socket

T = .8
P = .8
M = .8
R = .8
PI = .8


serverMac = 
port = 50001

#inp1 = MCP3008(channel=0, device=0)
inp1 = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp2 = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp3 = MCP3008(channel=2, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp4 = MCP3008(channel=3, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp5 = MCP3008(channel=4, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverMac, port))
while 1:
    string1 = str(inp1.value) + "," + str(inp2.value) + "," + str(inp3.value) + "," + str(inp4.value) + "," + str(inp5.value) + ","
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
    text = str(string1)
    state = str(Tpress) + "," + str(Ppress) + "," + str(Mpress) + "," + str(Rpress) + "," + str(Pipress) + ","
    print(state)
    s.send(bytes(state, 'UTF-8'))
    sleep(.02)

