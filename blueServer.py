import socket

# All socket server scripting is taken from this guide:
# https://realpython.com/python-sockets/#multi-connection-client-and-server

# Right hand is port 50001, Left hand 50002
port1 = 50001
port2 = 50002
# Mac address is the IPV4 wifi address of the host computer. 
macAddress = ""
backlog = 5
size = 1024

# Values for neutral, down
NEUTRAL = 0
PRESS = 1

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
def typeOutput(rtuple, ltuple):
    print("changed")
    print(rtuple)
    if rtuple == (0, 0, 0, 0, 0) and ltuple == (0, 0, 0, 0, 0):
        print("neutral")
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
            print(f"rh: {str(data1):10}  lh: {str(data2):10}")
            state1 = getState(data1)
            state2 = getState(data2)
            
            # If the right hand changes in state, then go to type something.
            # This is only for the right hand since the left hand is needed for 
            # changing what the right hand can type.
            if state1 != stateCheck1:
                typeOutput(state1, state2)
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
