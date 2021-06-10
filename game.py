import os
import tree
from UI import UI
from take_action import take_action

def take_next_input():
    while True: 
        try:
            a = input()
            if(a == 'S'):
                #save func
                continue
            elif (a == 'E'):
                os.system('cls')
                return a
            a = int(a)
            return a
        except:
            print("Invalid input")

start_state = [4]*14
start_state[6] = 0
start_state[13] = 0

difficulty = 5
is_stealing= 1

while True:
    os.system('cls')
    print("Mancala\tv0.2")
    print("Start game:")
    print("   1 - Player vs Player")
    print("   2 - Player vs AI")
    print("   3 - AI vs AI")
    print("L - Load Game")
    print("O - Options")
    print("E - Exit")

    inp = input()

    if inp == '1':
        pass
    elif inp =='2':
        os.system('cls')
        print('Choose who starts!')
        print('1 - Me')
        print('2 - AI')
        inp = input()
        ai_side = 1
        if inp == '1':
            ai_start = False
        elif inp == '2':
            ai_start = True
        else:
            continue
        os.system('cls')
        if ai_start == False:
            UI(start_state)
            a = take_next_input()
            if(a=='E'):
                continue
            state,player_side = take_action(start_state,is_stealing,a,0)
        else:
            state = start_state
            player_side = ai_side
        while True:
            #Win-Lose condition
            if((int(state[13])+int(state[6])) == 48):
                UI(state)
                print('Game finished!')
                diff = int(state[13]) - int(state[6])
                if(diff>0):
                    print("AI (Red) wins by "+abs(diff)+" points!")
                elif(diff<0):
                    print("Player (Blue) wins by "+abs(diff)+" points!")
                else:
                    print("Tie!")
                print('Continue to main menu?')
                print('Y - Yes')
                print('E - Exit')
                inp = input()
                if (inp=='E'):
                    exit()
                else:
                    break
            #AI playing
            if player_side == ai_side:
                #os.system('cls')
                UI(state)
                t = tree.generate_search_tree(state,difficulty,ai_side,is_stealing,difficulty)
                alpha = tree.alpha_beta(t)
                for node in t.Nodes:
                    if ((node.is_maximizer and (node.alpha==alpha)) or (not(node.is_maximizer) and (node.beta==alpha))):
                        a = node.idx
                        break
                state,player_side = take_action(start_state,is_stealing,a,ai_side)
            #Hooman playing
            else:
                #os.system('cls')
                UI(state)
                a = take_next_input()
                if(a=='E'):
                    break
                state,player_side = take_action(start_state,is_stealing,a,player_side)
                a = None
    elif inp == '3':
        pass
    elif inp == 'L':
        os.system('cls')
        pass
    elif inp == 'E':
        break
    else:
        os.system('cls')
        continue
