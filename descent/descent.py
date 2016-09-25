import sys
import math
import collections

# The while loop represents the game.
# Each iteration represents a turn of the game
# where you are given inputs (the heights of the mountains)
# and where you have to print an output (the index of the mountain to fire on)
# The inputs you are given are automatically updated according to your last actions.

Mountain = collections.namedtuple('Mountain', ['pos','height'])




# game loop
while True:
    mountains = []
    for i in range(8):
        mountains.append( Mountain(pos=i, height=int(input())) )
    mountains.sort(key= lambda m: m.height)
    print( str(mountains.pop().pos))

