#TODO some measure of closness in choosing targets/improve priority
#TODO add some kind of defense (see incoming drone and stay at zone). In first version only a shortranged defense is necesarry)
#IDEA evalute defense againts gettin more zones (distance ivaders versus distance cap)
        #if cap is closer maybe it's beter to cap? or is defence always betters
#FXME sometiems two drones go to the same open control zone
#REMARK better in versus compared to team games (prob because fixing your and your enemeies drones is positive in 1v1 but not so much in team)
        #Potentially diffe algo on player count

import sys
import math
import collections

#constants
ZONERADIUS =100

#init data structure
zones = []
drones = []
Pos = collections.namedtuple("Pos", ["x", "y"])

class Drone:
    def __init__(self, id):
        self.pos, self._targetZone, self.id = None, None, id

    def print_move(self):
        print(str(self.targetZone.pos.x) + " " + str(self.targetZone.pos.y))

    def find_target(self):
        sortedZones = sorted (zones, key=lambda z: z.priority())
        if sortedZones[-1].priority() < -50:
            self.set_target_zone_to_closest()
            print("D{} setting target to CLOSEST zone {}".format(self.id, self.targetZone), file=sys.stderr)

        else:
            self.targetZone = sortedZones[-1]
            print("D{} setting target PRIO zone {}".format(self.id, self.targetZone), file=sys.stderr)

    def set_target_zone_to_closest(self):
        minDist = 10000
        target = -1
        for z in zones:
            if distance(self.pos, z.pos) < minDist:
                target = z
                minDist = distance(self.pos, z.pos)
        self.targetZone = target

    def __repr__(self):
        return "D{}".format(self.id)

    def _set_target_zone(self, target):
        try:
            self.targetZone.drones.remove(self)
        except AttributeError:
            pass #do nothing is previous target ws None
        self._targetZone = target
        target.drones.append(self)

    def _get_target_zone(self):
        return self._targetZone

    targetZone = property(_get_target_zone, _set_target_zone)

class Zone:
    def __init__(self,id, pos):
        self.pos, self.id, self.controller, self.drones, self.playerDronesInZone = pos, id, -1, [], [0]*playerCount

    @property
    def maxEnemyCount(self):
        """ Current enemy count of the enemy with the most drones in this zone"""
        return max(self.playerDronesInZone[:playerId] + self.playerDronesInZone[playerId+1:])

    @property
    def futureCount(self):
        """Expected number of drones in the future """
        return len(self.drones)

    @property
    def control(self):
        if self.controller == playerId:
            return True
        return False

    def priority(self):
        #higer prio if number of enemies and our future drones are high
        if self.futureCount >= self.maxEnemyCount and self.control:
            return -100

        if self.futureCount >= self.maxEnemyCount + 1:
            return -100

        return - self.maxEnemyCount + self.futureCount


    def release_redundant_drones(self):
        #init vars
        enCount = self.maxEnemyCount
        futureCount = self.futureCount

        control = False
        if self.controller == playerId:
            control = True

        #goalcount is the number of drones requierd to acquire and/or maintain control
        if control:
            goalCount = enCount
        else:
            goalCount = enCount +1

        #delete redundant drones
        self._release_drones(futureCount - goalCount)

    def release_if_hopeless(self):
        """Release all drones if obtaining control of this zone seems hopeless"""
        if (not self.control) and self.futureCount <= self.maxEnemyCount:
            self._release_drones("all")



    def _release_drones(self, count):
        """Releases required number of drones. Also accepts string "all" """

        if isinstance(count, int) and  count<=0:
            return

        if count=="all":
            for d in self.drones:
                d.find_target()
        else:
            self.drones.sort( key = lambda d: distance(d.pos, self.pos))
            for d in self.drones[-count:]:
                d.find_target()

        print("Releasing {} drones from Z{}@({},{})".format(count, self.id, self.pos.x, self.pos.y), file= sys.stderr)



    def __repr__(self):
        return "Z{} Prio:{} Cont:{} Drone:{}".format(self.id, self.priority(), self.controller, self.drones)

#define helper functions
def distance(a, b):
    return math.sqrt((a.x -b.x) **2 + (a.y-b.y)**2)


# p: number of players in the game (2 to 4 players)
# id: ID of your player (0, 1, 2, or 3)
# d: number of drones in each team (3 to 11)
# z: number of zones on the map (4 to 8)
playerCount, playerId, droneCount, zoneCount = [int(i) for i in input().split()]
for id in range(zoneCount):
    # x: corresponds to the position of the center of a zone. A zone is a circle with a radius of 100 units.
    x, y = [int(j) for j in input().split()]
    zones.append( Zone(id=id,  pos=Pos(x,y)))
for id in range(droneCount):
    drones.append( Drone(id) )

# game loop
while True:
    #update gamestate
    for z in zones:
        test = int(input())
        z.controller = test  # ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled. The zones are given in the same order as in the initialization.
        z.playerDronesInZone = [0]*playerCount
    for i in range(playerCount):
        for d in drones:
            x, y = [int(k) for k in input().split()]
            pos = Pos(x,y)
            #Add drone to area if it's in it
            for z in zones:
                if distance(pos, z.pos)<ZONERADIUS:
                    z.playerDronesInZone[i]+=1
            #update player drone positions
            if i == playerId:
                d.pos = pos

    #print status
    for z in zones:
        print(z, file = sys.stderr)

    #make decisions
    for z in zones:
        z.release_redundant_drones()
    for z in zones:
        z.release_if_hopeless()

    #handle drones
    for d in drones:
        #fallback targeting
        if d.targetZone == None:
            d.set_target_zone_to_closest()

        d.print_move()
