"""
This algorithm works in a taskbased manner.
Zone create different tasks with different priorities.
These Tasks are assigned to drones on bassis of both priority(first) and
closness(second) and are then executed
"""


#TODO add some kind of defense task (see incoming drone and recruit at zone).
# In first version only a shortranged defense is necesarry)
#TODO Better tradeoff betwee of closness and priority in choosing targets
#       Maybe let drones pick closeby tasks (between same prio) instead of tasks chosing the drone
#IDEA evalute defense againts gettin more zones (distance ivaders versus distance cap)
#	If cap is closer maybe it's beter to cap? or is defence always betters

#TODO intra-zone positioning while holding zone

#REMARK better in versus compared to team games (prob because fixing your and your enemeies drones is positive in 1v1 but not so much in team)
#	-Potentially differ algo on player count
#	-DronePerZoneRatio = drones/zones
#	-If we fix more then constant times this ratio on a zone, drop the zone altogether
#	-e.g 2players never drop, 3 players drop with more then 3*DPZratio 4 players 2 times DPZ ratio

import sys
import math
import collections
import copy

#constants
ZONERADIUS =100
IDLEPOS = None

#init data structure
zones = []
drones = []

#define helper functions
def distance(a, b):
    return math.sqrt((a.x -b.x) **2 + (a.y-b.y)**2)

#define classes
Pos = collections.namedtuple("Pos", ["x", "y"])

class Task:
    """
        Tasks are atomic assignments. Either all drones should be found or the enitre operation is cancelled.
        """
    def __init__(self, dronesRequired, zone):
        self.dronesRequired, self.zone = dronesRequired, zone
        self.pos = zone.pos

    def __str__(self):
        return "{} with Zone {} and Prio {}".format(type(self).__name__, self.zone, self.priority)

    @property
    def priority(self):
        """priority of this task. Higher is more important"""
        raise NotImplementedError()

    def acquire_drones(self, freedrones):
        """acquire closest drones for this task.
        Subclasses can overwrite this method to for example conditnally acquire drones  """
        freedrones.sort(key=lambda d:distance(d.pos, self.zone.pos))
        for _ in range(self.dronesRequired):
            d = freedrones.pop(0)
            d.task = self

class AttackTask(Task):
    """moving to some uncontrolled zone to acquire it """
    @property
    def priority(self):
        """priority of this task. Higher is more important"""
        return 1000 + 100 - self.dronesRequired

class MaintainControlTask(Task):
    """idiling at a zone to maintain Control """
    @property
    def priority(self):
        """priority of this task. Higher is more important"""
        return 2000

class IdleTask(Task):
    """assigned if no other task could be found """
    def __init__(self):
        self.dronesRequired = 1
        self.pos = IDLEPOS
        self.zone = None

    @property
    def priority(self):
        """priority of this task. Higher is more important"""
        return -1000

    def acquire_drones(self, freedrones):
        """ overwrite without sorting """
        d = freedrones.pop()
        d.task = self

class Drone:
    def __init__(self, id):
        self.pos, self.task, self.id = None, None, id

    def print_move(self):
        print(str(int(self.task.pos.x)) + " " + str(int(self.task.pos.y)))

    def __str__(self):
        return "D{} Task:{}".format(self.id, self.task)

class Zone:
    def __init__(self,id, pos):
        self.pos, self.id, self.controller, self.playerDronesInZone = pos, id, -1, [0]*playerCount

    @property
    def maxEnemyCount(self):
        """ Current enemy count of the enemy with the most drones in this zone"""
        return max(self.playerDronesInZone[:playerId] + self.playerDronesInZone[playerId+1:])

    @property
    def control(self):
        if self.controller == playerId:
            return True
        return False

    def tasks(self):
        """Returns a list of tasks this zone wants to see fullfilled """
        if self.control:
            return [MaintainControlTask(self.maxEnemyCount, self)]
        else:
            return [AttackTask(self.maxEnemyCount+1, self)]

    def __str__(self):
        return "Z{} Cont:{}".format(self.id, self.controller)

playerCount, playerId, droneCount, zoneCount = [int(i) for i in input().split()]
idlex, idley = 0, 0
for id in range(zoneCount):
    x, y = [int(j) for j in input().split()]
    zones.append( Zone(id=id,  pos=Pos(x,y)))
    idlex += x/zoneCount
    idley += y/zoneCount
IDLEPOS = Pos(idlex,idley)

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
    #for z in zones:
    #    print(z, file = sys.stderr)

    #make decisions
    tasks = []
    freedrones = copy.copy(drones)
    for z in zones:
        tasks += z.tasks()
    for _ in drones:
        tasks += [IdleTask()]

    tasks.sort(key=lambda t: t.priority, reverse=True)

    print("TASKS", file=sys.stderr)
    for t in tasks:
        print(t, file=sys.stderr)

    for t in tasks:
        if len(freedrones) >= t.dronesRequired:
            t.acquire_drones(freedrones)
    assert len(freedrones) == 0

    print("DRONES", file=sys.stderr)
    for d in drones:
        print(d, file=sys.stderr)

    #move drones
    for d in drones:
        d.print_move()
