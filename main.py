import copy
from hashlib import new
import random
import time


# SAMET ENES ORSDEMIR 150119661

class State: # state class to represent nodes
    def __init__(self, holes, map, depth, parent):
        self.holes = holes
        self.map = map
        self.depth = depth
        self.parent = parent

    def print_board(self):
        i = 0
        print("Depth:" + str(self.depth))
        for row in self.map:
            print("")
            for column in row:
                if(column == 1):
                    print("X", end = ' ')
                elif(column == 0):
                    print("O", end = ' ')  
                else:
                    print(" ", end = ' ')  
            i += 1
        

time_limit = 0
frontier_list=[]
        
initial_state = State([[3,3]],
           [
            [8,8,1,1,1,8,8],
            [8,8,1,1,1,8,8],
            [1,1,1,1,1,1,1],
            [1,1,1,0,1,1,1],
            [1,1,1,1,1,1,1],
            [8,8,1,1,1,8,8],
            [8,8,1,1,1,8,8]
            ], 0, None)

goal_state_map =  [
            [8,8,0,0,0,8,8],
            [8,8,0,0,0,8,8],
            [0,0,0,0,0,0,0],
            [0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0],
            [8,8,0,0,0,8,8],
            [8,8,0,0,0,8,8]
            ]

frontier_list.append(initial_state)


