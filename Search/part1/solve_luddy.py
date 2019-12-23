#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [Rushikesh Gawande, Ruta Utture, Sumeet Sarode]
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import sys

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
MOVES_L = { "A": (-2, -1), "B": (-2, 1), "C": (2, -1), "D": (2, 1), "E": (-1, -2), "F": (-1, 2), "G": (1, -2), "H": (1, 2)}

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1+1:ind2] + (list[ind1],) + list[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successors(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]

# return a list of possible successor states
def successors_C(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    if sys.argv[2]=='circular':
            return [ (swap_tiles(state, empty_row, empty_col, (empty_row+i)%4, (empty_col+j)%4), c) \
             for (c, (i, j)) in MOVES.items() if valid_index((empty_row+i)%4, (empty_col+j)%4) ]
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES.items() if valid_index(empty_row+i, empty_col+j) ]

# return a list of possible successor states
def successors_L(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVES_L.items() if valid_index(empty_row+i, empty_col+j) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0

def function(x):
    goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
    n = len(x)
    h_score = 0
    for i in range(n) :
        p = x.index(i)
        q = goal.index(i)
        if p!=q:
            h_score = h_score+1
    return h_score
    
# The solver! - using A* now
def solve(initial_board):
    visited = []
    q = PriorityQueue()
    q.put((function(initial_board), (initial_board, "")))
    while not q.empty():
        (a, (state, route_so_far)) = q.get()
        visited.append(state)
        for (succ, move) in successors( state ):
            if is_goal(succ):
                return( route_so_far + move )
            g_score = len(route_so_far + move)
            f_score = g_score + function(succ)
            if succ not in visited:
                q.put((f_score, (succ, route_so_far + move )))
    return False

# The solver! - using A* now
def solve_C(initial_board):
    visited = []
    q = PriorityQueue()
    q.put((function(initial_board), (initial_board, "")))
    while not q.empty():
        (a, (state, route_so_far)) = q.get()
        visited.append(state)
        for (succ, move) in successors_C( state ):
            if is_goal(succ):
                return( route_so_far + move )
            g_score = len(route_so_far + move)
            f_score = g_score + function(succ)
            if succ not in visited:
                q.put((f_score, (succ, route_so_far + move )))
    return False

# The solver! - using A* now
def solve_L(initial_board):
    visited = []
    q = PriorityQueue()
    q.put((function(initial_board), (initial_board, "")))
    while not q.empty():
        (a, (state, route_so_far)) = q.get()
        visited.append(state)
        for (succ, move) in successors_L( state ):
            if is_goal(succ):
                return( route_so_far + move )
            g_score = len(route_so_far + move)
            f_score = function(succ)
            if succ not in visited:
                q.put((f_score, (succ, route_so_far + move )))
    return False

def inversion(start_state):
        row=start_state.index(0)//4
        state1=[]
        for a in start_state:
                if a!=0:
                        state1.append(a)
        inv = 0
        for i in range (len(state1)-1):
                for j in range(i+1,len(state1)):
                        if state1[i]>state1[j]:
                                inv+=1
        if inv%2 == 1 and row%2==0  or inv%2 == 0 and row%2==1:
                return True
        else:
                return False

# test cases
if __name__ == "__main__":
    
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]
        
    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))
    print("Solving...")
    
    if inversion(start_state):
        if (sys.argv[2] == "original"):
            route = solve(tuple(start_state))
        elif (sys.argv[2] == "circular"):
            route = solve_C(tuple(start_state))
        elif (sys.argv[2] == "luddy"):
            route = solve_L(tuple(start_state))
            
        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)
    else:
        print ('Inf')
