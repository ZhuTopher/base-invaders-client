from Commands import Commands

from operator import sub

from math import atan2, pi, sqrt, pow
from random import random

commands = Commands()

class Ship:
    def __init__(self, x, y, dx, dy, angle):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = angle
        self.targetLocked = False
        self.stopped = False

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

def makeDecision(ship, conf, status_dict):
    mines = filter(lambda x: x[0] != 'kanata',status_dict['mines'])
    if mines:
        closestMine = findBestMine(ship, mines)
        ship.targetLocked = True
        if ship.stopped:
            diff = map(sub, (ship.x, ship.y), closestMine)
            ship.angle = toProperRad(atan2(diff[1], diff[0]))
            print "GOING AT THIS ANGLE NOW: " + str(ship.angle)
            accel = sqrt(pow(diff[0], 2) + pow(diff[1], 2)) / conf['vision_radius']
            commands.accelerate(ship.angle, accel)
        else:
            commands.stop()
    else:
        if ship.dx == 0 and ship.dy == 0:
            commands.accelerate(random() * 2 * pi, 1)

if __name__ == '__main__':
    ship = Ship(0,0,0,0,0)
    while(True):
        conf = commands.configurations()
        status_dict = commands.getStatus()
        ship.x = status_dict['x']
        ship.y = status_dict['y']
        ship.dx = status_dict['dx']
        ship.dy = status_dict['dy']
        ship.angle = toProperRad(atan2(ship.y, ship.x))
        if not ship.targetLocked:
            makeDecision(ship, conf, status_dict)
        else:
            if ship.dx < 0.01 and ship.dy < 0.01:
                ship.targetLocked = False
                ship.stopped = True