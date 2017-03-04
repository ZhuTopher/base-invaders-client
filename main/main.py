from Commands import Commands

from operator import sub

from math import atan2, pi, sqrt, pow
from random import random

commands = Commands()

def toProperRad(a):
    return a + pi

# ship stats
x = 0
y = 0
dx = 0
dy = 0
my_angle = toProperRad(atan2(y, x))
targetLocked = False

def calculateScore(pos1, pos2):
    def calc(dist, angle):
        angleScore = abs(my_angle-angle)
        return dist

    diff = map(sub, pos2, pos1)
    print "DIFF: " + str(diff)
    distance = sqrt(pow(diff[0], 2) + pow(diff[1], 2))
    angle = toProperRad(atan2(diff[1], diff[0]))
    return calc(distance, angle)

    return scores

def findBestMine(mines):
    mines_coords = [m[1:] for m in mines]
    scores = [calculateScore((x, y), m) for m in mines_coords]
    return mines_coords[scores.index(min(scores))]

def makeDecision(conf, status_dict):
    mines = status_dict['mines']
    if mines:
        closestMine = findBestMine(mines)
        commands.stop()
        targetLocked = True
        diff = map(sub, (x, y), closestMine)
        angle = toProperRad(atan2(diff[1], diff[0]))
        print "GOING AT THIS ANGLE NOW: " + str(angle)
        accel = sqrt(pow(diff[0], 2) + pow(diff[1], 2)) / conf['vision_radius']
        commands.accelerate(angle, accel)
    else:
        if dx == 0 and dy == 0:
            commands.accelerate(random() * 2 * pi, 1)

if __name__ == '__main__':
    while(True):
        conf = commands.configurations()
        status_dict = commands.getStatus()
        x = status_dict['x']
        y = status_dict['y']
        dx = status_dict['dx']
        dy = status_dict['dy']
        if not targetLocked:
            makeDecision(conf, status_dict)
        else:
            if dx == 0.0 and dy == 0.0:
                targetLocked == False