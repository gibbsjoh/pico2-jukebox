import json
import os
import asyncio
import audiomp3
import audiopwmio
import board
import time
import digitalio
from async_button import SimpleButton
import menuFunctions
from miscFunctions import showFreeMem
from fileops import getTrackInfoAsList

audio = audiopwmio.PWMAudioOut(left_channel=board.GP18, right_channel=board.GP19)

# function to stream mp3 audio
# this may require the stream to be transcoded, which the pico won't be able to do
# I have thrown together a node.js app to do this at https://github.com/gibbsjoh/streamconvert
# obvs requires a wifi-enabled board!

# button listener for pause/play (using onboard buttons on SeenGreat board, GP20)
async def pauseButtonListener():
    global audio
    #using SimpleButton now
    playPauseButton = SimpleButton(board.GP21, value_when_pressed=False)
    
    while True:
        # Wait until button is pressed
        await playPauseButton.pressed()
        print("Play/pause button pressed")
        if audio.playing is True and audio.paused is False:
            audio.pause()
        elif audio.playing is True and audio.paused is True:
            audio.resume()

        # Wait until button is released
        await playPauseButton.released()

def playAll(tracksDict):
    # plays all tracks sequentially
    theArtistsList = list(tracksDict.keys())

async def goToNext(startingTrack, totalTracks, displayEnabled):
    currentTrack = startingTrack
    while True:
        if audio.playing is False:
            # for fun, show free memory
            showFreeMem()
            if currentTrack < totalTracks:
                currentTrack = currentTrack + 1
            else:
                currentTrack = currentTrack + 1
            # refresh display if display enabled
            if(displayEnabled == 1):
                thisTrackInfo = getTrackInfoAsList(tracksList[currentTrack])
                nowPlayingArtist = thisTrackInfo[0]
                nowPlayingAlbum = thisTrackInfo[1]
                nowPlayingTrack = thisTrackInfo[2]
                menuFunctions.displayTrackInfo(nowPlayingArtist, nowPlayingAlbum, nowPlayingTrack)
            
            playMP3Task = asyncio.create_task(playMP3(tracksList[currentTrack]))
            await asyncio.gather(playMP3Task)
        await asyncio.sleep(0.1)

async def playMP3(filePath):
    global audio
    print("Playing ", filePath)
    thePath = filePath if "/sd/" in filePath else "/sd/" + filePath
    decoder = audiomp3.MP3Decoder(open(thePath, "rb"))
    audio.play(decoder)
    await asyncio.sleep(0.1)