import logging

import util
from problems.q1a_problem import q1a_problem


def q1a_solver(problem: q1a_problem):
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()  # Your code replaces this line
    start_state = problem.getStartState()
    goal_position = get_food_position(start_state)
    # print(start_state.getLegalPacmanActions(),'LEGAL ACTIONS')
    # return
    start_node = q1a_node(start_state, None, None, 0)
    frontier = util.PriorityQueue()
    frontier.push(start_node, 0)
    explored = set()

    cost_g = 1

    counter = 0
    fn=0
    manhattan=0

    while not frontier.isEmpty():
        node = frontier.pop()

        if node.get_position() in explored:
            continue
       
        
        # print(node.get_position(),'POSITION')
        # print('\n',node.get_action(),node.get_path(), node.get_position(),'ACTION_POP')
        
        if problem.isGoalState(node.get_state()):
            return node.get_path()
        # explored.add(node.get_state())
        explored.add(node.get_position())
        # print(explored,'EXPLORED')


        for successor in problem.getSuccessors(node.get_state()):
            
            # if successor[0] not in explored:
            # print(successor[0].getPacmanPosition(),'SUCCESSOR')
            if successor[0].getPacmanPosition() not in explored:
                # child_node = q1a_node(successor[0], node, successor[1], 1)
                child_node = q1a_node(successor[0], node, successor[1], len(node.get_path())+1)
                # child_node = q1a_node(successor[0], node, successor[1], util.manhattanDistance(successor[0].getPacmanPosition(), start_node.get_position()))
                manhattan = util.manhattanDistance(child_node.position, goal_position)
                print(child_node.get_action(),child_node.get_cost(),manhattan,'COSTTTTTTT')
     
                if problem.isGoalState(child_node.get_state()):
                # if manhattan == 0:
                    return child_node.get_path()
                else:
                    fn = child_node.get_cost() + manhattan

                frontier.update(child_node, fn)
                # frontier.push(child_node, child_node.get_cost())
        
        # if counter ==10:
        #     print(node.get_path())
        #     return
        # print(successor,'HAHAHAH')
        cost_g += 1
        counter +=1
    return None


    


def get_food_position(state):
    food_grid = state.getFood()
    for x in range(food_grid.width):
        for y in range(food_grid.height):
            if state.hasFood(x, y):
                return (x, y)


    
    # util.raiseNotDefined()  # Your code replaces this line

class q1a_node:
    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.position = state.getPacmanPosition()


    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent
    
    def get_action(self):
        return self.action
    
    def get_cost(self):
        return self.cost
    
    def get_position(self):
        return self.position
    
    def get_path(self):
        path = []
        node = self
        while node.get_parent() is not None:
            path.append(node.get_action())
            node = node.get_parent()
        path.reverse()
        # print(path,'PATHHHHHHHHHH')
        return path
    


