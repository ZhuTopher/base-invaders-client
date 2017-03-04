from Commands import Commands
from Directions import calculateAccel

from operator import sub, mul

from math import sin, cos, atan2, pi, sqrt, pow
from random import random
from time import time

commands = Commands()

EPSILON = 0.015

class Ship:
    def __init__(self, x, y, dx, dy, angle):
        self.xPrev = x
        self.yPrev = y
        self.dxPrev = dx
        self.dyPrev = dy
        self.aPrev = None
        self.timePrev = None

        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.a = None
        self.time = time()

        self.angle = angle
        self.accelDir = None

        self.target = None

        self.startTargetTime = time()
        self.hasStopped = False

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

def bombRoam(ship, conf):
    if (ship.dx <= EPSILON and ship.dy <= EPSILON):
        ship.angle = random() * 2* pi
        commands.accelerate(ship.angle, 1)


    if ship.a and ship.aPrev:
        deltaT = (conf['bomb_delay']-0.25)
        futureX = ship.x + (ship.dx*deltaT)+0.5*(ship.a[0] * cos(ship.a[1]))*pow(deltaT, 2)
        futureY = ship.y + (ship.dy*deltaT)+0.5*(ship.a[0] * sin(ship.a[1]))*pow(deltaT, 2)
        dist = sqrt(pow(futureX-ship.x, 2) + pow(futureY-ship.y, 2))

        # leave a trail, attempt to boost yourself (direction, pi/4)
        if dist > conf['bomb_place_radius']:
            print "Attempting Bomb BOOST"
            try:
                commands.bomb(ship.x-1, ship.y-1, conf['bomb_delay'])
            except:
                pass
        else:
            try:
                commands.bomb(int(futureX), int(futureY), conf['bomb_delay'])
            except:
                pass

            print "BOMB at (" + str(futureX) + ", " + str(futureY) + ") : " + str(deltaT)        

def goToTarget(ship):
    print "DX: " + str(ship.dx)
    print "DY: " + str(ship.dy)

    if ship.hasStopped:
        print "MOVING TO TARGET"
        ship.angle = toProperRad(atan2(ship.y-ship.target[1], ship.x-ship.target[0]))
        ship.accelDir = [ship.x-ship.target[0], ship.y-ship.target[1]]
        commands.accelerate(ship.angle, 1)

        print "SHIP ACCEL DIR: " + str(ship.accelDir)
        if ship.accelDir and sum(map(mul, ship.accelDir, [ship.x-ship.target[0], ship.y-ship.target[1]])) < 0:
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

        ship.timePrev = ship.time
        ship.time = time()

        ship.xPrev = ship.x
        ship.yPrev = ship.y
        ship.dxPrev = ship.dx
        ship.dyPrev = ship.dy
        

        ship.x = status_dict['x']
        ship.y = status_dict['y']
        ship.dx = status_dict['dx']
        ship.dy = status_dict['dy']

        ship.angle = toProperRad(atan2(ship.y-ship.yPrev, ship.x-ship.xPrev))

        ship.aPrev = ship.a
        ship.a = calculateAccel(ship)


        owned = filter(lambda x: x[0] == 'kanata',status_dict['mines'])
        if (ship.target and isMineOwned(ship.target, owned)):
            ship.target = None
            print "GOT TARGET"

        if not ship.target:
            bombRoam(ship, conf)
            mines = filter(lambda x: x[0] != 'kanata',status_dict['mines'])
            if mines:
                print "FOUND TARGET"
                ship.target = findBestMine(ship, mines)
                ship.startTargetTime = time()
                ship.hasStopped = False
        else:
            if time() - ship.startTargetTime > 15:
                print str(time()) + ' ' + str(ship.startTargetTime)
                ship.target = None
            else:
                if (abs(ship.dx) <= EPSILON and abs(ship.dy) <= EPSILON):
                    ship.hasStopped = True
                elif not ship.hasStopped:
                    commands.stop()

                goToTarget(ship)

