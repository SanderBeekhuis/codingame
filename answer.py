import sys
import math
import collections
import numbers

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
boostUsed = [False, False]

Bot = collections.namedtuple("Bot", ['loc',
                        'velocity',
                        'distance',
                        'nextCheckpointDir',
                        'movementDir',
                        'headingDir',
                        'driftAngle',
                        'nextSectionBearing',
                        'directionChangeAfterNextCheckpoint'])

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

def outputDir(loc, direction, thrust):
    if isinstance( thrust, numbers.Number):
        thrust = int(thrust)
    print("Target direction: " +str(int(direction)) +
        " Thrust: " + str(thrust), file =sys.stderr)
    target = computeTarget(loc, direction)
    print(str(int(target[0])) + " " + str(int(target[1])) + " " + str(thrust))

def nextId(id):
    return (id +1) % checkpointCount

def handleData(debugPrint = False):
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

    #determine target bearing of next section
    checkpointAfter = checkpoints[ nextId(nextCheckpointId) ]
    nextSectionBearing = computeAngle(checkpointloc, checkpointAfter)

    #fix headingdir
    if headingDir == -1 : # at start of the game
        headingDir = nextCheckpointDir
    headingDir = normalizeAngle(headingDir)

    #Q is it better to base this on orientattion or direction? Does it matter when we are in normal operation?
    directionChange = abs(diffAngle(nextCheckpointDir, nextSectionBearing))

    result =Bot(loc=loc,
                velocity=velocity,
                distance=distance,
                headingDir=headingDir,
                movementDir=movementDir,
                nextCheckpointDir=nextCheckpointDir,
                driftAngle=driftAngle,
                nextSectionBearing=nextSectionBearing,
                directionChangeAfterNextCheckpoint=directionChange)

    if debugPrint:
        print(result, file = sys.stderr)
    return result

def handleBot(botId, botData, tactic):
    assert  (tactic == "agr" or tactic == "fast")
    thisBot = botData[botId]

    driftCorrection = min( DRIFT_CORRECTION_CAP, max (thisBot.driftAngle , - DRIFT_CORRECTION_CAP))
    nextChekpointTargetDir = thisBot.nextCheckpointDir + driftCorrection


    #default target
    target = nextChekpointTargetDir

    #priority 1 reorient
    if abs(diffAngle(thisBot.headingDir, thisBot.nextCheckpointDir)) > 90:
        print("Reorienting", file = sys.stderr)
        thrust =0


    #use boost at start
    elif tactic == "fast" and boostUsed[botId] == False:
        boostUsed[botId] =True
        thrust = "BOOST"

    #prio 2: struglling
    elif thisBot.velocity < STRUGLE_FLOOR:
        print("Strugle detected", file = sys.stderr)
        thrust = 100

    elif abs(driftCorrection) >TRIVAL_DRIFT_CORRECTION_BOUND:
        print("nontrivial drift correction", file = sys.stderr)
        thrust = 100

    #prio 3 normal operation
    else:

        print("Normal Operation", file = sys.stderr)
        turnsToChekpoint = thisBot.distance/thisBot.velocity
        turnsToTurn = max(thisBot.directionChangeAfterNextCheckpoint-2*TURNING_SPEED, 0) /TURNING_SPEED  #litte bit of turning is free

        #TODO do somthing with drag instead of magic constant 2
        if turnsToChekpoint < turnsToTurn/2:
            print("Turning", file = sys.stderr)
            thrust = 0
            target = nextSectionBearing
        else:
            thrust = 100
    outputDir(thisBot.loc, target, thrust)

print("Starting game loop", file =sys.stderr)
# game loop
while True:
    bots = [handleData(debugPrint=True), handleData(), handleData(), handleData(),]
    handleBot(0, bots, tactic="fast")
    handleBot(1, bots, tactic="fast")
