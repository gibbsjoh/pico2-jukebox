# Pi Pico (1/2) jukebox v2
# Started 03/04/26
# https://github.com/gibbsjoh/pico2-jukebox

# imports
import board
import time
import busio
import digitalio
import sdcardio
import storage
import os
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1106
# import audiopwmio
import adafruit_sdcard
import microcontroller
import asyncio
import adafruit_ticks
import json

# custom functions from other files
import fileops
#import menuFunctions
import audioFunctions
from miscFunctions import trackRandomiser, showFreeMem
import menuFunctions

# options from settings.toml
overclockToggle = os.getenv("overclockToggle")
initSDCard = os.getenv("initSDCard")
playMP3OnStart = os.getenv("playMP3OnStart")
displayEnabled = os.getenv("displayEnabled")

# show current cpu speed and then overclock
currentCPUFrequencyString = str((microcontroller.cpu.frequency / 1000000)) + "MHz"
print("Default CPU frequency:", currentCPUFrequencyString)
if (overclockToggle == 1):
    print("Overclocking...")
    try:
        microcontroller.cpu.frequency = 200000000  # 200 MHz
        currentCPUFrequencyString = str((microcontroller.cpu.frequency / 1000000)) + "MHz"
        print("New CPU frequency:", currentCPUFrequencyString )
    except AttributeError:
        print("Overclocking not supported in this CircuitPython build.")
    except ValueError as e:
        print("Invalid frequency:", e)
        

# set up LCD panel (sh1106 in this case, using i2c
# Always release any previous displays
displayio.release_displays()

# initialise oled display if displayEnabled = 1

# Create the I2C interface
i2c = busio.I2C(board.GP3, board.GP2) 
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)  # Change if needed

# Create the SH1106 display object
display = adafruit_displayio_sh1106.SH1106(
    display_bus,
    width=128,
    height=64
)

displayGroup = displayio.Group()

# display a welcome message
textLine1 = label.Label(
    terminalio.FONT,
    text="Welcome!",
    color=0xFFFFFF,
    x=10,
    y=10
)
textLine2 = label.Label(
    terminalio.FONT,
    text="Pico2Jukebox",
    color=0xFFFFFF,
    x=10,
    y=25
)

textLine3 = label.Label(
    terminalio.FONT,
    text="Overclocked! " + currentCPUFrequencyString,
    color=0xFFFFFF,
    x=10,
    y=40
)

displayGroup.append(textLine1)
displayGroup.append(textLine2)
displayGroup.append(textLine3)

display.root_group= displayGroup
# myGroup.append(thisText)
# display.root_group = thisText

time.sleep(3)
splash = displayio.Group()
display.root_group = splash

# initialise the SD card interface
theFiles = fileops.setupSDCard()

# build the artist -> album -> tracks dictionary
tracksDictionary = fileops.buildTracksDict(theFiles)
tracksList = fileops.buildFlatTracksList(tracksDictionary)

# set the start track to index 0
startingTrack = 0
#set the total tracks to the total number in tracksList
totalTracks = len(tracksList) - 1 # -1 because indexes start at zero!

# checkTime for loop to show free mem
checkTime = time.monotonic()
# inject the display object into menuFunctions
menuFunctions.display = display
# inject the tracksList var to audioFunctions
audioFunctions.tracksList = tracksList

async def main():  # calls all the functions using asyncio
    playMP3Task = asyncio.create_task(audioFunctions.playMP3(tracksList[0]))
    
    # ***
    # display the first track info - next track info is handled by audioFunctions.goToNext()
    thisTrackInfo = fileops.getTrackInfoAsList(tracksList[0])
    nowPlayingArtist = thisTrackInfo[0]
    nowPlayingAlbum = thisTrackInfo[1]
    nowPlayingTrack = thisTrackInfo[2]
    menuFunctions.displayTrackInfo(nowPlayingArtist, nowPlayingAlbum, nowPlayingTrack)
    # ****
    
    goToNextTask = asyncio.create_task(audioFunctions.goToNext(startingTrack, totalTracks, displayEnabled))
    pauseButtonListenerTask = asyncio.create_task(audioFunctions.pauseButtonListener())
    await asyncio.gather(playMP3Task)
    await asyncio.gather(goToNextTask)
    await asyncio.gather(pauseButtonListenerTask)
    await asyncio.sleep(0.1)


asyncio.run(main())