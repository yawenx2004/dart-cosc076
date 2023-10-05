Yawen Xue\
COGS 44\
PS3 - Chess\
1 Oct. 23
# Intro
Disclaimer: Having nearly lost to RandomAI.py several times, I don't think I'm the best person to comment on the intelligence of chess AI's. But here we go anyway!
# Code Design and Implementation
## MinimaxAI
My minimax implementation includes four functions. The function choose_move() calls minimax(). In turn, minimax() evaluates best scores based on material_value_heuristic().\
\
Minimax() is recursive, looping until the base case is reached as determined by cutoff_test(), which returns True when the game ends or when the depth limit has been reached. During the maximizing player's turn, minimax() returns the move that results in the highest score; during the minimizing player's turn, minimax() returns the move with the lowest score.\
\
MinimaxAI takes a while to deliberate (relatively high runtime complexity), at one point taking 1 minute 47 seconds (although at other times it makes very quickly, especially when I'm one step away from capturing the king). This makes sense, as it loops through a lot of states.

Upon my first run of my minimax algorithm (at depth 5), I was skeptical -- the opponent neither reacted to my moves nor made any attempt to approach my side of the board, instead settling for moving its rook back and forth between h8 and h7. When my knight arrived at its side of the board, it just let me capture a pawn and a rook, even though there were plenty of chess pieces nearby that could've captured my knight in a single step. It sent over a bishop to threaten my king with no regard for my own bishop that was a single step away and captured it immediately. At one point, it even allowed me to capture the queen without any (readily-available) retaliation. However, despite its astonishing willingness to lose pieces, it's  a lot harder to beat than RandomAI -- it took around 100 moves to beat MinimaxAI, while 50 were sufficient for Random AI.\
\
MinimaxAI has the advantage of being unpredictable. While RandomAI is very responsive and consistently makes moves to avoid losing pieces (as it seems to value all the pieces the same), MinimaxAI doesn't do the same. It's willing to wait and dally around by moving a single piece back and forth. While this makes MinimaxAI an interesting opponent, it also results in its downfall, as the AI allowed me to capture every single piece except the king, leaving no one to defend him.\
\
Overall, I'd say that MinimaxAI seems somewhat intelligent in its unpredictability, and to an extent its willingness to sacrifice pieces makes it harder to beat. However, the fact that it allows me to capture every single one of its pieces in very simple moves suggests that it's very flawed.
## Evaluation Function
I used the material value heuristic as suggested in the textbook -- that is, pawn = 1, knight = 3, bishop = 3, rook = 5, queen = 9, king = 0. I made the values positive during the maximizing player's turn and negative during the minimizing player's turn.\
\
As discussed above, there are issues with this evaluation function, mainly its passivity -- it does a better job than RandomAI at blocking wins, but it doesn't try that hard to take wins and is very complacent with having non-king pieces captured. Therefore, as an extension, I implemented the class AggressiveHeuristic to improve my chess AI.
## BONUS_AggressiveHeuristic
To encourage captures, I implemented AggressiveHeuristic. It assigns the king an arbitruary value of 100 instead of 0 (since the king seems somewhat overvalued in the original heuristic -- it's the only piece that gets defended), but the other material values remain the same. The significant part of this heuristic is the evaluate() function, which increases scores for moves that result in captures.\
\
This heuristic definitely outplays the material value heuristic, as it not only blocks wins but also tries to take wins. However, like the  material value heuristic, it is quite complacent with having its pieces captured (although, if a chance for retaliation arises, it _will_ take it).
## Iterative Deepening
To implement iterative deepening, I  added a version parameter to MinimaxAI. When the version is "non-iterative," choose_move() runs as usual. When the version is "iterative," a for loop inside choose_move() runs minimax() at incrementing depths until the maximum depth is reached.\
\
I made my iterative deepening AI print out the best move outputted at each depth, and there are indeed different moves considered at different depths. Here is the result when the code is run at depth 4:
<pre>
White to move

Please enter your move: 
g1h3
True
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . N
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Depth:  1 	Best move:  g8h6
Depth:  2 	Best move:  g7g6
Depth:  3 	Best move:  h7h6
Depth:  4 	Best move:  b8c6
Iterative Minimax AI recommending move b8c6
after  9745  nodes explored
r . b q k b n r
p p p p p p p p
. . n . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . N
P P P P P P P P
R N B Q K B . R
----------------
a b c d e f g h

White to move

Please enter your move: 
e2e3
True
r . b q k b n r
p p p p p p p p
. . n . . . . .
. . . . . . . .
. . . . . . . .
. . . . P . . N
P P P P . P P P
R N B Q K B . R
----------------
a b c d e f g h

Black to move

Depth:  1 	Best move:  g8h6
Depth:  2 	Best move:  a8b8
Depth:  3 	Best move:  c6b4
Depth:  4 	Best move:  c6e5
Iterative Minimax AI recommending move c6e5
after  16479  nodes explored
r . b q k b n r
p p p p p p p p
. . . . . . . .
. . . . n . . .
. . . . . . . .
. . . . P . . N
P P P P . P P P
R N B Q K B . R
----------------
a b c d e f g h

White to move

Please enter your move: 
</pre>
## AlphaBetaAI
To implement alpha-beta pruning, I copied code from my MinimaxAI.py and added a few lines and parameters. I changed minimax() to alphabeta() and added parameters alpha and beta. Within the function itself, I keep track of alpha and beta values. If the new best_score is not as good as the current one, the function breaks, effectively pruning the less efficient path.\
\
I ran (non-iterative) minimax and alphabeta at the same depth (4), with the same heuristic (AggressiveHeuristic) and verified that they gave the same results, though alphabeta explores fewer nodes.\
\
Here is a table displaying my data from trials with different AI --
<pre>
| my move | minimax (nodes) | alphabeta (nodes) | zobrist (nodes) |
| ------- | --------------- | ----------------- | --------------- |
| c2c4    | b7b5 (10206)    | b7b5 (1242)       | b7b5 (1004)     |
| c4b5    | b8c6 (10491)    | b8c6 (1438)       | b8c6 (1265)     |
| b5c6    | d7c6 (8470)     | d7c6 (1279)       | d7c6 (1032)     |
| g1f3    | d8d3 (19423)    | d8d3 (3017)       | d8d3 (2358)     |
| e2e3    | e8d8 (39492)    | e8d8 (6758)       | e8d8 (5035)     |
</pre>
As expected, Minimax and AlphaBeta return the same moves when in the same state, though AlphaBeta explores fewer nodes.\
\
AlphaBeta with a transposition table (current AlphaBeta), however, does not always return the same moves. This may be a result of hash collisions. After using Zobrist hashing instead, the moves returned became more consistent.\
\
Note that Minimax and AlphaBeta nodes traveled both increase exponentially as the depth increases, resulting in noticeably slower runtimes around depth 4-6.
## Transposition Table
I implemented a transposition table using hash(str(board)) to further optimize and avoid searching already-searched nodes. First, in the initiation function for AlphaBetaAI, I added self.transition_table as a dictionary. Then, in the alphabeta() function, I added another base case in which we check whether or not the hash key is in the transposition table. If it is, we return the move and score that already exist in the table instead of searching again. Later in the function, with each node searched, I add the new node (along with its move, score, and depth) to the transposition table.
# Testing
I pitted various AI's with various heuristics against each other, and here are my conclusions:
- With AggressiveHeuristic, deeper versions of MinimaxAI and AlphaBetaAI consistently perform better than shallower ones (e.g. depth 6 wins against 5, 5 wins against 4 and 3). Although, at depth 3 and below, depth has no noticeable effect as the algorithm starts to drastically decline in performance regardless.
- Regardless of depth, the material value heuristic seems to be not that effective, as pitting two AI's with this heuristic against each other creates a passive game in which neither side seems that interested in the other as long as they don't attack.
- I can usually win against the material value heuristic by taking out all their pieces one by one so no one is left to defend the king.
- I sometimes lose to AggressiveHeuristic, usually to attacks i fail to notice.
# BONUS_Zobrist
I also implemented a simple version of Zobrist hashing in AlphaBetaAI. The chess programming wiki describes a version with four variables in the initiation, but I decided to ignore castling rights and en passant moves because these are special cases that don't often come up. In my code, I initiated piece_at_square to keep track of piece-square combinations and side_to_move to represent which side's turn it is to move. In get_hash(), I used XOR to combine random keys to generate a unique hash key.\
\
My Zobrist hashing function does a better job than the original transposition table at avoiding collisions. It also effectively decreases number of nodes explored -- see the table in the AlphaBetaAI section.
# BONUS_OpeningBook
I implemented an opening book with a default empty opening as well as the openings for the Italian Game and the King's Gambit. Each opening is represented as a sequence of steps. I tested my opening book in AlphaBeta, where we check the length of the current moves stack against the length of the chosen opening moves and returns the appropriate moves in the correct order. I added an optional parameter to AlphaBetaAI that allows you to select an opening (see test_chess.py).\
\
I tested two AlphaBetaAI's playing the Italian Game, and the implementation works. However, when I personally played against an AlphaBetaAI following the Italian opening, I realized a flaw with this approach -- my opening book has a very rigid series of steps, not allowing the chess algorithm to decide the best path until all the moves have been played out. In other words, playing by the opening book, the AI is not free in the first couple of steps to react to the opponent's actions.
# Bonus: Literature Review
A 2023 paper, Analysis and Comparison of Chess Algorithms, discusses three chess algorithms. We've discussed minimax in class, and the paper also describes the genetic algorithm and Monte Carlo. The writers of this paper implemented these algorithms and tested them with the Stockfish engine. The genetic algorithm, which operates on Darwinian principles to optimize in large search spaces, performs poorly but runs very fast. The Monte Carlo algorithm, which uses random sampling to find approximate solutions, doesn't seem very suitable in chess. Minimax, based on the principles of game theory, generally outperforms the other algorithms.
## References
Trajkoska, V., & Dimeski, G. (2023). Analysis and Comparison of Chess Algorithms. Paper presented at the 20th International Conference on Informatics and Information Technologies - CIIT 2023. Ss Cyril and Methodius University in Skopje, Faculty of Computer Science and Engineering, Republic of North Macedonia. Retrieved from [URI: http://hdl.handle.net/20.500.12188/27381]
