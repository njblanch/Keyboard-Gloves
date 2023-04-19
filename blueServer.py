import socket
import pyautogui

# All socket server scripting is taken from this guide:
# https://realpython.com/python-sockets/#multi-connection-client-and-server

# Left hand is port 50001, Right hand 50002
port1 = 50001
port2 = 50002
# Mac address is the IPV4 wifi address of the host computer. 
macAddress = ""
backlog = 5
size = 1024

# Values for neutral, down
NEUTRAL = 0
PRESS = 1

# Dictionary for determining output
keyDict = {"0,0,1,0,0," + "0,1,0,0,0,": "'", "0,0,1,0,0," + "0,0,1,0,0,": ",", "0,0,1,0,0," + "0,0,0,1,0,": ".",
           "0,0,1,0,1," + "0,1,0,0,0,": "\"", "0,0,1,0,1," + "0,0,1,0,0,": "(", "0,0,1,0,1," + "0,0,0,1,0,": ")", "0,0,1,0,1," + "0,0,0,0,1,": ":",
           "1,0,0,0,0," + "0,1,0,0,0,": "q", "1,0,0,0,0," + "0,0,1,0,0,": "w", "1,0,0,0,0," + "0,0,0,1,0,": "e", "1,0,0,0,0," + "0,0,0,0,1,": "r",
           "1,1,0,0,0," + "0,1,0,0,0,": "a", "1,1,0,0,0," + "0,0,1,0,0,": "s", "1,1,0,0,0," + "0,0,0,1,0,": "d", "1,1,0,0,0," + "0,0,0,0,1,": "f",
           "1,1,1,0,0," + "0,1,0,0,0,": "z", "1,1,1,0,0," + "0,0,1,0,0,": "x", "1,1,1,0,0," + "0,0,0,1,0,": "c", "1,1,1,0,0," + "0,0,0,0,1,": "v",
           "0,0,0,1,0," + "0,1,0,0,0,": "u", "0,0,0,1,0," + "0,0,1,0,0,": "i", "0,0,0,1,0," + "0,0,0,1,0,": "o", "0,0,0,1,0," + "0,0,0,0,1,": "p",
           "0,0,1,1,0," + "0,1,0,0,0,": "j", "0,0,1,1,0," + "0,0,1,0,0,": "k", "0,0,1,1,0," + "0,0,0,1,0,": "l", "0,0,1,1,0," + "0,0,0,0,1,": ";",
           "0,1,1,1,0," + "0,1,0,0,0,": "b", "0,1,1,1,0," + "0,0,1,0,0,": "n", "0,1,1,1,0," + "0,0,0,1,0,": "m", "0,1,1,1,0," + "0,0,0,0,1,": "/",
           "0,1,1,0,0," + "0,1,0,0,0,": "t", "0,1,1,0,0," + "0,0,1,0,0,": "g", "0,1,1,0,0," + "0,0,0,1,0,": "y", "0,1,1,0,0," + "0,0,0,0,1,": "h",
           "1,0,0,0,1," + "0,1,0,0,0,": "Q", "1,0,0,0,1," + "0,0,1,0,0,": "W", "1,0,0,0,1," + "0,0,0,1,0,": "E", "1,0,0,0,1," + "0,0,0,0,1,": "R",
           "1,1,0,0,1," + "0,1,0,0,0,": "A", "1,1,0,0,1," + "0,0,1,0,0,": "S", "1,1,0,0,1," + "0,0,0,1,0,": "D", "1,1,0,0,1," + "0,0,0,0,1,": "F",
           "1,1,1,0,1," + "0,1,0,0,0,": "Z", "1,1,1,0,1," + "0,0,1,0,0,": "X", "1,1,1,0,1," + "0,0,0,1,0,": "C", "1,1,1,0,1," + "0,0,0,0,1,": "V",
           "0,0,0,1,1," + "0,1,0,0,0,": "U", "0,0,0,1,1," + "0,0,1,0,0,": "I", "0,0,0,1,1," + "0,0,0,1,0,": "O", "0,0,0,1,1," + "0,0,0,0,1,": "P",
           "0,0,1,1,1," + "0,1,0,0,0,": "J", "0,0,1,1,1," + "0,0,1,0,0,": "K", "0,0,1,1,1," + "0,0,0,1,0,": "L", "0,0,1,1,1," + "0,0,0,0,1,": "!",
           "0,1,1,1,1," + "0,1,0,0,0,": "B", "0,1,1,1,1," + "0,0,1,0,0,": "N", "0,1,1,1,1," + "0,0,0,1,0,": "M", "0,1,1,1,1," + "0,0,0,0,1,": "?",
           "0,1,1,0,1," + "0,1,0,0,0,": "T", "0,1,1,0,1," + "0,0,1,0,0,": "G", "0,1,1,0,1," + "0,0,0,1,0,": "Y", "0,1,1,0,1," + "0,0,0,0,1,": "H",
           "0,1,0,0,0," + "0,1,0,0,0,": "0", "0,1,0,0,0," + "0,0,1,0,0,": "1", "0,1,0,0,0," + "0,0,0,1,0,": "+", "0,1,0,0,0," + "0,0,0,0,1,": "-",
           "1,0,0,1,0," + "0,1,0,0,0,": "2", "1,0,0,1,0," + "0,0,1,0,0,": "3", "1,0,0,1,0," + "0,0,0,1,0,": "4", "1,0,0,1,0," + "0,0,0,0,1,": "5",
           "1,0,0,1,1," + "0,1,0,0,0,": "6", "1,0,0,1,1," + "0,0,1,0,0,": "7", "1,0,0,1,1," + "0,0,0,1,0,": "8", "1,0,0,1,1," + "0,0,0,0,1,": "9"}

