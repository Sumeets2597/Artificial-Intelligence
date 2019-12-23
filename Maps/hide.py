#!/usr/local/bin/python3
#
# hide.py : a simple friend-hider
#
# Submitted by : [Name: SUMEET SARODE
#		  USERNAME: ssarode]
#
# Based on skeleton code by D. Crandall and Z. Kachwala, 2019
#
# The problem to be solved is this:
# Given a campus map, find a placement of F friends so that no two can find one another.
#

import sys
import time

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().split("\n")]

# Count total # of friends on board
def count_friends(board):
    return sum([ row.count('F') for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    return board[0:row] + [board[row][0:col] + ['F',] + board[row][col+1:]] + board[row+1:]

#Check for & or F:
def check(board,i,j):
        if board[i][j]=='.':
                for a in range(i,-1,-1):
                        if board[a][j] in '#@&':
                                break
                        if board[a][j]=='F':
                                return False
                                break
                for a in range(i,len(board)):
                        if board[a][j] in '#@&':
                                break
                        if board[a][j]=='F':
                                return False
                                break
                for a in range(j,-1,-1):
                        if board[i][a] in '#@&':
                                break
                        if board[i][a]=='F':
                                return False
                                break
                for a in range(j,len(board[0])):
                        if board[i][a] in '#@&':
                                break
                        if board[i][a]=='F':
                                return False
                                break
                return True
        
# Get list of successors of given board state
def successors(board):
        return [ add_friend(board, r, c) for r in range(len(board)) for c in range(len(board[0])) if check(board,r,c)]

def is_goal(board):
    return count_friends(board) == K 

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    check=[]
    while len(fringe) > 0:
            check.append(fringe[-1])
            for s in successors( fringe.pop() ):

                    if is_goal(s):
                            return(s)
                    if s not in check:
                            fringe.append(s)
    return False

# Main Function
if __name__ == "__main__":
    IUB_map=parse_map(sys.argv[1])
    global K
    # This is K, the number of friends
    K = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(IUB_map) + "\n\nLooking for solution...\n")
    solution = solve(IUB_map)
    print ("Here's what we found:")
    print (printable_board(solution) if solution else "None")
