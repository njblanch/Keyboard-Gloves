from gpiozero import MCP3008
from time import sleep
import socket

# The following documentation was used to help create this script:
# https://gpiozero.readthedocs.io/en/stable/api_spi.html#analog-to-digital-converters-adc

# inp1 = MCP3008(channel=0, device=0)
inp1 = MCP3008(channel=0, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp2 = MCP3008(channel=1, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp3 = MCP3008(channel=2, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp4 = MCP3008(channel=3, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)
inp5 = MCP3008(channel=4, clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8)


while True:
    print(str(inp1.value) + "   " + str(inp2.value) + "   " + str(inp3.value) + "   " + str(inp4.value) + "   " + str(inp5.value))
    sleep(0.001)

