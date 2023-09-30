import logging

import util
from problems.q1c_problem import q1c_problem
import math

def q1c_solver(problem: q1c_problem):
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()  # Your code replaces this line
    start_state = problem.getStartState()
    goal_position = get_all_food_position(start_state)
    # print(goal_position,'INITIAL_GOAL_POSITION')

    total_foodNum = start_state.getNumFood()

    start_node = q1c_node(start_state, None, None, 0)
    frontier = util.PriorityQueue()
    frontier.push(start_node, 0)
    explored = set()
    fn=0
    manhattan=0
    
    counter = 0
    while not frontier.isEmpty():
        node = frontier.pop()

        if node.get_state().getNumFood() < total_foodNum:
            manhattan = 0
            # print("AHAHAHAHAHAHAH")
            total_foodNum = node.state.getNumFood()
            goal_position = get_all_food_position(node.state)
            explored = set()
            frontier = util.PriorityQueue()
            frontier.push(node, 0)
            continue
            # print(goal_position,'GOAL_POSITION')

        if node.get_position() in explored:
            continue
       
        # print('\n',node.get_action(),node.get_path(), node.get_position(),'ACTION_POP')
        
        if problem.isGoalState(node.get_state()):
            return node.get_path()
      
        explored.add(node.get_position())
        # print(explored,'EXPLORED')

        
   

        for successor in problem.getSuccessors(node.get_state()):
            manhattan = 0
            min_manhattan = math.inf
            if successor[0].getPacmanPosition() not in explored:
                
                child_node = q1c_node(successor[0], node, successor[1], len(node.get_path())+1)


                wall_count = 0
                x, y = child_node.position
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if successor[0].hasWall(x + dx, y + dy):
                        wall_count += 1


                food_count_x = 0
                food_count_y = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    next_x, next_y = x + dx, y + dy
                    while 0 <= next_x < successor[0].getFood().width and 0 <= next_y < successor[0].getFood().height:
                        if successor[0].hasFood(next_x, next_y):
                            if dx != 0:
                                food_count_x += 1
                            else:
                                food_count_y += 1
                        next_x += dx
                        next_y += dy
          

    

                for goal in goal_position:
                    # manhattan += util.manhattanDistance(child_node.position, goal)
                    manhattan = util.manhattanDistance(child_node.position, goal)
                    if manhattan<min_manhattan:
                        min_manhattan = manhattan

                    if manhattan == min_manhattan:
                        # print(wall_count,'WALLLLLLLLL')
                        #move to direction that has more walls
                        min_manhattan -= 0.1 * wall_count
                        if food_count_y < food_count_x and (successor[1]=='East' or successor[1]=='West'):
                            min_manhattan -= 0.1  
                        elif food_count_y > food_count_x and (successor[1]=='North' or successor[1]=='South'):
                            min_manhattan -= 0.1




                # print(child_node.get_action(),child_node.get_cost(),manhattan,'COSTTTTTTT')
     
                if problem.isGoalState(child_node.get_state()):
                    return child_node.get_path()
                else:
                    fn = child_node.get_cost() + min_manhattan

                # frontier.push(child_node, fn)
                frontier.update(child_node, fn)
                
        
        # if counter ==10:
        #     print(node.get_path())
        #     return
    
        counter +=1
    return None
def get_all_food_position(state):
    food_grid = state.getFood()
    food_pos = []
    for x in range(food_grid.width):
        for y in range(food_grid.height):
            if state.hasFood(x, y):
                food_pos.append((x, y))

    return food_pos

            
class q1c_node:
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


