import socket
import sys
import _pickle as cPickle
from UI import UI
from take_action import take_action
current_state_vec=[4,4,4,4,4,4,0,4,4,4,4,4,4,0]
############################################################################
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
############################################################################
print("To enable stealing enter 1 to disable stealing enter 0 , both players must agree on a mode")
while True:
    stealing = input("Please enter your mode choice: " )
    sock.sendall(stealing.encode())
    opponent_Choice = sock.recv(1)
    opponent_Choice = opponent_Choice.decode()
    if opponent_Choice == '1' :
        print("Game Started")
        break
    elif opponent_Choice == '0' :
        print("You chose different mode than your opponent please retry")

print("It's your oponent turn , You Play Second")
UI(current_state_vec)
is_stealing = int(stealing)
player_side = 0

while (True):
    player_side = 0
    action = sock.recv(1)
    action = action.decode()
    current_state_vec, next_turn = take_action(current_state_vec, is_stealing, int(action), player_side)
    UI(current_state_vec)
    if next_turn == 0:
        continue
    elif next_turn == 1:
        while next_turn == 1 :
            player_side = 1
            action = int(input("Please enter which slot you want to play: "))
            current_state_vec , next_turn = take_action(current_state_vec, is_stealing, action, player_side)
            UI(current_state_vec)
            sock.sendall((str(action)).encode())


data = sock.recv(1)
print(data.decode())

print('closing socket')
sock.close()