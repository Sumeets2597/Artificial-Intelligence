#!/usr/local/bin/python3
#
# find_luddy.py : a simple maze solver
#
# Submitted by : [Name:SUMEET SARODE
#                             Usename:ssarode]
#
# Based on skeleton code by Z. Kachwala, 2019
#

import sys
import json

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().split("\n")]

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return (0 <= pos[0] < n  and 0 <= pos[1] < m)

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

	# Return only moves that are within the board and legal (i.e. on the sidewalk ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
def search1(IUB_map):        
        # Find my start position
        you_loc=[(row_i,col_i) for col_i in range(len(IUB_map[0])) for row_i in range(len(IUB_map)) if IUB_map[row_i][col_i]=="#"][0]
        fringe=[(you_loc,0)]
        visited=[]
        while fringe:                
                (curr_move, curr_dist)=fringe.pop()
                visited.append(curr_move)
                for move in moves(IUB_map, *curr_move):
                        if IUB_map[move[0]][move[1]]=="@":
                                visited.append(move)
                                visited.reverse()
                                ind=1
                                while ind<len(visited):
                                        if visited[ind][0]!=visited[ind-1][0] and visited[ind][1]!=visited[ind-1][1]:
                                                visited.remove(visited[ind])
                                                ind=1                                           
                                        elif (visited[ind][0]==visited[ind-1][0] and abs(visited[ind][1]-visited[ind-1][1])==1) or (visited[ind][1]==visited[ind-1][1] and abs(visited[ind][0]-visited[ind-1][0])==1):
                                                ind+=1
                                        else:
                                                visited.remove(visited[ind])
                                                ind=1
                                visited.reverse()
                                path=''
                                for i in range(1,len(visited)):
                                        if visited[i][0]==visited[i-1][0]+1 and visited[i-1][1]==visited[i][1]:
                                                path+='S'
                                        if visited[i][0]==visited[i-1][0]-1 and visited[i-1][1]==visited[i][1]:
                                                path+='N'
                                        if visited[i][1]==visited[i-1][1]+1 and visited[i-1][0]==visited[i][0]:
                                                path+='E'
                                        if visited[i][1]==visited[i-1][1]-1 and visited[i-1][0]==visited[i][0]:
                                                path+='W'                                
                                return str(curr_dist+1)+" "+path
                        else:
                                if move not in visited:
                                        fringe.append((move, curr_dist + 1))
                
# Main Function
if __name__ == "__main__":
        IUB_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution= search1(IUB_map)
        print("Here's the solution I found:")
 
        if solution == None:
                print('Inf')
        else:
                print(solution)