# Use these threshold values to create states (aka finger positions)
# When these positions change, then take an input, or nothing if neutral
def getState(stringPos):
    stringPos = stringPos.split(",")
    # sometimes the socket will send more than one set of states at once
    # This can still be accepted since this will only take the first set of
    # inputs of that string, not the whole thing

    # print(stringPos)
    tPos = float(stringPos[0])
    pPos = float(stringPos[1])
    mPos = float(stringPos[2])
    rPos = float(stringPos[3])
    piPos = float(stringPos[4])
    return tPos, pPos, mPos, rPos, piPos


# typeOutput simply takes in the data of the right and left hands,
# and then determines what to type.
def typeOutput(key):
    try:
        if key[10] == "1":
            if key[8] == "0":
                pyautogui.write(" ")
                return
            else:
                pyautogui.press("backspace")
                return
        elif key == "0,0,1,0,0,0,0,0,0,1,":
            pyautogui.press("enter")
        else:
            pyautogui.write(keyDict.get(key))
    except:
        return
    return


def main():
    # s1 is right hand, s2 left hand
    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((macAddress, port1))
    s1.listen(backlog)

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind((macAddress, port2))
    s2.listen(backlog)

    print("Server started")

    # Much of this doesn't do that much, but may need more logic in future
    stateCheck1 = (0, 0, 0, 0, 0)
    stateCheck2 = (0, 0, 0, 0, 0)
    state1 = (0, 0, 0, 0, 0)
    state2 = (0, 0, 0, 0, 0)
    data1 = "1,1,1,1,1,"
    data2 = "1,1,1,1,1,"

    # Try except statement with embedded loop is the entire server. 
    try:
        # Make connection with the two raspberry pis
        client1, address1 = s1.accept()
        print("First connection accepted")
        client2, address2 = s2.accept()
        print("Accepted both connections")
        # Infinite while loop unless terminated by a crash on any of the 3 computers or
        # a given input results in a break
        while 1:
            # receiving the data and parsing it
            data1 = client1.recv(size)
            data2 = client2.recv(size)
            if data1:
                data1 = data1.decode('utf-8')
            if data2:
                data2 = data2.decode('utf-8')
            print(f"lh: {str(data1):10}  rh: {str(data2):10}")
            state1 = getState(data1)
            state2 = getState(data2)
            
            # If the right hand changes in state, then go to type something.
            # This is only for the right hand since the left hand is needed for 
            # changing what the right hand can type.
            if state2 != stateCheck2:
                typeOutput(f"{str(data1):10}{str(data2):10}")
                # updating statechecks so can determine the next time the right hand changes
                stateCheck1 = state1
                stateCheck2 = state2
    except:
        # Close everything down
        print("Closing socket")
        client1.close()
        s1.close()
        client2.close()
        s2.close()

main()
