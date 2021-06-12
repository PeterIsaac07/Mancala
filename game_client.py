import os
import tree
import time
from UI import UI
import pickle
import socket

from take_action import take_action

def take_next_input(state=None,is_stealing=None,difficulty=None,verbose_mode=None,turn_no=None):
    while True:
        try:
            a = input()
            a = int(a)
            return a
        except:
            if(a.upper() == 'S'):
                #save func
                saving=[state,is_stealing,difficulty,verbose_mode,turn_no] ############################
                out=open("saved","wb")
                pickle.dump(saving,out)
                out.close()

                exit() ###############
            elif (a.upper() == 'E'):
                os.system('cls')
                return a
            print("Invalid input")

def traverse(root,nodes_dict_list):
    info = {}
    info['branching_factor'] = root.branching_factor
    info['depth'] = root.depth
    info['is_evaluated'] = root.is_evaluated
    info['is_cutoff_start'] = root.is_cutoff_start
    info['is_leaf'] = root.branching_factor == 0
    info['score'] = root.score
    nodes_dict_list.append(info)
    if root.branching_factor>0:
        for i in range(root.branching_factor):
            traverse(root.Nodes[i],nodes_dict_list)

def print_verbose(is_verbose_on,tree,time_diff,turn_no,filename):
    if is_verbose_on:
        if filename is None:
            if not os.path.isdir('verbose'):
                os.mkdir('verbose')
            filename = "verbose\game_"+str(time.time())+".txt"
            file = open(filename, "x")
            file.close()
        print('---------------------------')
        print('Information on last turn :-')
        print('---------------------------')
        print('Time taken: ', time_diff , "ms")
        nodes_dict_list = []
        traverse(tree,nodes_dict_list)
        max_depth,num_cutoffs,num_leafs = 0,0,0
        nodes_cutoff = []
        leaf_scores = []
        branching_factors = []
        for i in range(len(nodes_dict_list)):
            if max_depth<nodes_dict_list[i]['depth']:
                max_depth = nodes_dict_list[i]['depth']
            if nodes_dict_list[i]['is_cutoff_start']:
                num_cutoffs+=1
                nodes_cutoff.append((num_cutoffs,nodes_dict_list[i]['depth']))
            if nodes_dict_list[i]['is_leaf'] and nodes_dict_list[i]['is_evaluated']:
                num_leafs+=1
                leaf_scores.append((num_leafs,nodes_dict_list[i]['score']))
            if nodes_dict_list[i]['is_evaluated']:
                branching_factors.append(nodes_dict_list[i]['branching_factor'])
        average_branching_factor = sum(branching_factors)/len(branching_factors)
        print('Max depth in Tree = ' , max_depth)
        print('Average Branching Factor = ' ,round(average_branching_factor,3))
        print('Number of explored leaf nodes = ',num_leafs)

        file = open(filename,'a')

        file.write('\n')
        file.write("Turn "+str(turn_no)+' :\n')
        file.write('-----\n')
        file.write('#Leaf :: Utility value\n')
        for leaf in leaf_scores:
            file.write('   '+str(leaf[0])+' :: '+str(round(leaf[1],3))+'\n')
        print('Number of cutoffs = ',num_cutoffs)
        if num_cutoffs>0:
            print('#Cuttoff :: Level')
            for cut in nodes_cutoff:
                print('   ',cut[0],' :: ',cut[1])
        print('---------------------------')
        return filename

start_state = [4]*14
def reset_state():
    start_state[0:13] = [4]*14
    start_state[6] = 0
    start_state[13] = 0

#Default_options
difficulty = 5
is_stealing= 1
verbose_mode = False
#load_flag=False

