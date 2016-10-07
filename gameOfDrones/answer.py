#FXME zone ownership
#FXME make drone +zone class
#Feature how many drones in a zone

import sys
import math
import collections

#init data structure
zones = []
drones = []
Pos = collections.namedtuple("Pos", ["x", "y"])

class Drone:
    def __init__(self):
        self.pos, self.targetZone = None, None

    def printMove(self):
        print(str(self.targetZone.pos.x) + " " + str(self.targetZone.pos.y))

    def setTargetZoneToClosest(self):
        minDist = 10000
        target = -1
        for z in zones:
            if distance(self.pos, z.pos) < minDist:
                target = z
                minDist = distance(self.pos, z.pos)
        self.targetZone = target


class Zone:
    def __init__(self, pos):
        self.pos, self.controller = pos, -1

#define helper functions
def distance(a, b):
    return math.sqrt((a.x -b.x) **2 + (a.y-b.y)**2)


# p: number of players in the game (2 to 4 players)
# id: ID of your player (0, 1, 2, or 3)
# d: number of drones in each team (3 to 11)
# z: number of zones on the map (4 to 8)
playerCount, playerId, droneCount, zoneCount = [int(i) for i in input().split()]
for _ in range(droneCount):
    drones.append( Drone() )
for _ in range(zoneCount):
    # x: corresponds to the position of the center of a zone. A zone is a circle with a radius of 100 units.
    x, y = [int(j) for j in input().split()]
    zones.append( Zone( Pos(x,y)))

# game loop
while True:
    for z in zones:
        z.controler = int(input())  # ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled. The zones are given in the same order as in the initialization.
    for i in range(playerCount):
        for d in drones:
            # x: The first D lines contain the coordinates of drones of a player with the ID 0, the following D lines those of the drones of player 1, and thus it continues until the last player.
            x, y = [int(k) for k in input().split()]
            if i == playerId:
                d.pos = Pos(x,y)

    for d in drones:
        if d.targetZone == None:
            d.setTargetZoneToClosest()

        d.printMove()
