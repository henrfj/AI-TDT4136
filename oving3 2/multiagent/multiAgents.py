# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # TODO: wrong number of calls for gameState.generateSuccessor()

        def max_value(game_state, depth):
            """
            Returns a utility value, maximizing the utility of the recursive tree below itself.
            This function represents PacMan, and he always chooses the move to provide himself
            best possible utility.
            :param game_state: current game situation
            :param depth: how deep we currently are in the search tree, reduced by one
            for every call of max_value
            :return: a utility value
            """

            # Checks if we have reached a leaf node, or at max depth
            if terminal_test(game_state, depth):
                return self.evaluationFunction(game_state)

            # Goes through the recursive tree below by predicting how actions affect the gameState.
            # End up with a value v, being the maximum utility we can get from the below tree
            v = - float('inf')
            for _action in game_state.getLegalActions(self.index):
                # game_state.getNumAgents() -1 will give the number of ghosts
                v = max(v, min_value(result(game_state, _action, self.index), depth, game_state.getNumAgents()-1))
            return v

        def min_value(game_state, depth, num_ghosts):
            """
            Return a utility value, minimizing utility of the recursive tree below itself.
            We call this function recursively for every ghost before calling the max_value
            :param game_state: current situation of the game
            :param depth: how deep we currently are in the search tree
            :param num_ghosts: number of times we need to call min_value before calling max_value
            :return: a utility value
            """
            # Chekcs if we have reached a leaf node
            if terminal_test(game_state, depth):
                return self.evaluationFunction(game_state)

            v = float('inf')
            if num_ghosts > 1:
                # As long as we aren't the last ghost to be evaluated,
                # we will call min_value for the next gameState(s) as
                # a ghost will take action after us
                for _action in game_state.getLegalActions(num_ghosts):
                    v = min(v, min_value(result(game_state, _action, num_ghosts), depth, (num_ghosts - 1)))
            else:
                # Now a PacMan will take action after us, and we know PacMan always maximizes
                # his utility, therefor we call max_value on the next gameState(s)
                for _action in game_state.getLegalActions(num_ghosts):  # num_ghost is always 1 here
                    v = min(v, max_value(result(game_state, _action, num_ghosts), depth - 1))
            return v

        def terminal_test(game_state, depth):
            """
            Tests if we are at a terminal node and needs to return its utility
            :param game_state: current situation of the game
            :param depth: How deep we currently are in the search tree
            :return: True if we are at a leaf, or at max depth, False if we can go on
            """
            if len(game_state.getLegalActions(self.index)) == 0 or depth == 0:
                return True
            return False

        # Generates a successor state for each call
        def result(game_state, _action, index):
            """
            Calculates the next situation of the game-board
            :param game_state: the current situation of the game
            :param _action: the move to be done
            :param index: the agent about to do this move
            :return: the next game situation after the move is concluded
            """
            return game_state.generateSuccessor(index, _action)

        # Now we must fin the best action from our current position
        best_score = -float('inf')
        best_index = 0
        action_table = gameState.getLegalActions(self.index)

        for i, action in enumerate(action_table):
            # game_state.getNumAgents() -1 will give the number of ghosts
            utility = min_value(result(gameState, action, self.index), self.depth, gameState.getNumAgents() - 1)
            if utility > best_score:
                best_score = utility
                best_index = i

        return action_table[best_index]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

