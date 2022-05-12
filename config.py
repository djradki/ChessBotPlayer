from enum import Enum


class Config(object):
    class PlayerType(Enum):
        TIME = 0
        DEPTH = 1
        CLOCK_TIME = 2

    path = ""           #absolute path to Engine
    threads = 8                 #processor threads used by Engine
    hashMemory = 4096           #hash memory used by Engine (MB)
    depth = 28                  #depth used by Engine with DEPTH Type (see below)
    moveTime = 2000             #time for static move used by Engine with MOVE_TIME Type (see below)
    playerType = PlayerType.CLOCK_TIME

    isSlowMover = True          #if Player should wait if Engine computation is faster than threshold
    slowMoverTreshold = 2000    #time to activate slow mover

