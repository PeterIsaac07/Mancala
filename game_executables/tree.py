from take_action import take_action
import random

class TreeNode():

    def __init__(self,state,depth):
        self.Nodes = []
        self.idx = None
        self.state = state
        self.score = None
        self.depth = depth
        self.branching_factor = 0
        self.is_evaluated = False
        self.is_cutoff_start = False

        self.is_maximizer = True
        self.alpha = - 9999999
        self.beta = 99999999

    def eval_func(self,current_state,side,difficulty):
        mankla_to_front_fact = 0.7
        if difficulty<7:
            mankla_to_front_fact = 1
        state = self.state
        lamda = state[6]/(state[13]+1)
        p1_mankala = state[6] - current_state[6]
        p2_mankala = state[13] - current_state[13]
        p1_infront_beads = state[0] + state[1] + state[2] + state[3] +  state[4] + state[5] + state[6]
        p2_infront_beads = state[7] + state[8] + state[9] + state[10] + state[11] + state[12] + state[13]
        p1_score = mankla_to_front_fact * p1_mankala + (1-mankla_to_front_fact) * p1_infront_beads
        p2_score = mankla_to_front_fact * p2_mankala + (1-mankla_to_front_fact) * p2_infront_beads
        if difficulty<=5:
            lamda = 1
        if difficulty == 4 or difficulty == 3:
            p1_score = 0
        if difficulty == 2:
            p2_score = random.random()*10
        if difficulty == 1:
            p1_score = - p1_score
            p2_score = 0

        self.score = p2_score - lamda*p1_score
        if side == 0:
            self.score = - self.score
        return self.score

    def add_child(self,Node):
        self.Nodes.append(Node)


def generate_search_tree(current_state,max_depth,player_side,is_stealing,difficulty,last_depth = 0,top_state = None,top_side = None):
    if last_depth == 0:
        top_state = current_state
        top_side = player_side
    root = TreeNode(current_state,last_depth)
    root.is_maximizer = top_side==player_side
    if max_depth == 0:
        root.eval_func(top_state,top_side,difficulty)
        if root.is_maximizer:
            root.alpha = root.score
        else:
            root.beta = root.score
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
        new_node = generate_search_tree(new_state,max_depth-1,side,is_stealing,difficulty,last_depth+1,top_state,top_side)
        new_node.idx = i
        root.add_child(new_node)
    root.branching_factor = len(root.Nodes)
    if(root.branching_factor==0):
        root.eval_func(top_state,top_side,difficulty)
        if root.is_maximizer:
            root.alpha = root.score
        else:
            root.beta = root.score
    return root

def alpha_beta(node):

    for child in node.Nodes :
        if len(child.Nodes) == 0 : #if leaf
            v = child.score
            if node.is_maximizer:
                if v > node.alpha :
                    node.alpha = v
            else:
                if v < node.beta :
                    node.beta = v
            if node.alpha >= node.beta :
                child.is_evaluated = True
                node.is_cutoff_start = True
                if node.is_maximizer:
                    node.score = node.alpha  # exp
                    return node.alpha
                else:
                    node.score = node.beta  # exp
                    return node.beta

        else : # if not leaf
            child.alpha = node.alpha
            child.beta = node.beta
            v = alpha_beta(child)
            node.score = v #exp
            if node.is_maximizer:
                if v > node.alpha:
                    node.alpha = v
            else:
                if v < node.beta:
                    node.beta = v
            if node.alpha >= node.beta:
                child.is_evaluated = True
                node.is_cutoff_start = True
                if node.is_maximizer:
                    return node.alpha
                else:
                    return node.beta
    if node.is_maximizer:
        node.score = node.alpha #exp
        return node.alpha
    else:
        node.score = node.beta #exp
        return node.beta




#start_state = [4]*14
#start_state[6] = 0
#start_state[13] = 0

#tree = generate_search_tree(start_state,3,0,1)

#v = alpha_beta(tree)

