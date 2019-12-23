#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: Sumeet Sarode(ssarode)-Rushikesh Gawande(rgawande)-Ruta Utture(rutture)

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import copy
import string

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game 
#
# This function should analyze the current state of the game and determine the 
# best move for the current player. It should then call "yield" on that move.

def next_move(game: Game_IJK)-> None:

        '''board: list of list of strings -> current state of the game
        current_player: int -> player who will make the next move either ('+') or -'-')
        deterministic: bool -> either True or False, indicating whether the game is deterministic or not
        '''


        board = game.getGame()
        player = game.getCurrentPlayer()
        deterministic = game.getDeterministic()
        d={'+':True , '-':False }

        #Defining max depth till which the minmax tree is to be traversed
        max_depth=12
        
        def heuristic(state):
                uc,lc=' '+string.ascii_uppercase,' '+string.ascii_lowercase
                c=36-len([j for i in state for j in i if j in string.ascii_letters])
                if d[player]:
                        try:    
                                return c**uc.index(max([j for i in state for j in i if j in string.ascii_uppercase]))
                        except:
                                return c
                else:
                        try:
                                return c**lc.index(max([j for i in state for j in i if j in string.ascii_lowercase]))
                        except:
                                return c
                
#Store the current state with the movement and the children in lists        
        def child(current):                
                d,c=[],[]
                for i in 'UDLR':
                        s=copy.deepcopy(current)
                        s.makeMove(i)
                        c.append(s.getGame())
                        d.append(s)
                return c,d

#Check for the termination condition
        def termination(state):
                return max([j for i in state for j in i if j in string.ascii_letters]) in 'Kk'

#Max player's chance
        def maximize(board,state,alpha,beta,depth):
                if termination(board) or depth==max_depth:
                        return heuristic(board)

                # best value gives the best value from all the children which is first initialized to the worst possible value
                best = float('-inf')
                children,states=child(state)
                for i in range(len(children)):              
                    val = minimize(children[i],states[i],alpha, beta,depth+1)

                    #If the alpha value is greater than the beta value, prune the tree from that node
                    if beta<=max(alpha,max(best, val)):  
                        break 
                return best  

#Min player's chance
        def minimize(board,state,alpha,beta,depth):
                if termination(board) or depth==max_depth:
                        return heuristic(board)
                # best value gives the best value from all the children which is first initialized to the worst possible value
                best = float('inf')
                children,states=child(state)
                for i in range(len(children)):              
                    val = maximize(children[i],states[i],alpha, beta,depth+1)

                    #If the alpha value is greater than the beta value, prune the tree from that node
                    if min(alpha,min(best,val))<=alpha:  
                        break 
                return best                        

        l1,d1=child(game)
        h=[]

        #calling the minimum player's chance for each of the child node.
        for i in range(len(l1)):
                h.append(minimize(l1[i],d1[i],float('-inf'),float('inf'),1))

        #The child that gives the maximum value will be selected for the next move
        yield 'UDLR'[h.index(max(h))]
