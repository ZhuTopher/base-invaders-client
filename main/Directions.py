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

# requires that ship has prev and current fields init'd
def targettedAccel(ship, xMine, yMine):
	mineTheta = toProperRad(atan2(
		(yMine-ship.y), (xMine-ship.x)))

	vMag = sqrt(pow(ship.dx, 2) + pow(ship.dy, 2))

	# Equations from .docx
	ax = (vMag*(cos(ship.angle))) - (vMag*(cos(mineTheta)))
	ay = (vMag*(sin(ship.angle))) - (vMag*(sin(mineTheta)))

	aMag = sqrt(pow(ax, 2), pow(ay, 2))
	theta = toProperRad(atan2(ay, ax))


	return (aMag, theta)