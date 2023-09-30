import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
# from util import manhattanDistance

last_action = None
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    # return currentGameState.getScore()
    global last_action
    score = currentGameState.getScore()

    # Game State Information
    ghostStates = currentGameState.getGhostStates()
    pacmanPos = currentGameState.getPacmanPosition()
    foodPositions = currentGameState.getFood().asList()
    capsulePositions = currentGameState.getCapsules()

    # Initialize variables to prevent divide-by-zero and other issues
    closestScaredGhostDist = float('inf')
    closestGhostDist = float('inf')
    closestFoodDist = float('inf')
    closestCapsuleDist = float('inf')


    if pacmanPos == last_action:
        score -= 100  # Adjust the penalty as needed

    # Update the last Pacman position
    last_action = pacmanPos

    # Scared Ghosts
    scaredGhosts = [ghost for ghost in ghostStates if ghost.scaredTimer > 0]
    if scaredGhosts:
        closestScaredGhostDist = min([util.manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in scaredGhosts])
        if closestScaredGhostDist > 0:
            score += 200 / closestScaredGhostDist
    else:
        closestGhostDist = min([util.manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in ghostStates])
        if closestGhostDist > 8:  # Increased the distance to consider a ghost "not near"
            if foodPositions:
                closestFoodDist = min([util.manhattanDistance(pacmanPos, food) for food in foodPositions])
                score += 50 / closestFoodDist  # Strongly encourage going for the food
        elif closestGhostDist > 0:
            score -= 5 / closestGhostDist

    # Food
    if foodPositions:
        closestFoodDist = min([util.manhattanDistance(pacmanPos, food) for food in foodPositions])
        if closestFoodDist > 0:
            score += 50 / closestFoodDist

    # Capsules
    if capsulePositions:
        closestCapsuleDist = min([util.manhattanDistance(pacmanPos, capsule) for capsule in capsulePositions])
        if closestCapsuleDist > 0:
            score += 30 / closestCapsuleDist  # Introduce Capsules into evaluation with a weight

    # Global and Local Penalties
    global_food_penalty = -2 * len(foodPositions)
    global_capsule_penalty = -3 * len(capsulePositions)

    # Local penalty based on food and capsules within a certain distance
    close_distance = 3
    local_food_penalty = -sum(1 for food in foodPositions if util.manhattanDistance(pacmanPos, food) <= close_distance)
    local_capsule_penalty = -sum(1 for capsule in capsulePositions if util.manhattanDistance(pacmanPos, capsule) <= close_distance)
    
    # tie_breaker = random.uniform(0, 0.1)
    # Final Score
    improved_score = score + global_food_penalty + global_capsule_penalty + local_food_penalty + local_capsule_penalty #+ tie_breaker

    return improved_score
    
    

class Q2B_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
    
    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        if gameState.isWin() or gameState.isLose() or depth == 0:
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
    
