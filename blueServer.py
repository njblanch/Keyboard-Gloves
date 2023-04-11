import socket

port1 = 50001
port2 = 50002
macAddress = "10.245.124.161"
backlog = 5
size = 1024

# threshold values for different fingers, are resistance
T1 = .1
T2 = .9
P1 = .1
P2 = .9
M1 = .1
M2 = .9
R1 = .1
R2 = .9
Pi1 = .1
Pi2 = .9

# Values for up, neutral down
DOWN = -1
NEUTRAL = 0
UP = 1

# Use these threshold values to create states (aka finger positions)
# When these positions change, then take an input, or nothing if neutral
def get_state(stringPos):
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

def typeOutput(tupleStates1, tupleStates2):
    print("changed")
    print(tupleStates1)
    if tupleStates1 == (0, 0, 0, 0, 0) and tupleStates2 == (0, 0, 0, 0, 0):
        print("neutral")
        return


def main():
    #socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind((macAddress, port1))
    s1.listen(backlog)

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind((macAddress, port2))
    s2.listen(backlog)
    print("connected to left hand")

    stateCheck1 = (0, 0, 0, 0, 0)
    stateCheck2 = (0, 0, 0, 0, 0)
    state1 = (0, 0, 0, 0, 0)
    state2 = (0, 0, 0, 0, 0)
    data1 = "1,1,1,1,1,"
    data2 = "1,1,1,1,1,"

    try:
        client1, address1 = s1.accept()
        print("accepted")
        client2, address2 = s2.accept()
        while 1:
            data1 = client1.recv(size)
            data2 = client2.recv(size)
            if data1:
                data1 = data1.decode('utf-8')
            if data2:
                data2 = data2.decode('utf-8')
            print(str(data1) + "        " + str(data2))
            state1 = get_state(data1)
            state2 = get_state(data2)
            if state1 != stateCheck1: # only change when right hand
                typeOutput(state1, state2)
                stateCheck1 = state1
                stateCheck2 = state2
            #print(str(state) + "\n")
    except:
        print("Closing socket")
        client1.close()
        s1.close()
        client2.close()
        s2.close()
    print("passed")


main()
