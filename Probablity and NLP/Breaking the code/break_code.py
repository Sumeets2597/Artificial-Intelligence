#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: Sumeet(ssarode), Rushikesh(rgawande), Ruta(rutture)
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#


import random
import sys
import encode
import string as st
import numpy as np

def score_dict(corpus):
    d={}
    for i in range(len(corpus)-1):
        if corpus[i]+corpus[i+1] not in d:
            d[corpus[i]+corpus[i+1]]=corpus.count(corpus[i]+corpus[i+1])  
            
    return d

def decrypt(cipher,text):
    d,decrypted,a={},'',st.ascii_lowercase
    for i in range(len(cipher)):
        d[a[i]]=cipher[i]
    
    for i in text:
        if i in d:
            decrypted+=d[i]
        else:
            decrypted+=" "
    return decrypted

def score(d):
    d1=" "+d
    s=0
    d_d=score_dict(d1)
    for i in d_d:
        # The scoring is referred from https://mlwhiz.com/blog/2015/08/21/mcmc_algorithm_cryptography/
        if i in scoring_dict:
            s+=d_d[i]*np.log(scoring_dict[i])

    return s

def rearrange(text,pos):
    n,c=4,''
    for i in range(0,len(text),n):
        for j in pos:
            c+=text[i:i+n][j]
    return c
               
def gen_cipher(cipher):
    x=list(cipher)
    a,b=random.randint(0,25),random.randint(0,25)
    x[a],x[b]=x[b],x[a]
    
    if ''.join(x)==cipher:
        return gen_cipher(cipher)
    return ''.join(x)
    
def break_code(string, corpus):
    current=st.ascii_lowercase
    curr_re=random.sample(range(4),4)
    flag,best_score,best_key,best_re=True,0,current,curr_re
    
    for i in range(60000): 
        if flag:
            encrypted=rearrange(string,curr_re)
            current_d=decrypt(current,encrypted)
            curr_score=score(current_d)    
            flag=False
        
        proposed=gen_cipher(current)
        proposed_re=random.sample(range(4),4)
        encrypted=rearrange(string,proposed_re)
        proposed_d=decrypt(proposed,encrypted)
        proposed_score=score(proposed_d)
        
        keys,re,scr=[best_key,current,proposed],[best_re,curr_re,proposed_re],[best_score,curr_score,proposed_score]
        if np.argmax(scr)!=0:
            best_key,best_re,best_score=keys[np.argmax(scr)],re[np.argmax(scr)],scr[np.argmax(scr)]
            
        p=np.exp(proposed_score-curr_score)
        prob=p if p<=1 else 1
        if prob>random.uniform(0,1):
            current=proposed
            curr_re=proposed_re
            flag=True

    best_encrypted=rearrange(string,best_re)
    return decrypt(best_key,best_encrypted)

if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    while len(encoded)%4!=0:
        encoded+=" "
    global scoring_dict
    scoring_dict=score_dict(corpus)
    
    decoded = break_code(encoded, corpus)

    with open(sys.argv[3], "w") as file:
        print(decoded, file=file)
