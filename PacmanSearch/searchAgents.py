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
# class BFSAgent(Agent):
#     def getAction(self, state):
#         problem = PacmanProblem(state.__str__())
#         searchStratergy = SearchStrategies()
#         result = searchStratergy.bfs_search(problem)
#         if result[0] == "East": return Directions.EAST
#         if result[0] == "South": return Directions.SOUTH
#         if result[0] == "West": return Directions.WEST
#         if result[0] == "North": return Directions.NORTH
#         return Directions.STOP
#
# class AStarAgent(Agent):
#     def getAction(self, state):
#
#         problem = PacmanProblem(state.__str__())
#         searchStratergy = SearchStrategies()
#         result = searchStratergy.a_star_search(problem)
#         if result[0] == "East": return Directions.EAST
#         if result[0] == "South": return Directions.SOUTH
#         if result[0] == "West": return Directions.WEST
#         if result[0] == "North": return Directions.NORTH
#         return Directions.STOP

class SearchAgent(Agent):

    def __init__(self, searchFunction=None):
        self.searchFunction = searchFunction
        self.isSearchPerformed = False
        self.actions = []
        self.performedActions = []
        self.boolOneTimePrint = False

    def printTheResult(self):
        print("List of actions: ")
        print(self.performedActions)
        print("Total cost: ", len(self.performedActions))

    def reRunSearch(self, state):
        problem = PacmanProblem(state.__str__())  # Adjust this to pass whatever the problem needs
        self.actions = self.searchFunction(problem) if self.searchFunction else []
        self.isSearchPerformed = True

    def getAction(self, state):
        if state.getNumFood() == 0:
            if self.boolOneTimePrint is False:
                self.printTheResult()
                self.boolOneTimePrint = True
            return Directions.STOP

        while not self.actions or not self.isSearchPerformed:
            self.reRunSearch(state)
        nextAction = self.actions.pop(0)
        self.performedActions.append(str(nextAction))

        return nextAction

class BFSAgent(SearchAgent):
    def __init__(self):
        super().__init__(searchFunction=SearchStrategies().bfs_search)

class UCSAgent(SearchAgent):
    def __init__(self):
        super().__init__(searchFunction=SearchStrategies().ucs_search)

class AStarAgent(SearchAgent):
    def __init__(self):
        super().__init__(searchFunction=lambda problem: SearchStrategies().a_star_search(problem, SearchStrategies().EuclidDistanceHeuristic))
