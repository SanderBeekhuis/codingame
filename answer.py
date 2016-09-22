import sys
import math

#TODO lapscomplete counter increase above 1
#TODO measure approach speed (not just velocity)
#TODO look at overcorrecting when going to a checkpoint
#TODO use boost
#FIXME orientationdir seems wrong, or not
#TODO in normal operation make turn time instead of dstance dependent
#IDEA vary drift correction with distance

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

lapsComplete = 0 
checkpoints = []
finish = (-1, -1)
boostUsed = False
firstIteration = True

DRIFT_CORRECTION_CAP =20 # max correction angle for drift
STRUGLE_FLOOR = 150
TRIVAL_DRIFT_CORRECTION_BOUND = 4 #in degreees

TURNING_SPEED = 15 #Estimation

#computes smallest difference between two andles, asssumes degrees

def normalizeAngle(x):
    if x > 180:
        x -= 360
    if x < -180:
        x += 360 
    return x

def angleDiff(a , b):
    x = a - b
    x = normalizeAngle(x)
    return x
    
def angle(fromLoc, toLoc):
    #atan2 is in (yx) format!
     return math.degrees(math.atan2(toLoc[1] - fromLoc[1], toLoc[0]-fromLoc[0]))
    

def computeTarget(loc, direction):
    return (loc[0] + math.cos(math.radians(direction)) * 100, loc[1] + math.sin(math.radians(direction))*100 )

def outputTarget(target, thrust):
    print(str(int(target[0])) + " " + str(int(target[1])) + " " + str(int(thrust)))


def outputDir(loc, direction, thrust):
    print("Target direction: " +str(int(direction)) +
        " Thrust: " + str(int(thrust)), file =sys.stderr)
    outputTarget(computeTarget(loc, direction), thrust)

# game loop
while True:

    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, nextCheckpointX, nextCheckpointY, distance, nextCheckpointRelativeAngle = [int(i) for i in input().split()]
    opponentX, opponentY = [int(i) for i in input().split()]
    checkpointloc = (nextCheckpointX, nextCheckpointY)
    loc= (x,y)
    if firstIteration:
        prevLoc = loc
    speed = (loc[0] - prevLoc[0], loc[1] - prevLoc[1])
    velocity = math.sqrt(speed[0]*speed[0] + speed[1]*speed[1])
    movementDir = angle((0,0), speed)
    nextCheckpointAngle = angle( loc , checkpointloc)
    orientationDir = normalizeAngle(nextCheckpointAngle + nextCheckpointRelativeAngle)
    driftCorrection = min( DRIFT_CORRECTION_CAP, max ( angleDiff(nextCheckpointAngle, movementDir), - DRIFT_CORRECTION_CAP))
    nextChekpointTargetDir = nextCheckpointAngle + driftCorrection

    print("Velocity " + str(velocity), file = sys.stderr)
    print("Dist " + str(distance), file = sys.stderr)
    print("CP Dir " + str(nextCheckpointAngle), file = sys.stderr)
    print("orientationDir" + str(orientationDir), file = sys.stderr)
    print("movementDir" + str(movementDir), file = sys.stderr)
    print("Diff CP vs movement" + str(angleDiff(nextCheckpointAngle, movementDir)), file =sys.stderr)
    print("Drift correction" + str(driftCorrection), file = sys.stderr)
    #print("Loc" + str(loc), file = sys.stderr)

    
    ## OBTAIN course data ###
    if lapsComplete == 0:

    
        #init cp's if list is empty
        if firstIteration: 
            checkpoints.append(checkpointloc)
    
        #note we completed a lap if a checkpoit reoccurs
        if (len(checkpoints) > 1 and checkpoints[0] == checkpointloc):
            lapsComplete = 1
            finish = checkpoints[-1]
            
        #add cp's as long as no lap is complete    
        if checkpoints[-1] != checkpointloc:
            checkpoints.append(checkpointloc)

        
        if abs(nextCheckpointRelativeAngle) > 90:
            thrust = 0
        else:
            thrust = int(min(100, distance/10))
            

        outputDir(loc, nextChekpointTargetDir, thrust)



    ## PLAY
    else:
        checkpointid = checkpoints.index(checkpointloc)
        #print(checkpointid, file = sys.stderr)
                
        #determine target bearing of next section
        checkpointAfter = checkpoints[ (checkpointid +1) % len(checkpoints) ]
        nextSectionBearing = angle(checkpointloc, checkpointAfter  )
        
        
        #Q is it better to base this on orientattion ipv. direction? Does it matter when we are in normal operation?
        directionChange = abs(angleDiff(nextCheckpointAngle, nextSectionBearing))
       
        print("Dir change"+ str(directionChange), file = sys.stderr)
        print("", file = sys.stderr)
        
        # You have to output the target position
        # followed by the power (0 <= thrust <= 100)
        # i.e.: "x y thrust"
        
        
        #priority 1 reorient
        if abs(nextCheckpointRelativeAngle) > 90:
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

    ## END OF LOOP
    prevLoc = (x,y)
    prevDistace = distance
    firstIteration = False
    #print(checkpoints, file = sys.stderr)
    #print(lapsComplete, file = sys.stderr)

