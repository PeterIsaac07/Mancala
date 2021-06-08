import socket
import sys
import math
import _pickle as cPickle

def UI(state_vector):
    string_vector=["0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
    for i in range(0,14):
        if(state_vector[i]<10):
            string_vector[i] = " " + str(state_vector[i])
        else:
            string_vector[i] = str(state_vector[i])
    print("\x1b[0;30;41m" + "[ {} ]".format(string_vector[13]) + "\x1b[0;30;47m"+" "+"\x1b[0;30;41m" + "({})\u2085 ({})\u2084 ({})\u2083 ({})\u2082 ({})\u2081 ({})\u2080".format(
        string_vector[12], string_vector[11], string_vector[10], string_vector[9], string_vector[8],
        string_vector[7]) + "\x1b[0;30;47m" + "       "+"\33[0m")
    print("\x1b[0;30;47m"+"                                                 "+"\33[0m")
    print("\x1b[0;30;47m"+"       "+"\x1b[0;30;44m" + "({})\u2080 ({})\u2081 ({})\u2082 ({})\u2083 ({})\u2084 ({})\u2085".format(string_vector[0],
                                                                                                       string_vector[1],
                                                                                                       string_vector[2],
                                                                                                       string_vector[3],
                                                                                                       string_vector[4],
                                                                                                       string_vector[
                                                                                                           5]) + "\x1b[0;30;47m"+" " + "\x1b[0;30;44m" + "[ {} ]".format(
        string_vector[6]) + "\33[0m")
    print()

def take_action(current_state_vec, is_stealing ,action, player_side):
    if((is_stealing not in range(0,2))):
        raise Exception("is_stealing must be 0 or 1")

    if (action not in range(0,6)):
        raise Exception("action must be in range of 0 to 5")

    if(player_side==0):
        if(current_state_vec[action]==0):
            return current_state_vec,player_side
        s=0
        for i in range(1, current_state_vec[action] + 1):
            if ((action + i) % 14 == 13):   s+=1

        for i in range(1, current_state_vec[action] + 1 + s):
            if ((action + i) % 14 != 13):   current_state_vec[(action+i)%14] += 1

        old_current_state_vec = current_state_vec[action]
        current_state_vec[action] = int(current_state_vec[action] / 13)

        if ((action + old_current_state_vec) % 14 == 6):
            next_turn = 0
        else:
            next_turn = 1

        if(is_stealing):
            if(((action + old_current_state_vec)%13 in range (0,6)) and (current_state_vec[(action + old_current_state_vec)%13]==1) and (current_state_vec[12-((action + old_current_state_vec)%13)]>0)):
                current_state_vec[(action + old_current_state_vec)%13]=0
                current_state_vec[6]+=(current_state_vec[12-((action + old_current_state_vec)%13)]+1)
                current_state_vec[12-((action + old_current_state_vec)%13)]=0
            else:   pass
        else:   pass


    elif(player_side==1):
        action+=7
        if (current_state_vec[action] == 0):
            return current_state_vec, player_side
        s=0
        for i in range(1, current_state_vec[action] + 1):
            if ((action + i) % 14 == 6):   s+=1

        for i in range(1, current_state_vec[action] + 1 + s):
            if ((action + i) % 14 != 6):    current_state_vec[(action + i) % 14] += 1
            else:   s+=1


        old_current_state_vec = current_state_vec[action]
        current_state_vec[action] = int(current_state_vec[action] / 13)

        if ((action + old_current_state_vec) % 14 == 13):
            next_turn = 1
        else:
            next_turn = 0

        if (is_stealing):
            if (((action + old_current_state_vec)%13 in range (7,13)) and (current_state_vec[(action + old_current_state_vec) % 13] == 1) and (current_state_vec[12-((action + old_current_state_vec)%13)]>0)):
                current_state_vec[(action + old_current_state_vec) % 13] = 0
                current_state_vec[13] += (current_state_vec[12 - ((action + old_current_state_vec) % 13)] + 1)
                current_state_vec[12 - ((action + old_current_state_vec) % 13)] = 0
            else:   pass
        else:   pass

    else:
        raise Exception("player_side must be 0 or 1")

    if (current_state_vec[0] == 0 and current_state_vec[1] == 0 and current_state_vec[2] == 0 and current_state_vec[3] == 0 and current_state_vec[4] == 0 and current_state_vec[5] == 0):
        current_state_vec[13]+=(current_state_vec[12]+current_state_vec[11]+current_state_vec[10]+current_state_vec[9]+current_state_vec[8]+current_state_vec[7])
        current_state_vec[12] = 0
        current_state_vec[11] = 0
        current_state_vec[10] = 0
        current_state_vec[9] = 0
        current_state_vec[8] = 0
        current_state_vec[7] = 0
        if(current_state_vec[6]>current_state_vec[13]):
            print("Player 1 wins! (Blue)")
        elif(current_state_vec[6]<current_state_vec[13]):
            print("Player 2 wins! (Red)")
        elif(current_state_vec[6]==current_state_vec[13]):
            print("It's a Draw!")

    elif(current_state_vec[7]==0 and current_state_vec[8]==0 and current_state_vec[9]==0 and current_state_vec[10]==0 and current_state_vec[11]==0 and current_state_vec[12]==0):
        current_state_vec[6] += (current_state_vec[0] + current_state_vec[1] + current_state_vec[2] + current_state_vec[3] +current_state_vec[4] + current_state_vec[5])
        current_state_vec[0] = 0
        current_state_vec[1] = 0
        current_state_vec[2] = 0
        current_state_vec[3] = 0
        current_state_vec[4] = 0
        current_state_vec[5] = 0
        if (current_state_vec[6] > current_state_vec[13]):
            print("Player 1 wins! (Blue)")
        elif (current_state_vec[6] < current_state_vec[13]):
            print("Player 2 wins! (Red)")
        elif (current_state_vec[6] == current_state_vec[13]):
            print("It's a Draw!")

    return current_state_vec,next_turn

current_state_vec=[4,4,4,4,4,4,0,4,4,4,4,4,4,0]

#############################################################################
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
# Wait for a connection
print('waiting for a connection')
connection, client_address = sock.accept()
print('connection from', client_address)
#############################################################################
print("To enable stealing enter 1 to disable stealing enter 0 , both players must agree on a mode")
while True :
    stealing = input("Please enter your mood choice: " )
    opponent_choice = connection.recv(1)
    opponent_choice = opponent_choice.decode()
    if opponent_choice == stealing :
        connection.sendall('1'.encode())
        print("Game Started")
        break
    else:
        print("You chose different mode than your opponent please retry")
        connection.sendall('0'.encode())

print("It's your turn , You Play First")
UI(current_state_vec)
is_stealing = int(stealing)
player_side = 0
while True:
    player_side = 0
    action = int(input("Please enter which slot you want to play: "))
    current_state_vec, next_turn = take_action(current_state_vec, is_stealing, action, player_side)
    UI(current_state_vec)
    connection.sendall((str(action)).encode())
    if next_turn == 0:
        continue
    elif next_turn == 1:
        while next_turn == 1:
            player_side = 1
            action = connection.recv(1)
            action = action.decode()
            current_state_vec , next_turn = take_action(current_state_vec, is_stealing, int(action), player_side)
            UI(current_state_vec)

print("done")
connection.close()