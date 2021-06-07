import os
import tree
from UI import UI
from take_action import take_action

start_state = [4]*14
start_state[6] = 0
start_state[13] = 0

difficulty = 7
is_stealing= 1

while True:
    print("Mancala\tv0.1")
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
            a = int(input())
            state,player_side = take_action(start_state,is_stealing,a,0)
        else:
            state = start_state
            player_side = ai_side
        while True:
            if player_side == ai_side:
                #os.system('cls')
                UI(state)
                t = tree.generate_search_tree(state,difficulty,ai_side,is_stealing)
                alpha = tree.alpha_beta(t)
                for node in t.Nodes:
                    if ((node.is_maximizer and (node.alpha==alpha)) or (not(node.is_maximizer) and (node.beta==alpha))):
                        a = node.idx
                        break
                if(a is None):
                    print("Game is finished!")
                    input()
                state,player_side = take_action(start_state,is_stealing,a,ai_side)
            else:
                #os.system('cls')
                UI(state)
                a = int(input())
                state,player_side = take_action(start_state,is_stealing,a,player_side)
                a = None
    elif inp == '3':
        pass
    elif inp == 'L':
        pass
    elif inp == 'E':
        break
    else:
        os.system('cls')
        continue
