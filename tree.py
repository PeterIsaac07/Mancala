import numpy as np
from take_action import take_action

class TreeNode():

    def __init__(self,state,depth):
        self.Nodes = []
        self.state = state
        self.score = None
        self.depth = depth
        self.branching_factor = None
        self.is_evaluated = False
        self.is_cutoff_start = False

        self.is_maximizer = True
        self.alpha = - np.inf
        self.beta = np.inf

    def eval_func(self,current_state,mankla_to_front_fact = 0.7):
        state = self.state
        lamda = state[13]/(state[6]+1)
        p1_mankala = state[6] - current_state[6]
        p2_mankala = state[13] - current_state[13]
        p1_infront_beads = state[0] + state[1] + state[2] + state[3] +  state[4] + state[5] + state[6] 
        p2_infront_beads = state[7] + state[8] + state[9] + state[10] + state[11] + state[12] + state[13]
        p1_score = mankla_to_front_fact * p1_mankala + (1-mankla_to_front_fact) * p1_infront_beads
        p2_score = mankla_to_front_fact * p2_mankala + (1-mankla_to_front_fact) * p2_infront_beads

        self.score = p1_score - lamda*p2_score

    def add_child(self,Node):
        self.Nodes.append(Node)


def generate_search_tree(current_state,max_depth,player_side,is_stealing,last_depth = 0,top_state = None,top_side = None):
    if last_depth == 0:
        top_state = current_state
        top_side = player_side
    root = TreeNode(current_state,last_depth)
    root.is_maximizer = top_side==player_side
    if max_depth == 0:
        root.eval_func(top_state)
        return root
    for i in range(0,6):
        if player_side == 1:
            if current_state[i+7] ==  0:
                continue
        elif player_side == 0:
            if current_state[i] ==  0:
                continue
        state = current_state.copy()
        new_state,side = take_action(state,is_stealing,i,player_side)
        root.add_child(generate_search_tree(new_state,max_depth-1,side,is_stealing,last_depth+1,top_state,top_side))
    root.branching_factor = len(root.Nodes)
    return root

start_state = [4]*14
start_state[6] = 0
start_state[13] = 0

tree = generate_search_tree(start_state,3,0,1)




