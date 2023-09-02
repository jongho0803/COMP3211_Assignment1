# reactiveAgents.py
# ---------------
# Licensing Information: You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC
# Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import perceptron


class NaiveAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        sense = state.getPacmanSensor()
        if sense[7]:
            action = Directions.STOP
        else:
            action = Directions.WEST
        return action

class PSAgent(Agent):
    "An agent that follows the boundary using production system."

    def getAction(self, state):
        sense = state.getPacmanSensor()
        x = [sense[1] or sense[2] , sense[3] or sense[4] ,
        sense[5] or sense[6] , sense[7] or sense[0]]
        if x[0] and not x[1]:
            action = Directions.EAST
        elif x[1] and not x[2]:
            action = Directions.SOUTH
        elif x[2] and not x[3]:
            action = Directions.WEST
        elif x[3] and not x[0]:
            action = Directions.NORTH
        else:
            action = Directions.NORTH
        return action

class ECAgent(Agent):
    "An agent that follows the boundary using error-correction."
    def getAction(self, state):
        sense = state.getPacmanSensor()
        sum_north = sum_west = sum_south = sum_east = 0

        for i in range(len(perceptron.north_perceptron) - 1):
            sum_north += perceptron.north_perceptron[i+1] * sense[i]
            sum_west += perceptron.west_perceptron[i+1] * sense[i]
            sum_south += perceptron.south_perceptron[i+1] * sense[i]
            sum_east += perceptron.east_perceptron[i+1] * sense[i]
            
        if (sum_north >= perceptron.north_perceptron[0]):
            return Directions.NORTH
        if (sum_west >= perceptron.west_perceptron[0]):
            return Directions.WEST
        if (sum_south >= perceptron.south_perceptron[0]):
            return Directions.SOUTH
        if (sum_east >= perceptron.east_perceptron[0]):
            return Directions.EAST
        
        return Directions.NORTH

class SMAgent(Agent):
    "An sensory-impaired agent that follows the boundary using state machine."
    def registerInitialState(self,state):
        "The agent receives the initial GameState (defined in pacman.py)."
        sense = state.getPacmanImpairedSensor() 
        self.prevAction = Directions.STOP
        self.prevSense = sense

    def getAction(self, state):
        sense = state.getPacmanImpairedSensor()
        S1 = S3 = S5 = S7 = 0

        if(self.prevSense[0] == 1 and self.prevAction == Directions.EAST):
            S1 = 1
        if(self.prevSense[1] == 1 and self.prevAction == Directions.SOUTH):
            S3 = 1
        if(self.prevSense[2] == 1 and self.prevAction == Directions.WEST):
            S5 = 1
        if(self.prevSense[3] == 1 and self.prevAction == Directions.NORTH):
            S7 = 1

        if(not(sense[0]) and sense[3]):
            self.prevAction = Directions.NORTH
            self.prevSense = sense
            return Directions.NORTH
        if(not(sense[3]) and sense[2]):
            self.prevAction = Directions.WEST
            self.prevSense = sense
            return Directions.WEST
        if(not(sense[2]) and sense[1]):
            self.prevAction = Directions.SOUTH
            self.prevSense = sense
            return Directions.SOUTH
        if(not(sense[1]) and sense[0]):
            self.prevAction = Directions.EAST
            self.prevSense = sense
            return Directions.EAST
        if(S1 == 1):
            self.prevAction = Directions.NORTH
            self.prevSense = sense
            return Directions.NORTH
        if(S7 == 1):
            self.prevAction = Directions.WEST
            self.prevSense = sense
            return Directions.WEST
        if(S5 == 1):
            self.prevAction = Directions.SOUTH
            self.prevSense = sense
            return Directions.SOUTH
        if(S3 == 1):
            self.prevAction = Directions.EAST
            self.prevSense = sense
            return Directions.EAST
        
        self.prevAction = Directions.NORTH
        self.prevSense = sense
        return Directions.NORTH
