from Commands import Commands
from Directions import calculateAccel

from operator import sub

from math import atan2, pi, sqrt, pow
from random import random
from time import time

commands = Commands()

class Ship:
    def __init__(self, x, y, dx, dy, angle):
        self.xPrev = -1
        self.yPrev = -1
        self.dxPrev = -1
        self.dyPrev = -1
        self.aPrev = None # tuple holding (magnitude, angle)
        self.anglePrev = toProperRad(atan2(self.yPrev, self.xPrev))

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = angle
        self.a = None # tuple holding (magnitude, angle)

        self.timePrev = -1
        self.time = time() # in seconds

        self.targetLocked = False
        self.stopped = False

        self.target = None

def toProperRad(a):
    return a + pi

def calculateScore(ship, pos1, pos2):
    def calc(dist, angle):
        angleScore = abs(ship.angle-angle)
        return dist

    diff = map(sub, pos2, pos1)
    print "DIFF: " + str(diff)
    distance = sqrt(pow(diff[0], 2) + pow(diff[1], 2))
    angle = toProperRad(atan2(diff[1], diff[0]))
    return calc(distance, angle)

    return scores

def findBestMine(ship, mines):
    mines_coords = [m[1:] for m in mines]
    scores = [calculateScore(ship, (ship.x, ship.y), m) for m in mines_coords]
    return mines_coords[scores.index(min(scores))]

def isMineOwned(mine, mines):
    mines_coords = [m[1:] for m in mines]
    if ((m[0] == mine[0]) and (m[1] == mine [1])):
        return True

    return False

def makeDecision(ship, conf, status_dict):
    if ship.targetLocked:
        # Change ship.a to try and path towards ship.target
        ship.aPrev = ship.a
        ship.a = targettedAccel(ship, ship.target[0], ship.target[1])
        commands.accelerate(ship.angle, ship.a[0])
    else:
        mines = filter(lambda x: x[0] != 'kanata',status_dict['mines'])
        if mines:
            ship.target = findBestMine(ship, mines)
            ship.targetLocked = True

            # Change ship.a to try and path towards ship.target
            ship.aPrev = ship.a
            ship.a = targettedAccel(ship, ship.target[0], ship.target[1])
            if ship.a[0] > 1:
               commands.accelerate(ship.angle, 1)
            else:
                commands.accelerate(ship.angle, ship.a)

            # if ship.stopped:
            #     diff = map(sub, (ship.x, ship.y), closestMine)
            #     ship.angle = toProperRad(atan2(diff[1], diff[0]))
            #     print "GOING AT THIS ANGLE NOW: " + str(ship.angle)
            #     accel = sqrt(pow(diff[0], 2) + pow(diff[1], 2)) / conf['vision_radius']
            #     commands.accelerate(ship.angle, accel)
            # else:
            #     commands.stop()
        else:
            commands.accelerate(ship.angle, 1)

if __name__ == '__main__':
    ship = Ship(0,0,0,0,0)
    while(True):
        conf = commands.configurations()
        status_dict = commands.getStatus()

        ship.xPrev = status_dict['x']
        ship.yPrev = status_dict['y']
        ship.dxPrev = status_dict['dx']
        ship.dyPrev = status_dict['dy']
        ship.anglePrev = ship.angle

        ship.x = status_dict['x']
        ship.y = status_dict['y']
        ship.dx = status_dict['dx']
        ship.dy = status_dict['dy']
        ship.angle = toProperRad(atan2(ship.y, ship.x))

        ship.timePrev = ship.time
        ship.time = time()

        ship.aPrev = ship.a
        ship.a = calculateAccel(ship)

        minesOwned = filter(lambda x: x[0] == 'kanata',status_dict['mines'])
        if (ship.targetLocked and (isMineOwned(ship.target, minesOwned))):
            ship.target = None
            ship.targetLocked = False

        if ship.aPrev[0] != -1:
            makeDecision(ship, conf, status_dict)

        # else:
        #     if ship.dx < 0.01 and ship.dy < 0.01:
        #         ship.targetLocked = False
        #         ship.stopped = True