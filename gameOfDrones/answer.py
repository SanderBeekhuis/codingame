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
    def
Drone = collections.namedtuple("Drone", ["pos", "target"])
Zone = collections.namedtuple("Zone", ["pos", "controller"])

#define helper functions
def distance(a, b):
    return math.sqrt((a.x -b.x) **2 + (a.y-b.y)**2)



# p: number of players in the game (2 to 4 players)
# id: ID of your player (0, 1, 2, or 3)
# d: number of drones in each team (3 to 11)
# z: number of zones on the map (4 to 8)
playerCount, playerId, droneCount, zoneCount = [int(i) for i in input().split()]
for _ in range(droneCount):
    drones.append( Drone(None, None) )
for _ in range(zoneCount):
    # x: corresponds to the position of the center of a zone. A zone is a circle with a radius of 100 units.
    x, y = [int(j) for j in input().split()]
    zones.append( Zone( Pos(x,y),  -1))

# game loop
while True:
    for i in range(zoneCount):
        tid = int(input())  # ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled. The zones are given in the same order as in the initialization.
    for i in range(playerCount):
        for d in drones:
            # x: The first D lines contain the coordinates of drones of a player with the ID 0, the following D lines those of the drones of player 1, and thus it continues until the last player.
            x, y = [int(k) for k in input().split()]
            if i == playerId:
                d.pos = Pos(x,y)

    for d in drones:
        if d.target == None:
            minDist = 10000
            target = -1
            for z in zones:
                if distance(d.pos, z.pos) < minDist:
                    target = z
                    minDist = distance(d.pos, z.pos)

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)


        # output a destination point to be reached by one of your drones. The first line corresponds to the first of your drones that you were provided as input, the next to the second, etc.
        print(str(d.target.pos.x) + " " + str(d.target.pos.y))
