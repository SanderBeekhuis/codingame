"""
This algorithm works in a taskbased manner.
Zone create different tasks with different priorities.
These Tasks are assigned to drones on bassis of both priority(first) and
closness(second) and are then executed
"""


#TODO add some kind of defense task (see incoming drone and recruit at zone). Using that the dronelist now has all drones (maybe track direction and speed in drones)
#TODO Better tradeoff betwee of closness and priority in choosing targets
#       Maybe let drones pick closeby tasks (between same prio) instead of tasks chosing the drone
# Or antoerd IDEA First free all drones, then assign inteligently (see above)

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
ZONERADIUS = 100
MOVESPEED = 100

#tuning
IDLEPOS = None
ADVANCEWARNINGRADIUS =1000

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
        """Acquire closest drones for this task.
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
    """Idiling at a zone to maintain Control """
    @property
    def priority(self):
        """priority of this task. Higher is more important"""
        return 2000

class IdleTask(Task):
    """Assigned if no other task could be found """
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
    def __init__(self, id, controller):
        self._pos, self._prevpos, self._task, self.id, self.controller = None, None, None, id, controller

    def print_move(self):
        assert self.controller == playerId
        print(str(int(self.task.pos.x)) + " " + str(int(self.task.pos.y)))

    def __str__(self):
        result = "P{}D{}".format(self.controller, self.id)
        if controller == playerId:
            result +=  " Task:{}".format(self.task)
        return result;

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, value):
        assert self.controller == playerId
        self._task = value

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._prevpos = self._pos
        self._pos = value

    @property
    def prevpos(self):
        return self._prevpos

class Zone:
    def __init__(self,id, pos):
        self.pos, self.id, self.controller = pos, id, -1

    @property
    def control(self):
        if self.controller == playerId:
            return True
        return False


    def _maxEnemyCount(self, dronesToCount):
        """ Current enemy count of the enemy with the most drones in this zone"""
        return max(dronesToCount[:playerId] + dronesToCount[playerId+1:])

    def tasks(self, drones):
        """Returns a list of tasks this zone wants to see fullfilled """
        #calculate intemediatairy data

        playerDronesInZone = [0]*playerCount #init
        playerDronesInbound = [0]*playerCount
        inboundDrones = []

        for d in drones:
            dist = distance(d.pos, self.pos)
            if d.prevpos is None:
                prevdist = dist
            else:
                prevdist = distance(d.prevpos, self.pos)
            if dist<ZONERADIUS:
                playerDronesInZone[d.controller]+=1
            elif dist < ADVANCEWARNINGRADIUS and dist < (prevdist - .95 * MOVESPEED):
                inboundDrones.append({"drone": d, "dist":dist})
                playerDronesInbound[d.controller] += 1

        print( "Z{} Cont:{} Drones:{}{}".format(self.id, self.controller, playerDronesInZone, playerDronesInbound),file=sys.stderr)


        #return tasks
        if self.control:
            return [ MaintainControlTask(self._maxEnemyCount(playerDronesInZone), self) ]
        else:
            return [ AttackTask(self._maxEnemyCount(playerDronesInZone)+1, self) ]

    def __str__(self):
        return "Z{} Cont:{}".format(self.id, self.controller)

#INIT
playerCount, playerId, droneCount, zoneCount = [int(i) for i in input().split()]
idlex, idley = 0, 0
for id in range(zoneCount):
    x, y = [int(j) for j in input().split()]
    zones.append( Zone(id=id,  pos=Pos(x,y)))
    idlex += x/zoneCount
    idley += y/zoneCount
IDLEPOS = Pos(idlex,idley)

for controller in range(playerCount):
    for id in range(droneCount):
        drones.append( Drone(id, controller) )

print("Init complete", file=sys.stderr)


#GAME LOOP
while True:
    #update gamestate
    for z in zones:
        z.controller = int(input()) # ID of the team controlling the zone (0, 1, 2, or 3) or -1 if it is not controlled. The zones are given in the same order as in the initialization.
    for i in range(playerCount*droneCount):
        x, y = [int(k) for k in input().split()]
        drones[i].pos = Pos(x,y)

    print("Input read", file=sys.stderr)

    #make decisions
    tasks = []
    freedrones = list(filter( lambda d: d.controller == playerId, drones))
    for z in zones:
        tasks += z.tasks(drones)
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
    for d in filter(lambda d: d.controller == playerId, drones):
        d.print_move()
