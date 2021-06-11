import socket
import sys
import math
import _pickle as cPickle
from UI import UI
from take_action import take_action


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