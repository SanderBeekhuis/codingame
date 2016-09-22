import sys
import math

#Algorithm parameters
DRIFT_CORRECTION_CAP =20 # max correction angle for drift
STRUGLE_FLOOR = 150
TRIVAL_DRIFT_CORRECTION_BOUND = 4 #in degreees

#Phisics constants
TURNING_SPEED = 18
FRICTION = 0.85
#computes smallest difference between two andles, asssumes degrees



#TODO lapscomplete counter increase above 1
#TODO measure approach speed (not just velocity)
#TODO look at overcorrecting when going to a checkpoint
#TODO use boost
#TODO in normal operation make turn time instead of dstance dependent
#IDEA vary drift correction with distance

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

lapsComplete = 0
checkpoints = []
finish = (-1, -1)
boostUsed = False


#initialization input
lapCount = int(input())
checkpointCount = int(input())
for _ in range(checkpointCount):
    x,y = [int(i) for i in input().split()]
    checkpoints.append((x,y))

#Method definitions
def normalizeAngle(x):
    if x > 180:
        x -= 360
    if x < -180:
        x += 360
    return x

def diffAngle(a , b):
    x = a - b
    x = normalizeAngle(x)
    return x

def computeAngle(fromLoc, toLoc):
    #atan2 is in (yx) format!
    return math.degrees(math.atan2(toLoc[1] - fromLoc[1], toLoc[0]-fromLoc[0]))

def computeDistance(a,b):
    return math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

def computeTarget(loc, direction):
    return (loc[0] + math.cos(math.radians(direction)) * 100, loc[1] + math.sin(math.radians(direction))*100 )

def outputTarget(target, thrust):
    print(str(int(target[0])) + " " + str(int(target[1])) + " " + str(int(thrust)))

def outputDir(loc, direction, thrust):
    print("Target direction: " +str(int(direction)) +
        " Thrust: " + str(int(thrust)), file =sys.stderr)
    outputTarget(computeTarget(loc, direction), thrust)

def nextId(id):
    return (id +1) % checkpointCount

def handleBot(botNo):
    x, y, vx, vy, headingDir, nextCheckpointId = [int(i) for i in input().split()]
    checkpointloc = checkpoints[nextCheckpointId]
    loc= (x,y)
    speed = (vx, vy)
    velocity = math.sqrt(speed[0]*speed[0] + speed[1]*speed[1])
    movementDir = computeAngle((0,0), speed)

    distance = computeDistance(loc, checkpointloc)
    nextCheckpointDir = computeAngle(loc , checkpointloc)

    driftAngle =diffAngle(nextCheckpointDir, movementDir)
    driftCorrection = min( DRIFT_CORRECTION_CAP, max (driftAngle , - DRIFT_CORRECTION_CAP))
    nextChekpointTargetDir = nextCheckpointDir + driftCorrection

    print("Velocity " + str(velocity), file = sys.stderr)
    print("Dist " + str(distance), file = sys.stderr)
    print("CP Dir " + str(nextCheckpointDir), file = sys.stderr)
    print("headingDir" + str(headingDir), file = sys.stderr)
    print("movementDir" + str(movementDir), file = sys.stderr)
    print("Diff CP vs movement" + str(diffAngle(nextCheckpointDir, movementDir)), file =sys.stderr)
    print("Drift correction" + str(driftCorrection), file = sys.stderr)

    #determine target bearing of next section
    checkpointAfter = checkpoints[ nextId(nextCheckpointId) ]
    nextSectionBearing = computeAngle(checkpointloc, checkpointAfter)


    #Q is it better to base this on orientattion or direction? Does it matter when we are in normal operation?
    directionChange = abs(diffAngle(nextCheckpointDir, nextSectionBearing))

    print("Dir change"+ str(directionChange), file = sys.stderr)
    print("", file = sys.stderr)



    #priority 1 reorient
    if abs(diffAngle(headingDir, nextCheckpointDir)) > 90:
        print("Reorienting", file = sys.stderr)
        thrust =0
        target = nextChekpointTargetDir


    #prio 2: struglling
    elif velocity < STRUGLE_FLOOR:
        print("Strugle detected", file = sys.stderr)
        thrust = 100
        target = nextChekpointTargetDir

    elif abs(driftCorrection) >TRIVAL_DRIFT_CORRECTION_BOUND:
        print("nontrivial drift correction", file = sys.stderr)
        thrust = 100
        target = nextChekpointTargetDir

    #prio 3 normal operation
    else:

        print("Normal Operation", file = sys.stderr)
        turnsToChekpoint = distance/velocity
        turnsToTurn = max(directionChange-2*TURNING_SPEED, 0) /TURNING_SPEED  #litte bit of turning is free

        #TODO do somthing with drag instead of magic constant 2
        if turnsToChekpoint < turnsToTurn/2:
            print("Turning", file = sys.stderr)
            thrust = 0
            target = nextSectionBearing
        else:
            thrust = 100
            target = nextChekpointTargetDir
    outputDir(loc, target, thrust)

print("Starting game loop", file =sys.stderr)
# game loop
while True:
    handleBot(0)
    handleBot(1)

    ##READ out oppennets to throw input away
    opponent1X, opponent1Y, _, _ ,_ ,_ = [int(i) for i in input().split()]
    opponent2X, opponent2Y, _, _ ,_ ,_ = [int(i) for i in input().split()]

    #print(checkpoints, file = sys.stderr)
    #print(lapsComplete, file = sys.stderr)
