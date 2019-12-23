#!/usr/local/bin/python3
import sys
from queue import PriorityQueue

def neighbors(city1):
        n=[]
        d=[]
        s=[]
        for i in intercity:
                if i[0][0]==city1:
                        n.append(i[0][1])
                        d.append(i[1])
                        s.append(i[2])
        return n,d,s

def mpg(start,end):
        q=PriorityQueue()
        visited=[]
        q.put((0,([start],0,0,0)))
        while not q.empty():
                (key,(paths,d,t,g))=q.get()
                city1=paths[-1]
                adj,dist,sp=neighbors(city1)
                for i in range(len(adj)):
                        if adj[i] not in paths:
                                a1=[]
                                for abc in paths:
                                        a1.append(abc)
                                a1.append(adj[i])
                                mpg=400*sp[i]*((1-(sp[i]/150))**4)/150
                                gal=dist[i]/mpg
                                q.put((g+gal,(a1,d+dist[i],t+(dist[i]/sp[i]),g+gal)))
                                if end in a1:
                                        p = ""
                                        for c in a1:
                                            p += c+" "
                                        p = p[:-1]
                                        s = [len(a1)-1,d+dist[i],round(t+(dist[i]/sp[i]),4),round(g+gal,4),p]
                                        return s
        return -1

def segments(start,end):
        q=PriorityQueue()
        visited=[]
        q.put((0,([start],0,0,0)))
        while not q.empty():
                (key,(paths,d,t,g))=q.get()
                city1=paths[-1]
                adj,dist,sp=neighbors(city1)
                for i in range(len(adj)):
                        if adj[i] not in paths:
                                a1=[]
                                for abc in paths:
                                        a1.append(abc)
                                a1.append(adj[i])
                                mpg=400*sp[i]*((1-(sp[i]/150))**4)/150
                                gal=dist[i]/mpg
                                q.put((len(a1)-1,(a1,d+dist[i],t+(dist[i]/sp[i]),g+gal)))
                                if end in a1:
                                        p = ""
                                        for c in a1:
                                            p += c+" "
                                        p = p[:-1]
                                        s = [len(a1)-1,d+dist[i],round(t+(dist[i]/sp[i]),4),round(g+gal,4),p]
                                        return s
        return -1

def time(start,end):
        q=PriorityQueue()
        visited=[]
        q.put((0,([start],0,0,0)))
        while not q.empty():
                (key,(paths,d,t,g))=q.get()
                city1=paths[-1]
                adj,dist,sp=neighbors(city1)
                for i in range(len(adj)):
                        if adj[i] not in paths:
                                a1=[]
                                for abc in paths:
                                        a1.append(abc)
                                a1.append(adj[i])
                                mpg=400*sp[i]*((1-(sp[i]/150))**4)/150
                                gal=dist[i]/mpg
                                q.put((t+(dist[i]/sp[i]),(a1,d+dist[i],t+(dist[i]/sp[i]),g+gal)))
                                if end in a1:
                                        p = ""
                                        for c in a1:
                                            p += c+" "
                                        p = p[:-1]
                                        s = [len(a1)-1,d+dist[i],round(t+(dist[i]/sp[i]),4),round(g+gal,4),p]
                                        return s
        return -1

def distance(start,end):
        q=PriorityQueue()
        visited=[]
        q.put((0,([start],0,0,0)))
        while not q.empty():
                (key,(paths,d,t,g))=q.get()          
                city1=paths[-1]
                adj,dist,sp=neighbors(city1)
                for i in range(len(adj)):
                        if adj[i] not in paths:
                                a1=[]
                                for abc in paths:
                                        a1.append(abc)
                                a1.append(adj[i])
                                mpg=400*sp[i]*((1-(sp[i]/150))**4)/150
                                gal=dist[i]/mpg
                                q.put((d+dist[i],(a1,d+dist[i],t+(dist[i]/sp[i]),g+gal)))
                                if end in a1:
                                        p = ""
                                        for c in a1:
                                            p += c+" "
                                        p = p[:-1]
                                        s = [len(a1)-1,d+dist[i],round(t+(dist[i]/sp[i]),4),round(g+gal,4),p]
                                        return s
        return -1

if __name__ == "__main__":
        city=[]
        with open('city-gps.txt', 'r') as file:
                for line in file:
                        try:
                                name,lat,long=line.split(' ')
                                city.append((name,(float(lat),float(long))))
                        except:
                                if len(line.split(' '))==1:     
                                        city.append((line[:-1],(0,0)))
                                if len(line.split(' '))==2:
                                        name,lat=line.split(' ')
                                        city.append((name,(float(lat),0)))
        intercity=[]
        with open('road-segments.txt', 'r') as file:
                for line in file:
                        city1,city2,dist,spd,hw=line.split(' ')
                        intercity.append(((city1,city2),int(dist),int(spd),hw[:-1]))
                        intercity.append(((city2,city1),int(dist),int(spd),hw[:-1]))

        if(len(sys.argv) != 4):
            raise Exception('Error: expected 3 command line arguments')

        start_city = sys.argv[1]
        end_city = sys.argv[2]
        c = sys.argv[3]
        if c == "segments":
            sol=segments(start_city,end_city)
            if sol != -1:
                for s in sol:
                    print("%s " %s,end="")
            else:   
                print("Inf")
        elif c == "distance" :
            sol=distance(start_city,end_city)
            if sol != -1:
                for s in sol:
                    print("%s " %s,end="")
            else:
                print("Inf")
        elif c == "time" :
            sol=time(start_city,end_city)
            if sol != -1:
                for s in sol:
                    print("%s " %s,end="")
            else:    
                print("Inf")
        elif c == "mpg":
            sol=mpg(start_city,end_city)
            if sol != -1:
                for s in sol:
                    print("%s " %s,end="")
            else:
                print("Inf")
                                         

