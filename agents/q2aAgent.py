import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance

last_action = None
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    # return currentGameState.getScore()
   
    
####ORIGINAL MOD
    score = currentGameState.getScore()
    
    ghostStates = currentGameState.getGhostStates()
    pacmanPos = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    # capsulePositions = currentGameState.getCapsules()
    
    scared_ghost = [ghost for ghost in ghostStates if ghost.scaredTimer > 0]
    
    if scared_ghost:
        closestScaredGhostDist = min([util.manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in scared_ghost])
        if closestScaredGhostDist > 0:
            score += 200 / closestScaredGhostDist
    else:
        closestGhostDist = min([util.manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in ghostStates])
        if closestGhostDist > 8:  # Increased the distance to consider a ghost "not near"
            if foodPositions:
                closestFoodDist = min([util.manhattanDistance(pacmanPos, food) for food in foodPositions])
                score += 50 / closestFoodDist  # encourage going for the food
        elif closestGhostDist > 0:
            score -= 5 / closestGhostDist
    
    numFood = currentGameState.getNumFood() #penalize for number of food left
    score -= 2 * numFood
    
    numCapsules = len(currentGameState.getCapsules()) #penalize for number of capsule left
    score -= 3 * numCapsules
    
    return score

class Q2A_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
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
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"
        _, bestAction = self.minimax(gameState, self.depth, self.index, float('-inf'), float('inf'))
        return bestAction

        util.raiseNotDefined()

    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            # print(self.evaluationFunction(gameState),'EVALUATION')
            return self.evaluationFunction(gameState), None
    
        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(agentIndex)
        

        
        if agentIndex == 0:  # Maximizing (Pacman)
            # print(agentIndex,'PAC_MAX')
            maxbackup = float('-inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                backup, _ = self.minimax(successor, depth, (agentIndex + 1) % numAgents, alpha, beta)
                if backup > maxbackup:
                    maxbackup = backup
                    bestAction = action
                alpha = max(alpha, backup)
                if beta <= alpha:
                    break  # Beta cut-off
            return maxbackup, bestAction
        
        else:  # Minimizing (Ghosts)
            # print(agentIndex,'GHOST')
            minbackup = float('inf')
            bestAction = None
            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:
                    backup, _ = self.minimax(successor, depth - 1, 0, alpha, beta)
                else:
                    backup, _ = self.minimax(successor, depth, (agentIndex + 1) % numAgents, alpha, beta)
                if backup < minbackup:
                    minbackup = backup
                    bestAction = action
                beta = min(beta, backup)
                if beta <= alpha:
                    break  # Alpha cut-off
            return minbackup, bestAction
        



    def minimax_algo(self, gameState, depth,):
        pass





    #%%


        


