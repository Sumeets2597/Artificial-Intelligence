###################################
# CS B551 Fall 2019, Assignment #3
#
# Your names and user ids: Sumeet S(ssarode), Rushikesh G(rgawande), Ruta U(rutture)
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import numpy as np
from collections import defaultdict
import operator


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    def __init__(self):
        self.labels = ['det', 'noun', 'adj', 'verb', 'adp', '.', 'adv', 'conj', 'prt', 'pron', 'num', 'x']
        self.label_count = dict.fromkeys(self.labels,0)  #Frequency of labels in total
        self.lookup = defaultdict(dict)             #Frequency of (label,word)
        self.trans_count = {}                       #Frequency of transmission from one label to another
        self.word_count = {}                        #Frequency of words in total
        self.prior_count = {}                       #Frequency of start words
        self.trans_prob = {}
        self.emiss_prob = defaultdict(dict)
        self.prior_prob = {}
        self.alpha = 10**(-20)
        
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):

        if model == "Simple":
            posterior = 1
            for word,label in zip(sentence,label):
                if word not in self.word_count:
                    if word[:-2] in self.word_count:
                        word = word[:-2]
                    elif word+'es' in self.word_count:
                        word = word+'es'
                    elif word+'s' in self.word_count:
                        word = word+'s'
                    else:
                        self.emiss_prob[label][word] = self.alpha
                if word not in self.emiss_prob[label]:
                    self.emiss_prob[label][word] = self.alpha
                posterior *= self.prior_prob[label]*self.emiss_prob[label][word]
            return  math.log(posterior+self.alpha)
        
        elif model == "Complex":
            posterior = 1
            for word,label in zip(sentence,label):
                if word not in self.word_count:
                    if word[:-2] in self.word_count:
                        word = word[:-2]
                    elif word+'es' in self.word_count:
                        word = word+'es'
                    elif word+'s' in self.word_count:
                        word = word+'s'
                    else:
                        self.emiss_prob[label][word] = self.alpha
                if word not in self.emiss_prob[label]:
                        self.emiss_prob[label][word] = self.alpha
                posterior *= self.prior_prob[label]*self.emiss_prob[label][word]
            return  math.log(posterior+self.alpha)
        
        elif model == "HMM":

            posterior = 1
            n = -1
            for word,label in zip(sentence,label):
                if word not in self.word_count:
                    if word[:-2] in self.word_count:
                        word = word[:-2]
                    elif word+'es' in self.word_count:
                        word = word+'es'
                    elif word+'s' in self.word_count:
                        word = word+'s'
                    else:
                        self.emiss_prob[label][word] = 0
                if n == -1:
                    posterior *= self.prior_prob[label]*self.emiss_prob[label][word]
                    n = label
                else:
                    posterior *= self.trans_prob[(n,label)]*self.emiss_prob[label][word]

            return  math.log(posterior+self.alpha)            
        
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        
        for i in data:
            prev_label = -1
            for j in range(0, len(i[0])):
                word = i[0][j]
                label = i[1][j]
                
                #frequency of start probability
                if j == 0 :
                    if label in self.prior_count:
                        self.prior_count[label] += 1
                    else:
                        self.prior_count[label] = 1
                

                #frequency of words in the data
                if word in self.word_count:
                    self.word_count[word] += 1
                else:
                    self.word_count[word] = 1
                
                #frequency of labels in the data
                self.label_count[label] += 1
                
                #updating the lookup table
                if word in self.lookup[label]:
                    self.lookup[label][word] += 1
                else:
                    self.lookup[label][word] = 1
                
                #updating transmission frequency between labels 
                if prev_label != -1:
                    t = (prev_label,label)
                    if t in self.trans_count:
                        self.trans_count[t] += 1
                    else:
                        self.trans_count[t] = 1
                prev_label = label

        #calculating emission probability
        for label in self.lookup:   
            summ = sum(self.lookup[label].values())
            for word in self.lookup[label]:
                self.emiss_prob[label][word] = float(self.lookup[label][word]/summ)     
        
        #calculating prior probability
        summ = sum(self.prior_count.values())
        for i in self.prior_count:
            self.prior_prob[i] = float(self.prior_count[i]/summ)

        #calculating transmission probability
        l = {}
        for i in self.trans_count:
            if i[0] not in l:
                l[i[0]] = 0
            l[i[0]] += self.trans_count[i]
        for i in self.trans_count:
                self.trans_prob[i] = float(self.trans_count[i]/l[i[0]])
        
            
        all_trans = [(x,y) for x in self.labels for y in self.labels]
        for i in all_trans:
            if i not in self.trans_prob:
                self.trans_prob[i] = self.alpha  

        pass

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    
    def simplified(self, sentence):
        pos = []
        for word in sentence:
            max_val = 0
            max_lab = 'noun'
            for label in self.lookup:
                if word in self.lookup[label]:
                    if max_val < self.lookup[label][word]:
                        max_val = self.lookup[label][word]
                        max_lab = label
            pos.append(max_lab)
        return pos

    def complex_mcmc(self, sentence):
        import random
        poss=[]
        for i in sentence:
            poss.append(random.choice(self.labels))        
        for iteration in range(1000):  
            
            for i in sentence:
                s,record=0,{}
                for label in self.labels:
                    if i in self.emiss_prob[label]:
                        s+=self.emiss_prob[label][i]
                        record[label]=s
                r=random.uniform(0,s)
                keys=list(record.keys())
                for j in range(len(keys)-1):
                    if record[keys[j]]<r<=record[keys[j+1]]:
                        poss[sentence.index(i)]=keys[j+1]
        return poss
    


    def hmm_viterbi(self, sentence):
        
        T = [{}]
        for l in self.labels:
            if sentence[0] not in self.emiss_prob[l]:
                self.emiss_prob[l][sentence[0]] = self.alpha
            T[0][l] = {"prob": self.prior_prob[l] * self.emiss_prob[l][sentence[0]], "prev": None}
     
        for t in range(1, len(sentence)):
            T.append({})
            for h in self.labels:
                if sentence[t] not in self.emiss_prob[h]:
                    self.emiss_prob[h][sentence[t]] = self.alpha

                max_trp = T[t-1][self.labels[0]]["prob"]*self.trans_prob[(self.labels[0],h)]
                prev = self.labels[0]
                for prev_st in self.labels[1:]:
                    tr_prob = T[t-1][prev_st]["prob"]*self.trans_prob[(prev_st,h)]
                    if tr_prob > max_trp:
                        max_trp = tr_prob
                        prev = prev_st
            
                maxp = max_trp * self.emiss_prob[h][sentence[t]]
                T[t][h] = {"prob": maxp, "prev": prev}                
        opt = []
    
        maxp = max(value["prob"] for value in T[-1].values())
        p = None
    
        for st, data in T[-1].items():
            if data["prob"] == maxp:
                opt.append(st)
                p = st
                break
    
        for t in range(len(T) - 2, -1, -1):
            opt.insert(0, T[t + 1][p]["prev"])
            p = T[t + 1][p]["prev"]
    
        return opt   

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

