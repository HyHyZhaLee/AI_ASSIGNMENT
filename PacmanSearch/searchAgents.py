from game import Directions
from game import Agent
from game import Actions
import util
import time
import random
import search

class RandomAgent(Agent):
    def __int__(self):
        pass

    def getAction(self, state):
        legalActions = state.getLegalPacmanActions()
        if len(legalActions) > 0:
            return random.choice(legalActions)
        else:
            return Directions.STOP
        
'''
# TODO 03: SearchAgent
Implement a subclass of Agent class.
For each game step, getAction() method is invoked and 
the returned action is performed.
'''
from search import *
class BFSAgent(Agent):
    def getAction(self, state):
        problem = PacmanProblem(state.__str__())
        # print(state.__str__())cle
        # time.sleep(10)
        result = SearchStrategies.bfs_search(problem)
        if result[0] == "East": return Directions.EAST
        if result[0] == "South": return Directions.SOUTH
        if result[0] == "West": return Directions.WEST
        if result[0] == "North": return Directions.NORTH
        return Directions.STOP

class AStarAgent(Agent):
    def getAction(self, state):
        problem = PacmanProblem(state.__str__())
        # print(state.__str__())cle
        # time.sleep(10)
        result = SearchStrategies.bfs_search(problem)
        if result[0] == "East": return Directions.EAST
        if result[0] == "South": return Directions.SOUTH
        if result[0] == "West": return Directions.WEST
        if result[0] == "North": return Directions.NORTH
        return Directions.STOP