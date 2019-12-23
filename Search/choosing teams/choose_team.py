#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [ Rushikesh Gawande(rgawande)-Ruta Utture(rutture)-Sumeet Sarode(ssarode)]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
import itertools
from queue import PriorityQueue

def load_people(filename):
    people={}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [ float(i) for i in l[1:] ] 
    return people

# This function implements a greedy solution to the problem:
#  It adds people in decreasing order of "skill per dollar,"
#  until the budget is exhausted. It exactly exhausts the budget
#  by adding a fraction of the last person.
#
def approx_solve(people, budget):
        q=PriorityQueue()
        solution=()
        names=[]
        sub=[]
        for i in people:
                names.append(i)
        for i in range(1,len(names)+1):
                for a in list(itertools.combinations(names, i)):
                        if sum(people[p][1] for p in a)<=budget:
                                q.put((-1*sum(people[p][0] for p in a),a))
        if q.queue:
            (skills,sets)=q.get()
            skills=-skills
            for s in sets:
                solution += ( ( s, 1), )
            s = [solution,skills,sum(people[p][1] for p in sets)]
            return s
        else:
            return -1

if __name__ == "__main__":
        if(len(sys.argv) != 3):
                raise Exception('Error: expected 2 command line arguments')
        budget = float(sys.argv[2])
        people = load_people(sys.argv[1])
        s=approx_solve(people, budget)
        if s != -1:
            print("Found a group with %d people costing %f with total skill %f" % \
                   ( len(s[0]), s[2], s[1]))
            for sol in s[0]:
                print("%s %f" % sol)
        else:
            print("Inf")
