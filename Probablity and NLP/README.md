# Part 1

We implemented the POS tagging in which we were supposed to mark every word in a sentence with its correct part of speech. We had a dataset of Brown Corpus and we had to implement Bayesian Nets, Viterbi and MCMC using Gibbs Sampling. 
We calculated first the prior probability which is the probabilty of a label occuring at the start of the sentence. We maintained a lookup which had all the frequency of the words with respect to its labels. We made a list of all the labels which exist and also kept the track of transitions. We defined the transition probability as the probability of transition from one POS label to another. We calculated all the possible combinations of transitions and we calculated the probability for it. We defined the emission probability as the probability of the word for a particular label. 

Bayesian Nets: 
We had to implement Bayes net to find the all part of speech for each word in the given sentence. We considered each word and probability of each word for all 12 possibilities of part of speech. We considered the max value of the probability and selected that label as the final label for respective word. It was just a baseline model which worked and performed average.

Viterbi:
The second part of the problem is to use viterbi algorithm to optimize the previous setting and helping us calculate the suitable probability.  Viterbi helps us find the most likely sequence of states. Viterbi considers three probabilities, start, emission and transition and combines all these probabilities to give best label sequence. Since the probabilities depended on the previous states, unlike in Bayes Net and gave us a much better result. 

MCMC using Gibbs Sampling:
First we considered random labels for all the words of the sentence. Then we performed 1000 iterations on each word of a sentence. We calculated cumulative emission probability of each label for that word. We decided a particular label for that word by tossing a coin.

Problems:
when any new word came which is not present in the training corpus, we have set their probability to a very small value 1e-20. While calculating emission probability of such words we are assigning its value as 0. In Viterbi we have assigned emission value and probability value of states as 1e-20 if it is zero.

# Part 2

The main aim was to decipher an intercepted message which was encrypted by using two types of encryption methods: Rearrangement and Replacement. To decipher the message, we used the Metropolis-Hastings algorithm.
The corpus given is the set of valid English words. A scoring dictionary is made from it. The keys of the dictionary is the combination of two consecutive letters along with the counts of the combination in the corpus. This dictionary is used as the scoring parameter for the documents decrypted using the keys in each iterations.

First, the cipher key is initialized to the sequential combination of the alphabets from a to z. The rearrangement key is generated randomly by shuffling the list from 0 to 4. The document is rearraged using this rearrangement key and the score is calculated on this document. A proposed key is produced by swapping the elements of two random positions. The rearrangement key is the random shuffle of the list with a range of 4. The score is calculated for these proposed keys. 
The state is changed to the proposed directly if the proposed score is greater than the current state score. If the score of the proposed state is less than the current score, the state is changed with a probability equal to the proposed score divided by the current score. And compare it with the coin toss probability. 

The score of the document is calculated in the following ways:
1.	Dictionary of the current document is created the same way as the scoring dictionary.
2.	For each combination of two letters present in both, the scoring parameter and the document dictionary, the product of the count of the combination and the log of the value of that key in the scoring parameter is added in the document score.
The probability of the document was to be counted, but due to the very small values of the scoring parameters, the document score was getting reduced to almost 0. Thus the logarithmic method was used.

The outputs for the 4 encrypted documents are uploaded in the output folder.The time taken by each document on our local machines are:  

Encrypted 1(15 mins)

Encrypted 2(12 mins)

Encrypted 3(13 mins)

Encrypted 4(16 mins)

# Part 3
So our main task was to implement the Naive Bayes classifier to determine whether the given mail is a spam or not. We first read all the mails from training set seperately as spam and not spam. Then we calculated the spam probability which is ratio of no of spam mails to total no of mails. Similarly not spam probability was also calculated. After that, we split the mails to get the bag of words and counted the occurences of each word in spam mails as well as in not spam mails. From the word count, we calculated the probability of word given spam & probability of word given not spam. Thus, at the end of the training we had one dictionary with probability of word given spam & one dictionary with probability of word given not spam respectively and also the values of spam probability and not spam probability.

Now, we read all the testing mails and collected everthing in a single string. Then we split it to get the bag of words for testing mails. In each iteration, we multiplied the word given spam probability each time for every word and the when all words were done for one email, we multiplied the spam probabilty at the end. Same thing was done for the not spam probability. If the spam given word probability was greater than the not spam given word probability, then it is labelled as spam, else its labelled as not spam.

One problem we faced was when a new word came in testing mail, and it was not present in the bag of words we got from the training, it was giving a key error because it was not present in any dictionary of probabilities. To handle that, we assigned the fixed equal value of 0.5 to both word given spam probability and word given ham probability. The other problem we faced was as the value of probabilities were too low and we were multiplying it, it was resulting in more low value which made our model biased towards one label and resulting in very low accuracy. So we handled this by taking log values and adding it instead of multiplying the probabilities. This resolved the problem and gave a significant increase in accuracy. We also tried to filter the words we were considering while training by removing special characters and all the words above certain length but then it was reducing our accuracy because those special characters and long web links were mostly part of spam emails. So then we removed all the filtering and took all the words available in training mails. Lastly the implementation was too slow because we were using os.walk so it was taking too much time just to read emails, hence we switched to os.listdir which made the process like 5x faster. 
