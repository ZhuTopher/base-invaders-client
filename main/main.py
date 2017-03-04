from Commands import Commands

from operator import sub, mul

from math import atan2, pi, sqrt, pow
from random import random
from time import time

commands = Commands()

EPSILON = 0.015

class Ship:
    def __init__(self, x, y, dx, dy, angle):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.angle = angle
        self.accelDir = None

        self.target = None
        self.roaming = False
        self.startTargetTime = time()

def toProperRad(a):
    return a + pi

def isMineOwned(mine, mines):
    for m in mines:
        if mine == m:
            return True
    return False

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


def roam(ship):
    ship.angle = random() * 2* pi
    commands.accelerate(ship.angle, 1)

    ship.roaming = True

def goToTarget(ship):
    print "DX: " + str(ship.dx)
    print "DY: " + str(ship.dy)

    if (ship.dx <= EPSILON and ship.dy <= EPSILON):
        print "MOVING TO TARGET"
        ship.angle = toProperRad(atan2(ship.y-ship.target[1], ship.x-ship.target[0]))
        ship.accelDir = [ship.x-ship.target[0], ship.y-ship.target[1]]
        commands.accelerate(ship.angle, 1)

    print "SHIP ACCEL DIR: " + str(ship.accelDir)
    if ship.accelDir and sum(map(mul, ship.accelDir, [ship.x-ship.target[0], ship.y-ship.target[1]])) > 0:
        ship.angle = toProperRad(atan2(ship.y-ship.target[1], ship.x-ship.target[0]))
        commands.accelerate(ship.angle, 1)

def isMineOwned(mine, mines):
    print "Checking for" + str(mine)

    for m in mines:
        print m

        if mine == m[1:]:
            return True
    return False

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

        owned = filter(lambda x: x[0] == 'kanata',status_dict['mines'])
        if (ship.target and isMineOwned(ship.target, owned)):
            ship.target = None
            print "GOT TARGET"

        if not ship.target:
            if not ship.roaming:
                print "START ROAMING"
                roam(ship)
            else:
                mines = filter(lambda x: x[0] != 'kanata',status_dict['mines'])
                if mines:
                    print "FOUND TARGET"
                    ship.target = findBestMine(ship, mines)
                    ship.startTargetTime = time()
                    ship.roaming = False
                    commands.stop()
        else:
            if time() - ship.startTargetTime > 15:
                print str(time()) + ' ' + str(ship.startTargetTime)
                ship.target = None
            else:
                goToTarget(ship)

