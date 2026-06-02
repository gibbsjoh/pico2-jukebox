# any functions that don't really live anywhere else!
import random
import time
import gc
import asyncio

def trackRandomiser(maximum, excludeList):
    # generates a random number based on the "maximum" that isn't in "excludeList"
    theNumber = -1 # set to something outside the range
    while (theNumber in excludeList or theNumber == -1):
        theNumber = random.randrange(0,maximum,1)
    return theNumber

def showFreeMem():
    print(gc.mem_free())