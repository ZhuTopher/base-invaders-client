from Commands import Commands

commands = Commands()

# ship stats
x = 0
y = 0
dx = 0
dy = 0

def positionDelta(pos1, pos2):


def findClosestMine(mines):


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