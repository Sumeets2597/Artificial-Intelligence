# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 21:02:22 2019

@author: Rushikesh Gawande, Ruta Utture, Sumeet Sarode
"""
import os
import sys
import collections
import numpy as np

path = sys.argv[1]
paths=[]
for i in os.listdir(path):
    paths.append(path+'/'+i+'/')
    
sf = os.listdir(paths[1])
hf = os.listdir(paths[0])

scount = 0
ss = ''
for i in sf:
    with open(paths[1]+i,encoding='latin1') as f:
        scount+=1
        for line in f :
            ss+=line           
hcount = 0
hs = ''
for i in hf:
    with open(paths[0]+i,encoding='latin1') as f:
        hcount+=1
        for line in f :
            hs+=line           

p_spam = scount/(scount+hcount)
p_ham = hcount/(scount+hcount)
spam = ss.lower().split()
ham = hs.lower().split()

ds = collections.Counter(spam)
dh = collections.Counter(ham)

s1 = sum([ds[i] for i in ds])
pw_spam = {}
for i in ds:
    if i not in pw_spam:
        pw_spam[i] = ds[i]/s1
        
s2 = sum([dh[i] for i in dh])
pw_ham = {}
for i in dh:
    if i not in pw_ham:
        pw_ham[i] = dh[i]/s2

test_path = sys.argv[2]+'/'
test_loc = os.listdir(test_path)
list1 = []
for i in test_loc:
    with open(test_path+i,"r",encoding='latin1') as f:
        s = ''
        for line in f:
            s+=line
        list1.append(s) 
           
prob = []
for i in list1:
    ps = 0
    ph = 0
    li = i.lower().split()
    for j in li:
        if j not in pw_spam:
            pw_spam[j]=0.5
        if j not in pw_ham:    
            pw_ham[j]=0.5
        ps-=np.log(pw_spam[j])
        ph-=np.log(pw_ham[j])
    ps-=np.log(p_spam)
    ph-=np.log(p_ham)
    
    if ps>ph:
        prob.append('spam')
    else:
        prob.append('notspam')

with open(sys.argv[3],"w") as f:
    for i in range(len(prob)):
        f.writelines(test_loc[i]+' '+prob[i]+'\n')
f.close()