while True:
    filename = None
    reset_state()
    os.system('cls')
    print("Mancala\tv0.4")
    print("Start game:")
    print("   1 - Player vs Player")
    print("   2 - Player vs AI")
    print("   3 - AI vs AI")
    print("L - Load Game")
    print("O - Options")
    print("E - Exit")
    inp = input()
    if inp == '1':
        ############################################################################
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 5000)
        print('connecting to {} port {}'.format(*server_address))
        connection_Status = -1
        while True :
            try:
                connection_Status = sock.connect(server_address)
                break
            except:
                continue
        ############################################################################
        state = start_state
        print("connection established")

        print("it is your opponent turn")
        UI(state)

        while True:
            if ((int(state[13]) + int(state[6])) == 48):
                UI(state)
                print('Game finished!')
                diff = int(state[13]) - int(state[6])
                if (diff > 0):
                    print("You win " + str(abs(diff)) + " points!")
                elif (diff < 0):
                    print("your opponent wins " + str(abs(diff)) + " points!")
                else:
                    print("Tie!")
            player_side = 0
            action = sock.recv(1)
            action = action.decode()
            state, next_turn = take_action(state, is_stealing, int(action), player_side)
            UI(state)
            if next_turn == 0:
                continue
            elif next_turn == 1:
                while next_turn == 1:
                    player_side = 1
                    action = int(input("Please enter which slot you want to play: "))
                    state, next_turn = take_action(state, is_stealing, action, player_side)
                    UI(state)
                    sock.sendall((str(action)).encode())

    elif inp =='2': # Player vs AI
        turn_no = 0
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
        UI(start_state)
        if ai_start == False:
            a = take_next_input()
            if(a=='E'):
                continue
            turn_no+=1
            state,player_side = take_action(start_state,is_stealing,a,0)
            UI(state)
        else:
            state = start_state
            player_side = ai_side
        while True:

            #Win-Lose condition , check if game ended
            if((int(state[13])+int(state[6])) == 48):
                UI(state)
                print('Game finished!')
                diff = int(state[13]) - int(state[6])
                if(diff>0):
                    print("AI (Red) wins by "+str(abs(diff))+" points!")
                elif(diff<0):
                    print("Player (Blue) wins by "+str(abs(diff))+" points!")
                else:
                    print("Tie!")
                print('Back to main menu?')
                print('Y - Yes')
                print('E - Exit')
                inp = input()
                if (inp.upper()=='E'):
                    exit()
                else:
                    break
            #AI playing
            if player_side == ai_side:
                T1 = time.time_ns()
                #os.system('cls')
                t = tree.generate_search_tree(state,difficulty,ai_side,is_stealing,difficulty)
                alpha = tree.alpha_beta(t)
                for node in t.Nodes:
                    if ((node.is_maximizer and (node.alpha==alpha)) or (not(node.is_maximizer) and (node.beta==alpha))):
                        a = node.idx
                        break
                T2 = time.time_ns()
                time_diff = (T2 - T1)*10**-6
                state,player_side = take_action(start_state,is_stealing,a,ai_side)
                print('AI chooses ',a)
                UI(state)
                filename = print_verbose(verbose_mode,t,round(time_diff,3),turn_no,filename)
                turn_no += 1
            #Hooman playing
            else:
                #os.system('cls')
                print("Your turn")
                a = take_next_input(state,is_stealing,difficulty,verbose_mode,turn_no) ####################


                if(a=='E' or a == 'e'):
                    break
                state,player_side = take_action(state,is_stealing,a,player_side) #############################state
                turn_no += 1
                UI(state)
                a = None
    elif inp == '3':
        ############################################################################
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 5000)
        print('connecting to {} port {}'.format(*server_address))

        while True :
            try:
                connection_Status = sock.connect(server_address)
                break
            except:
                continue
        ############################################################################
        UI(start_state)
        state = start_state
        player_side = 0
        ai_side =1
        turn_no = 0
        while True:
            # Win-Lose condition , check if game ended
            turn_no +=1
            if ((int(state[13]) + int(state[6])) == 48):
                UI(state)
                print('Game finished!')
                diff = int(state[13]) - int(state[6])
                if (diff > 0):
                    print("OUR AI  wins by " + str(abs(diff)) + " points!")
                elif (diff < 0):
                    print("OPPONENT AI wins by " + str(abs(diff)) + " points!")
                else:
                    print("Tie!")
                print('Back to main menu?')
                print('Y - Yes')
                print('E - Exit')
                inp = input()
                if (inp.upper() == 'E'):
                    quit()
                else:
                    break
            if player_side == 0:
                opponent_Choice = sock.recv(1)
                a = opponent_Choice.decode()
                a = int(a)
                print('Opponent  AI chooses ', a)
                state, player_side = take_action(state, is_stealing, a, 0)
                UI(state)
            if player_side == ai_side:
                T1 = time.time_ns()
                # os.system('cls')
                t = tree.generate_search_tree(state, difficulty, ai_side, is_stealing, difficulty)
                alpha = tree.alpha_beta(t)
                for node in t.Nodes:
                    if ((node.is_maximizer and (node.alpha == alpha)) or (
                            not (node.is_maximizer) and (node.beta == alpha))):
                        a = node.idx
                        break
                T2 = time.time_ns()
                time_diff = (T2 - T1) * 10 ** -6
                state, player_side = take_action(state, is_stealing, a, ai_side)
                filename = print_verbose(verbose_mode,t,round(time_diff,3),turn_no,filename)
                print('OUR AI chooses ', a)
                UI(state)
                sock.sendall((str(a)).encode())






    elif inp.upper() == 'O':
        os.system('cls')
        difficulty_names = {}
        difficulty_names[1] = "Not even playing"
        difficulty_names[2] = "Stupid"
        difficulty_names[3] = "Very Easy"
        difficulty_names[4] = "Easy"
        difficulty_names[5] = "Normal"
        difficulty_names[6] = "Above Average"
        difficulty_names[7] = "Hard"
        difficulty_names[8] = "Very Hard"
        difficulty_names[9] = "Smarter than most"
        difficulty_names[10] = "Next step in the evolution (1 turn may take over a minute)"
        print("Difficulty Level: " , difficulty_names[difficulty])
        stealing = "On" if is_stealing else "Off"
        verbose = "On" if verbose_mode else "Off"
        print("Stealing: ",stealing)
        print("Verbose mode: ",verbose)
        print("D - Change Difficulty")
        print("S - Switch Stealing")
        print("V - Switch Verbose Mode")
        print("E - Back to main menu")
        inp = input()
        if(inp.upper() == 'D'):
            os.system('cls')
            i = 1
            for s in difficulty_names:
                print(str(i) + ' - ' + difficulty_names[s])
                i+=1
            inp = input()
            try:
                assert(int(inp)<=10)
                assert(int(inp)>0)
                i = int(inp)
                difficulty = i
                i = None
            except:
                i = None
                continue
        elif(inp.upper() == 'S'):
            is_stealing = not is_stealing
        elif(inp.upper() == 'V'):
            verbose_mode = not verbose_mode
        else:
            continue
    elif inp.upper() == 'L':
        file=open("saved","rb") ###########################3
        input_list=pickle.load(file)
        file.close()
        state=input_list[0]
        is_stealing=input_list[1]
        difficulty=input_list[2]
        verbose_mode=input_list[3]
        turn_no=input_list[4]
        player_side=0
        ai_side=1
        #load_flag=True
        UI(state)
        os.system('cls')
        while True:

            #Win-Lose condition , check if game ended
            if((int(state[13])+int(state[6])) == 48):
                UI(state)
                print('Game finished!')
                diff = int(state[13]) - int(state[6])
                if(diff>0):
                    print("AI (Red) wins by "+str(abs(diff))+" points!")
                elif(diff<0):
                    print("Player (Blue) wins by "+str(abs(diff))+" points!")
                else:
                    print("Tie!")
                print('Back to main menu?')
                print('Y - Yes')
                print('E - Exit')
                inp = input()
                if (inp.upper()=='E'):
                    exit()
                else:
                    break
            #AI playing
            if player_side == ai_side:
                T1 = time.time_ns()
                #os.system('cls')
                t = tree.generate_search_tree(state,difficulty,ai_side,is_stealing,difficulty)
                alpha = tree.alpha_beta(t)
                for node in t.Nodes:
                    if ((node.is_maximizer and (node.alpha==alpha)) or (not(node.is_maximizer) and (node.beta==alpha))):
                        a = node.idx
                        break
                T2 = time.time_ns()
                time_diff = (T2 - T1)*10**-6
                state,player_side = take_action(start_state,is_stealing,a,ai_side)
                print('AI chooses ',a)
                UI(state)
                filename = print_verbose(verbose_mode,t,round(time_diff,3),turn_no,filename)
                turn_no += 1
            #Hooman playing
            else:
                #os.system('cls')
                print("Your turn")
                a = take_next_input(state,is_stealing,difficulty,verbose_mode) ####################


                if(a=='E' or a == 'e'):
                    break
                state,player_side = take_action(state,is_stealing,a,player_side) #############################state
                turn_no += 1
                UI(state)
                a = None
    elif inp.upper() == 'E':
        break
    else:
        os.system('cls')
        continue