def expand_state(state,frontier): # expand for dfs bfs iterative
    for hole in state.holes: # holes in state
        x = hole[0] # x coordinate of hole
        y = hole[1] # y coordinate of hole
        parent = state # parent assign
        depth = int(state.depth + 1) # depth assign
        if((y!=0) and (y!=1)): # map limit
            if ((state.map[y-1][x]== 1) and (state.map[y-2][x]==1)): # north check
                map = copy.deepcopy(state.map) # map copy
                map[y][x] = 1 # hole update
                map[y-1][x] = 0 # hole update
                map[y-2][x] = 0 # hole update
                new_holes = [[x,y-1],[x,y-2]] # holes list update
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)
                    
                holes.remove([x,y])         
                frontier.append(State( holes, map, depth, parent)) # add child to frontier 
        if((x != 0) and (x != 1)): # map limit
            if ((state.map[y][x-1]== 1) and (state.map[y][x-2]==1)): # west check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x-1] = 0
                map2[y][x-2] = 0
                new_holes = [[x-1,y],[x-2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  

                holes.remove([x,y])        
                frontier.append(State( holes, map2, depth, parent))  # add child to frontier  
        if((x != 5) and (x != 6)): # map limit
            if ((state.map[y][x+1]== 1) and (state.map[y][x+2]==1)): # east check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x+1] = 0
                map2[y][x+2] = 0
                new_holes = [[x+1,y],[x+2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  
                    
                holes.remove([x,y])     
                frontier.append(State( holes, map2, depth, parent)) # add child to frontier 
        if((y!=5) and (y!=6)): # map limit
            if ((state.map[y+1][x]== 1) and (state.map[y+2][x]==1)): # south check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y+1][x] = 0
                map2[y+2][x] = 0
                new_holes = [[x,y+1],[x,y+2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                    
                holes.remove([x,y])      
                frontier.append(State( holes, map2, depth, parent)) # add child to frontier 


def expand_state_HEURISTIC(state,frontier): # a heuristic for alone pegs
    to_be_added = []
    for hole in state.holes:
        x = hole[0]
        y = hole[1]
        parent = state
        depth = int(state.depth + 1)
        if((y!=0) and (y!=1)):
            if ((state.map[y-1][x]== 1) and (state.map[y-2][x]==1)):
                map = copy.deepcopy(state.map)
                map[y][x] = 1
                map[y-1][x] = 0
                map[y-2][x] = 0
                new_holes = [[x,y-1],[x,y-2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                holes.remove([x,y])         
                to_be_added.append(State( holes, map, depth, parent))
                
        if((y!=5) and (y!=6)):
            if ((state.map[y+1][x]== 1) and (state.map[y+2][x]==1)):
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y+1][x] = 0
                map2[y+2][x] = 0
                new_holes = [[x,y+1],[x,y+2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                    
                holes.remove([x,y])      
                to_be_added.append(State( holes, map2, depth, parent)) 
        if((x != 0) and (x != 1)):
            if ((state.map[y][x-1]== 1) and (state.map[y][x-2]==1)):
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x-1] = 0
                map2[y][x-2] = 0
                new_holes = [[x-1,y],[x-2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  

                holes.remove([x,y])        
                to_be_added.append(State( holes, map2, depth, parent))         
        if((x != 5) and (x != 6)):
            if ((state.map[y][x+1]== 1) and (state.map[y][x+2]==1)):
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x+1] = 0
                map2[y][x+2] = 0
                new_holes = [[x+1,y],[x+2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  
                    
                holes.remove([x,y])     
                to_be_added.append(State( holes, map2, depth, parent))

    sorted_to_be_added = {}
    for newstate in to_be_added:
        alone_peg_counter = 0
        for row in range(7):
            for column in range(7):
                if((column != 6)):
                        if((newstate.map[row][column] == 1) and (newstate.map[row][column+1] == 1) ):
                            continue
                if((column != 0)):
                        if((newstate.map[row][column] == 1) and (newstate.map[row][column-1] == 1) ):
                            continue
                if((row != 6)):
                        if((newstate.map[row][column] == 1) and (newstate.map[row+1][column] == 1) ):
                            continue
                if((row != 0)):
                        if((newstate.map[row][column] == 1) and (newstate.map[row-1][column] == 1) ):
                            continue
                if((newstate.map[row][column] == 8) or (newstate.map[row][column] == 0)):
                        continue
                else:
                        alone_peg_counter += 1

        sorted_to_be_added[newstate] = alone_peg_counter
    sorted_to_be_added = dict(sorted(sorted_to_be_added.items(), key=lambda item: item[1], reverse=True))    
    sorted_to_be_added_only_keys = list(sorted_to_be_added.keys()) 
        
    fuc = list(sorted_to_be_added.values())
    #print(fuc)
    for i_state in sorted_to_be_added_only_keys:
            frontier.append(i_state)
            #print(len(frontier))    
            #print(i_state.print_board())

def expand_state_HEURISTIC3(state,frontier): # heuristic for manhattan distance
    to_be_added = [] # children's temp list
    for hole in state.holes: # state holes
        x = hole[0] # hole coordinate for x
        y = hole[1] # hole coordinate for y
        parent = state # parent assign
        depth = int(state.depth + 1) # depth assign
        if((y!=0) and (y!=1)): # limit of map
            if ((state.map[y-1][x]== 1) and (state.map[y-2][x]==1)): # north check
                map = copy.deepcopy(state.map)
                map[y][x] = 1
                map[y-1][x] = 0
                map[y-2][x] = 0
                new_holes = [[x,y-1],[x,y-2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                holes.remove([x,y])         
                to_be_added.append(State( holes, map, depth, parent))
                
        if((y!=5) and (y!=6)): # limit of map
            if ((state.map[y+1][x]== 1) and (state.map[y+2][x]==1)): # south check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y+1][x] = 0
                map2[y+2][x] = 0
                new_holes = [[x,y+1],[x,y+2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                    
                holes.remove([x,y])      
                to_be_added.append(State( holes, map2, depth, parent)) 
        if((x != 0) and (x != 1)): # limit of map
            if ((state.map[y][x-1]== 1) and (state.map[y][x-2]==1)): # west check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x-1] = 0
                map2[y][x-2] = 0
                new_holes = [[x-1,y],[x-2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  

                holes.remove([x,y])        
                to_be_added.append(State( holes, map2, depth, parent))         
        if((x != 5) and (x != 6)): # limit of map
            if ((state.map[y][x+1]== 1) and (state.map[y][x+2]==1)): # east check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x+1] = 0
                map2[y][x+2] = 0
                new_holes = [[x+1,y],[x+2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  
                    
                holes.remove([x,y])     
                to_be_added.append(State( holes, map2, depth, parent))

    sorted_to_be_added = {} # manhattan sorted list
    for newstate in to_be_added: # for loop in to be added states
        manhattan_distance_sum = 0
        for row in range(7): # row
            for column in range(7): # column
                if(newstate.map[row][column] == 1): # if current index is 1
                    manhattan_distance_sum += abs(row-3) + abs(column-3) # calculation absolute value for manhattan distance
                    sorted_to_be_added[newstate] = manhattan_distance_sum # add manhattan list as key-value
    sorted_to_be_added = dict(sorted(sorted_to_be_added.items(), key=lambda item: item[1],reverse=True)) # sort the list   
    sorted_to_be_added_only_keys = list(sorted_to_be_added.keys()) 
    fuc = list(sorted_to_be_added.values())
    for i_state in sorted_to_be_added_only_keys: # add to frontier in manhattan order
            frontier.append(i_state)
           

def expand_state_HEURISTIC2(state,frontier): #heuristic for number of holes 
    to_be_added = []
    for hole in state.holes:
        x = hole[0]
        y = hole[1]
        parent = state
        depth = int(state.depth + 1)
        if((y!=0) and (y!=1)):
            if ((state.map[y-1][x]== 1) and (state.map[y-2][x]==1)):
                map = copy.deepcopy(state.map)
                map[y][x] = 1
                map[y-1][x] = 0
                map[y-2][x] = 0
                new_holes = [[x,y-1],[x,y-2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                holes.remove([x,y])         
                to_be_added.append(State( holes, map, depth, parent))
                
        if((y!=5) and (y!=6)):
            if ((state.map[y+1][x]== 1) and (state.map[y+2][x]==1)):
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y+1][x] = 0
                map2[y+2][x] = 0
                new_holes = [[x,y+1],[x,y+2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                    
                holes.remove([x,y])      
                to_be_added.append(State( holes, map2, depth, parent)) 
        if((x != 0) and (x != 1)):
            if ((state.map[y][x-1]== 1) and (state.map[y][x-2]==1)):
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x-1] = 0
                map2[y][x-2] = 0
                new_holes = [[x-1,y],[x-2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  

                holes.remove([x,y])        
                to_be_added.append(State( holes, map2, depth, parent))         
        if((x != 5) and (x != 6)):
            if ((state.map[y][x+1]== 1) and (state.map[y][x+2]==1)):
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x+1] = 0
                map2[y][x+2] = 0
                new_holes = [[x+1,y],[x+2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  
                    
                holes.remove([x,y])     
                to_be_added.append(State( holes, map2, depth, parent))

    sorted_to_be_added = {}
    for newstate in to_be_added:
        sorted_to_be_added[newstate] = len(newstate.holes)
    sorted_to_be_added = dict(sorted(sorted_to_be_added.items(), key=lambda item: item[1]))    
    sorted_to_be_added_only_keys = list(sorted_to_be_added.keys()) 
        
    fuc = list(sorted_to_be_added.values())
    #print(fuc)
    for i_state in sorted_to_be_added_only_keys:
            frontier.append(i_state)
            #print(len(frontier))    
            #print(i_state.print_board())

def expand_state_RANDOM(state,frontier):
    to_be_added = [] # children's temp list
    for hole in state.holes: # state holes
        x = hole[0] # hole coordinate for x
        y = hole[1] # hole coordinate for y
        parent = state # parent assign
        depth = int(state.depth + 1) # depth assign
        if((y!=0) and (y!=1)): # limit of map
            if ((state.map[y-1][x]== 1) and (state.map[y-2][x]==1)): # north check
                map = copy.deepcopy(state.map)
                map[y][x] = 1 # map update
                map[y-1][x] = 0 # map update
                map[y-2][x] = 0 # map update
                new_holes = [[x,y-1],[x,y-2]] # holes update
                holes = copy.deepcopy(state.holes)
                for ho in new_holes: 
                    holes.append(ho)
                    
                holes.remove([x,y])         
                to_be_added.append(State( holes, map, depth, parent)) # add child to temp list
        if((y!=5) and (y!=6)): # limit of map
            if ((state.map[y+1][x]== 1) and (state.map[y+2][x]==1)): # south check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y+1][x] = 0
                map2[y+2][x] = 0
                new_holes = [[x,y+1],[x,y+2]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho) 
                    
                holes.remove([x,y])      
                to_be_added.append(State( holes, map2, depth, parent))  # add child to temp list
        if((x != 5) and (x != 6)): # limit of map
            if ((state.map[y][x+1]== 1) and (state.map[y][x+2]==1)): # east check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x+1] = 0
                map2[y][x+2] = 0
                new_holes = [[x+1,y],[x+2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  
                    
                holes.remove([x,y])     
                to_be_added.append(State( holes, map2, depth, parent))  # add child to temp list
        if((x != 0) and (x != 1)): # limit of map
            if ((state.map[y][x-1]== 1) and (state.map[y][x-2]==1)): # west check
                map2 = copy.deepcopy(state.map)
                map2[y][x] = 1
                map2[y][x-1] = 0
                map2[y][x-2] = 0
                new_holes = [[x-1,y],[x-2,y]]
                holes = copy.deepcopy(state.holes)
                for ho in new_holes:
                    holes.append(ho)  

                holes.remove([x,y])        
                to_be_added.append(State( holes, map2, depth, parent))    # add child to temp list
    while len(to_be_added) != 0:
        add_to_frontier = to_be_added.pop(random.randrange(0, len(to_be_added))) # randomly add to frontier list
        frontier.append(add_to_frontier)
       
    
def bfs_search(frontier): #bfs
    current_depth = 0 # current search depth
    expanded_counter = 0 # counter for expanded nodes
    frontier_max = 0 # max frontier length
    start = time.time() # starting time
    best_solution_in_our_hand = initial_state # best solution for t=0
    while (True): # loop
        print("\n")
        print(len(frontier))
	    # if condition for update max frontier length 
        if(len(frontier) > frontier_max): frontier_max = len(frontier)
        time_processed = time.time() - start # time update
        if time_processed >= time_limit: # time limit check
            return best_solution_in_our_hand, time_processed, expanded_counter,frontier_max
        state = frontier.pop(0) # frontier pop
        if(state.map == goal_state_map): # if con. for goal state check
            print("Successful!!!!")
            return state, time_processed, expanded_counter, frontier_max
        else:  
            if(state.depth == current_depth): # if depth is same
                state.print_board()      # print board 
            else:
                best_solution_in_our_hand = state #update best solution
                print("---->")
                state.print_board()
                current_depth += 1 
            expand_state(state,frontier) # expand state
            expanded_counter += 1


def dfs_search(frontier): # dfs
    current_depth = 0 # current search depth
    expanded_counter = 0 # counter for expanded nodes
    frontier_max = 0 # max frontier length
    start = time.time() # starting time
    best_solution_in_our_hand = initial_state # best solution for t=0
    while (True):
        print("\n")
        print(len(frontier))
        if(len(frontier) > frontier_max): frontier_max = len(frontier) 
        time_processed = time.time() - start
        if time_processed >= time_limit:
            return best_solution_in_our_hand, time_processed, expanded_counter, frontier_max
        state = frontier.pop(len(frontier)-1) # frontier pop from end of the list
        if(state.map == goal_state_map): # goal state check
            print("Successful!!!!")
            state.print_board() 
            return state, time_processed, expanded_counter, frontier_max
        else:   
            if(state.depth == current_depth):
                state.print_board()
                pass
            else:
                print("---->")
                if(state.depth > best_solution_in_our_hand.depth): # best solution update
                    best_solution_in_our_hand = state
                state.print_board()
                current_depth += 1
            expand_state(state,frontier) # expand state function
            expanded_counter += 1


def iterative_deepening_search(frontier): # iterative deepening
    current_depth = 0 # current search depth
    expanded_counter = 0 # counter for expanded nodes
    frontier_max = 0 # max frontier length
    start = time.time() # starting time
    best_solution_in_our_hand = initial_state # best solution for t=0
    depth_limit = 0 # depth limit for iteration
    while (True):
        print("\n")
        print("frontier length: " + str(len(frontier))) 
        if(len(frontier) > frontier_max): frontier_max = len(frontier)
        time_processed = time.time() - start
        if time_processed >= time_limit: # time check
            return best_solution_in_our_hand, time_processed, expanded_counter, frontier_max
        
        state = frontier.pop(len(frontier)-1) # pop from end of the list
        if(state.map == goal_state_map): # goal state check
            print("Successful!!!!")
            state.print_board()
            return state, time_processed, expanded_counter,frontier_max
        else:    
            state.print_board()
            if(state.depth == depth_limit): # depth limit check
                if(state.depth > best_solution_in_our_hand.depth):
                    best_solution_in_our_hand = state
                if(len(frontier)!=0): # is frontier empty or not? 
                    continue
                else:
                    print("\n\n*********iterative restart*******\n\n")
                    print("*********depth limit: " + str(depth_limit) + "**********\n")
                    depth_limit += 1 # depth limit increment
                    frontier.clear() # frontier clear to restart
                    frontier.append(initial_state) 
                    continue 
            current_depth += 1
            expand_state(state,frontier) # expand state 
            expanded_counter += 1

def random_dfs_search(frontier):
    current_depth = 0 # current search depth
    expanded_counter = 0 # counter for expanded nodes
    frontier_max = 0 # max frontier length
    start = time.time() # starting time
    best_solution_in_our_hand = initial_state # best solution for t=0
    while (True):
        print("\n")
        time_processed = time.time() - start
        #print(time_processed)
        if(len(frontier) > frontier_max): frontier_max = len(frontier)
        if time_processed >= time_limit:
            return best_solution_in_our_hand, time_processed, expanded_counter,frontier_max
        #print("\n")
        #print(len(frontier)) 
        state = frontier.pop(len(frontier)-1)
        if(state.map == goal_state_map):
            print("Successful!!!!")
            state.print_board()
            return state, time_processed, expanded_counter, frontier_max
        else:   
            if(state.depth == current_depth):
                state.print_board()
            else:
                print("---->")
                state.print_board()
                if(state.depth > best_solution_in_our_hand.depth):
                    best_solution_in_our_hand = state
                current_depth += 1
            expand_state_RANDOM(state,frontier) 
            expanded_counter += 1

def heuristic_dfs_search(frontier): 
    current_depth = 0 # current search depth
    expanded_counter = 0 # counter for expanded nodes
    frontier_max = 0 # max frontier length
    start = time.time() # starting time
    best_solution_in_our_hand = initial_state # best solution for t=0
    while (True):
        print("\n")
        print(len(frontier)) 
        time_processed = time.time() - start
        if(len(frontier) > frontier_max): frontier_max = len(frontier)
        if time_processed >= time_limit:
            return best_solution_in_our_hand, time_processed, expanded_counter, frontier_max
        state = frontier.pop(len(frontier)-1)
        if(state.map == goal_state_map):
            print("Successful!!!!")
            state.print_board()
            return state, time_processed, expanded_counter, frontier_max
        else:   
            if(state.depth == current_depth):
                state.print_board()
            else:
                print("---->")
                state.print_board()
                if(state.depth > best_solution_in_our_hand.depth):
                    best_solution_in_our_hand = state
                if(state.depth >= 29):
                    print("\n")
                    state.print_board()
                current_depth += 1
            expand_state_HEURISTIC3(state,frontier)
            expanded_counter += 1

def print_result(result,time_spent, expanded_node, frontier_max):
    if(result.map != goal_state_map):
        remaining_pegs = 33 - len(result.holes)
        print("\n\nSub-optimum Solution Found with " + str(remaining_pegs) +  " remaining pegs")
    else:
        print("\nOptimum solution found.")
    print("Time spent: " + str(int(time_spent/60)) + " minutes")
    print(str(expanded_node) + " nodes expanded during the search.")
    print("Maximum " + str(frontier_max) + " nodes stored in the memory during the search.")

def find_path(state,path):
    if state.depth == 0:
        i = len(path)-1
        print("\n\n////////////////////////////\n\n")
        print("          SOLUTION            \n\n ")
        print("////////////////////////////\n\n")
        while i >= 0:
            print("")
            path[i].print_board()
            i -= 1
            if(i < 0):
                return
    path.append(state.parent)
    find_path(state.parent,path)

path = []

methods = ["a. Breadth-First Search", "b. Depth-First Search", "c. Iterative Deepening Search",
            "d. Depth-First Search with Random Selection", "e. Depth-First Search with a Node Selection Heuristic"
            ]

while True:
    print("\n")
    print("<<<PEG SOLITAIRE SOLVER AI>>>")
    print("-----------------------------")
    for item in methods: 
        print(item)
    path.clear()
    print("\n")
    method = input("Select a method: ")  
    method.lower() 
    time_limit = int(input("Type your time limit (in minutes): ")) * 60 
    if(method == "a"):
        result, time_spent, expanded_node, frontier_max = bfs_search(frontier_list)
        path.append(result)
        find_path(result,path)  
        print_result(result, time_spent, expanded_node, frontier_max) 
    if(method == "b"):
        result, time_spent, expanded_node, frontier_max = dfs_search(frontier_list)  
        path.append(result)
        find_path(result,path)
        print_result(result, time_spent, expanded_node, frontier_max)
    if(method == "c"):
        result, time_spent, expanded_node, frontier_max = iterative_deepening_search(frontier_list) 
        path.append(result)
        find_path(result,path)
        print_result(result, time_spent, expanded_node, frontier_max)
    if(method == "d"):
        result, time_spent, expanded_node, frontier_max = random_dfs_search(frontier_list)
        path.append(result)
        find_path(result,path) 
        print_result(result, time_spent, expanded_node, frontier_max)
    if(method == "e"):
        result, time_spent, expanded_node, frontier_max = heuristic_dfs_search(frontier_list)
        path.append(result)
        find_path(result,path)
        print_result(result, time_spent, expanded_node, frontier_max)
    
            
#result = bfs_search(frontier_list)
#result = dfs_search(frontier_list)
#result = iterative_deepening_search(frontier_list)
#result = random_dfs_search(frontier_list)
#result = heuristic_dfs_search(frontier_list)




    










