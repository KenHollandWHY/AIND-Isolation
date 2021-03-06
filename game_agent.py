"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # for now using the improved_hueristic score.
    # in lecture 2 things were mentionted. If opening move, you go to center. If not opening, you go to un-mirrorable moves
    # so since ill set that up on the opening move 'book' 
    # perhaps here i should go with the 'unmirrorable moves left' for each? 
    
    
    # also. The req is to submit 3 hureistics? Then maybe this function should just call another one where 
    # the hueristics themselves are stored
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))   
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    # 
    # 
    
    return float(own_moves - opp_moves)   


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        
        # check if no legal moves and return
        
        # based on the class lecture, the best opening move is the central suqare if you open and
        # a non-mirrorable square if you dont so set those up
        
        # if opening player
        
        # if not 
        bestmove = (-1,-1)
        if not legal_moves:
            return bestmove
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if (self.method=='minimax' and self.iterative):
                depth = 0
                while True:
                    depth +=1 
                    score, bestmove = self.minimax(game, depth)
                    
                    
            elif self.method =='minimax':
                score, bestmove = self.minimax(game, self.search_depth)

            else:
                score, bestmove =self.alphabeta(game, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return bestmove

        # Return the best move from the last completed search iteration
        return bestmove

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_move = (-1,-1)
        if game.is_winner(self):
            return self.score(game, self), game.get_player_location(self)
        if game.is_loser(self):
            return self.score(game, self), (-1, -1)
        if len(game.get_legal_moves()) == 0:
            return self.score(game, self), game.get_player_location(self) #termination trigger for the recursion below
        if depth == 0:
            return self.score(game, self), game.get_player_location(self) #termination trigger for the recursion below
        if maximizing_player:                                             # if the True toggle is on we are in a max branch of minimax
            score = float("-inf")                                         # we want any score that is greater tahn negative infinity. even a tiny number is alright
            for move in game.get_legal_moves():                           # scan through all the moves we have in the current board
                
                next_score, next_move = self.minimax(game.forecast_move(move), depth-1, False)  # recursively call minimax, toggle to min
                if next_score > score:                                                      # check if we found a better score than we have so far. 
                    score = next_score                                                      # if we did make it the new score and make sure the top 
                    best_move = move                                                        # move that started this whole for loop is saved
        else:
            score = float("inf")
            for move in game.get_legal_moves():
                best_score = float('inf')
                next_score, next_move = self.minimax(game.forecast_move(move), depth-1,True)
                if next_score < score:
                    score = next_score
                    best_move = move
        return score, best_move 

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # copied the code from my normal min max. only alpha beta stuff will get additional explanation. 
        
        best_move = (-1,-1)
        if len(game.get_legal_moves()) == 0:
            return self.score(game, self), game.get_player_location(self) 
        if depth == 0:
            return self.score(game, self), game.get_player_location(self)



        if maximizing_player: 
                                                      
            score = float("-inf")
                                                   
            for move in game.get_legal_moves():                          
                
                next_score, _ = self.alphabeta(game.forecast_move(move), (depth - 1), alpha, beta, False)  
                if score < next_score:
                    score = next_score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return score, best_move

                

            
        else:
            
            score = float("inf")
            
            for move in game.get_legal_moves():
                
                next_score, _  = self.alphabeta(game.forecast_move(move), depth-1, alpha, beta, True) 
                if next_score < score:
                    score = next_score
                    best_move = move
                # up until this line we are using identical logic to the minimax, recursively looking for scores that are the best
                # so we can save the 'move' that represents the top most loop. we dont care about the leaf move. 
                #     
                beta = min(beta, score)
                if beta <= alpha:
                    break

            return score, best_move 
