#TODO symmetry breaking/ release drones in losing situation

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

    def _max_enemies(self):
        return max(self.playerDronesInZone[:playerId] + self.playerDronesInZone[playerId+1:])

    def _future_drones(self):
        return len(self.drones)

    def priority(self):
        #higer prio if number of enemies and our future drones are high
        enCount = self._max_enemies()
        futureCount = self._future_drones()
        control = False
        if self.controller == playerId:
            control = True
        if futureCount >= enCount and control:
            return -100

        if futureCount >= enCount + 1:
            return -100

        return - enCount + futureCount

    def release_redundant_drones(self):
        #init vars
        enCount = self._max_enemies()
        ourCount = self.playerDronesInZone[playerId]
        futureCount = self._future_drones()

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


    def _release_drones(self, count):
        if count>0:
            print("Releasing {} drones from Z{}@({},{})".format(count, self.id, self.pos.x, self.pos.y), file= sys.stderr)
            self.drones.sort( key = lambda d: distance(d.pos, self.pos))
            for d in self.drones[-count:]:
                d.find_target()


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

    #handle drones
    for d in drones:
        #fallback targeting
        if d.targetZone == None:
            d.set_target_zone_to_closest()

        d.print_move()
