# REPORT
# Part 1: IJK
The game has two players in it and can be played in two modes. In the deterministic mode, the firt letter is placed on the first tile of the board. In the Non-deterministic IJK, the new a or A is added to a random position on the board. The rest of the rules remain the same for the two variants. Anyone player wins the game by reaching the letter K or k.

In this part we had to design an AI which  will think and play the game logically as the human mind does. For this, we used Adversarial search method, also known as Minimax algorithm. We used this algorithm to find the best possible moves from the available set of moves. While implementing the Minimax algorithm, we always considerd the AI to be the maximum player. The maximum depth till which we are traversing the game tree is 12. To decrease the computational time and the space complexity, we implemented alpha-beta pruning to reduce the state space. It drastically reduced the time taken for execution. We had to design a heuristic function to determine whic is the best possible move. 
#The heuristic function that we found to give the best solution is “Number of empty tiles raised to the maximum letter.”

There are various heuristics that we tried and found the current heuristic to be performing better than the others. The heuristics that we tried are as follows:

i) The distance from the current state to the goal state .i.e. the difference between the maximum letter of the state and the letter K or k.

ii) The penalty of all the elements of the board. The penalty is calculated by checking the neighbours of all the elements. If the neighbours are not the same, the penalty is incremented.

iii) The penalty raised to the maximum letter.

iv) Number of empty tiles.

v)  Difference between the maximum letter of the AI and the maximum letter of the opponent.

vi) Number of merges possible.

vii) Attaining the maximum letter for self and the lowest possible for the opponent.

# Part 2: Horizon Finding

The basic aim of this part is to identify for each column of the image the row value such that it forms a line that separates the mountain from the sky. We are asked to solve this using bayes net, viterbi algorithm and by human feedback.

For the first part of the problem, we are supposed to use Bayes Net to find a the most probable row values and give that as input to draw a line on the image. After using Variable Elimination, we  foound that for each column, the row associated with the maximum value is the most probable row. So, by taking the row index where the maximum value of the column is present and using it as input to draw the line we are able to draw a line that divides the mountain from the horizon. But it performed poorly since the probability used is dependent on the edge strength and there can be some features in the image that can be strong enough in contrast but not necessarily a mountain.

The second part of the problem is to use viterbi algorithm to optimize the previous setting and helping us calculate the ridge. Viterbi helps us find the most likely sequence of states. Assuming that each row index is a hidden state and the column index is the observed state, we found for each column the most likely row value. Since the probabilities depended on the previous states, it found the overall maximum probable path, unlike in Bayes Net and gave us a much better result. But still in some images, the line would form on the most contrasting path of the image and not the mountains in particular.

The third part deals with the issue of the mountain being more in the background or not as contrasting. To  resolve this we need to add some external/human entered input to help identify the mountain. Using the same viterbi algorithm, we're assigning the point which the user identified as lying on the horizon with maximum probability so whatever path the algorithm takes, it has to go through that point.

In the Viterbi algorithm, We assigned start probability in such a way that it considers the columns in an increasing manner of index. So we assigned the highest probability to column 0 and then kept decreasing the value in a uniform manner. For emission probability, we assigned the scaled edge strenghts as the probability since it correctly gives us the probability of observing a column from a row index. For tansition prbability, initially we assigned probability of going from one row to the next from one  column to another to be highest when the row values are same and it keeps decreasing as the value of the rows start to differ drastically. But this didn't gave us as good of a result as we were expecting. When we changed the transition probability to being in descending order for all hidden states, we were able to get a better result.
