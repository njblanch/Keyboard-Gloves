# Keyboard-Gloves
### Skyler Heininger and Nathan Blanchard

The programs present within this repository are testing and final scripts. 


## Raspberry Pi Programs
The program titled "test2.py"
(while clearly not the first test.py file) was used rigorously for testing output of the MCP3008s. This 
displayed raw data to the user and if a certain potentiometer was hitting the threshold values. This code
was adapted in "inpTest2.py" (clearly also not the first of the inpTest.py iterations) to instead return 
binary if a potentiometer passed threshold. Additionally, inpTest2.py made the large jump of connecting to a
server, and sending the data. It turns out that the TCP socket connection used for this is much, much slower 
than the MCP3008 can return values, which is why inpTest2.py features a higher value to sleep upon each 
iteration of the while loop. Even still, multiple values can pile up in the TCP queue before it is sent to 
the server, causing concatenation of readouts. 

## Server Side Program
"blueServer.py" handles the inputs from inpTest2.py using the function "getState". This function takes a string input, 
splits the inputted string by commas, and returns a tuple of the first five inputs. This allows us to handle
concatenation of the readings in the TCP queue as we will only have one reading from each time the client 
sends over data. This data is also valid to be used within the "typeOutput" function, which takes the two 
tuples that were returned from running getState on inputs from each raspberry pi. TypeOutput then ____.
The TCP connection was handled in main, using the socket package and two different ports to accommodate 
two simultaneously-running socket connections. At any point, if a socket server fails, or any of the programs
are terminated, all the socket connections are closed and programs are terminated.