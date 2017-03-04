from Commands import Commands

from operator import sub

from math import atan2, pi

commands = Commands()

def toProperRad(a):
    while a < 0.0:
        a += pi * 2
    return a

# ship stats
x = 0
y = 0
dx = 0
dy = 0
angle = toProperRad(atan2(y, x))

def calculateScore(pos1, pos2):
    diff = [map(sub, pos2, pos1)]
    angles = [toProperRad(atan2(p[1], p[0])) for p in diff]
    scores = [calc]


def findBestMine(mines):
    positionDeltas = [positionDelta((x, y), m[1:]) for m in mines]

def makeDecision():
    status_dict = commands.getStatus()
    mines = status_dict['mine']
    if mine:
        closestMine = findClosestMine()

if __name__ == 'main':
    status_dict = commands.getStatus()
    x = status_dict['x']
    y = status_dict['y']
    dx = status_dict['dx']
    dy = status_dict['dy']
    while(True):
        makeDecision()