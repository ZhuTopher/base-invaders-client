from math import cos, sin, atan2, pi, sqrt, pow

def toProperRad(a):
    return a + pi

# requires that ship has prev and current fields init'd
def  calculateAccel(ship):
	deltaT = ship.timePrev-ship.time

	ax = ((ship.dx-ship.dxPrev)/deltaT)
	ay = ((ship.dy-ship.dyPrev)/deltaT)

	aMag = sqrt(pow(ax, 2) + pow(ay, 2))
	theta = toProperRad(atan2(ay, ax))

	return (aMag, theta)