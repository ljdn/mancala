# File: Player.py
# Author(s) names AND netid's: Lejia Duan (ldu917) Bryanna Yeh (byy911)
# Date: 4/16/2016
# Group work statement: All group members were present and contributing during all work on this project.
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.

from random import *
from decimal import *
from copy import *
from MancalaBoard import *
import time

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """

        alpha = -INFINITY
        beta = INFINITY
        move = -1
        score = -INFINITY
        turn = self

        score, move = self.ABmaxValue(board, ply, turn, alpha, beta)
        #return the best score and move so far
        return score, move

    def ABmaxValue(self, board, ply, turn, alpha = -(INFINITY), beta = INFINITY):
        """ Find the AB minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board), -1
        score = -INFINITY
        move = -1
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board), -1
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s, blah = opponent.ABminValue(nextBoard, ply-1, turn, alpha, beta)
            # update max score
            if s > score:
                score = s
                move = m
            # if score not within bounds, prune!
            if score >= beta:
                # print "you have been max pruned", score
                return score, move
            alpha = max(alpha, score)
        return score, move

    def ABminValue(self, board, ply, turn, alpha = -(INFINITY), beta = INFINITY):
        """ Find the AB minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board), -1
        score = INFINITY
        move = -1
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board), -1
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s, blah = opponent.ABmaxValue(nextBoard, ply-1, turn, alpha, beta)
            # update min score
            if s < score:
                score = s
                move = m
            # if score not within bounds, prune!
            if score <= alpha:
                # print "you have been min pruned", score, "[",alpha,",",beta,"]"
                return score, move
            beta = min(beta, score)
        return score, move

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        start = time.time()
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            end = time.time()
            elapsed = end - start
            print "MINIMAX time:", elapsed
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            end = time.time()
            elapsed = end - start
            print "ABRPRUNE time:", elapsed
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # if losing, choose random move with probability based on score difference
            scoreDiff = board.scoreCups[self.opp-1]-board.scoreCups[self.num-1]
            rando = choice([1]*min(4,scoreDiff-1) + [0]*50)
            if rando:
                print "Uh oh, you're winning by", scoreDiff, "- I choose random!"
                return choice(board.legalMoves(self))
            else:
                val, move = self.alphaBetaMove(board, self.ply)
                end = time.time()
                elapsed = end - start
                print "CUSTOM time:", elapsed
                print "chose move", move, " with value", val
                return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class ldu917(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """
    def __init__(self, playerNum, playerType, ply=11):
        """Calls Player init. Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        Player.__init__(self,playerNum, playerType, ply)
        print "ldu917 ply=", self.ply

    def score(self, board):
        """ Evaluate the Mancala board for this player with the following heuristic:
            if P1: score = (own mancala - opponent mancala) + (stones on own side - stones on opponent side)
            if P2: score = (own mancala - opponent mancala) + (stones on own side - stones on opponent side) + (empty cups on opponent side)"""
        if self.num == 1:
            # Player is P1
            return (board.scoreCups[self.num-1] - board.scoreCups[self.opp-1]) + (sum(board.P1Cups) - sum(board.P2Cups))
        else:
            # Player is P2
            return (board.scoreCups[self.num-1] - board.scoreCups[self.opp-1]) + (sum(board.P2Cups) - sum(board.P1Cups)) + board.P1Cups.count(0) # + board.P1Cups.count(0)
