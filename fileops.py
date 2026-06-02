import os
import board
import sdcardio
import busio
import storage
import json

def setupSDCard():
    spi = busio.SPI(clock=board.GP10, MOSI=board.GP11, MISO=board.GP12)
    cs = board.GP15
    sd = sdcardio.SDCard(spi, cs)
    print("file init:",sd)
    # set up as a vfs
    vfs = storage.VfsFat(sd)
    print("mount:",vfs)
    # mount the vfs storage
    storage.mount(vfs, "/sd")
    # get dir listing
    dirs = os.listdir("/sd")
    return dirs

def buildTracksDict(theFiles):
    tracksJSON = {}
    tracksTotal = 0
    print("SD card listing")
    for artistDir in theFiles:
        # get the album dirs
        if (artistDir[0] != "."):
            print(artistDir)
            # add artist to JSON
            tracksJSON[artistDir] = {}
            thisAlbumPath = "/sd/" + artistDir
            albumDirs = os.listdir(thisAlbumPath)
            for albumDir in albumDirs:
                if ( albumDir[0] != "." ):
                    # add album to JSON
                    tracksJSON[artistDir][albumDir] = {}
                    print(" --> ", albumDir)
                    thisAlbumPath = "/sd/" + artistDir + "/" + albumDir
                    print(thisAlbumPath)
                    thisAlbumFiles = os.listdir(thisAlbumPath)
                    for mp3File in thisAlbumFiles:
                        if ( mp3File[0] != "." ):
                            # add mp3 file to JSON
                            tracksTotal += 1
                            thisSongPath = "/sd/" + artistDir + "/" + albumDir + "/" + mp3File
                            tracksJSON[artistDir][albumDir][mp3File] = ({"trackNumber":tracksTotal,"file":mp3File,"path":thisSongPath})
                            print("    ----> ", mp3File)
    return tracksJSON

def buildFlatTracksList(tracksJSON):
    # builds a flat list of tracks for continuous play
    flatTracksList = []
    for key in tracksJSON:
        thisArtist = tracksJSON[key]
        for album in thisArtist:
            # albums
            thisAlbum = album
            thisAlbumJSON = tracksJSON[key][thisAlbum]
            for track in thisAlbumJSON:
                thisTrack = thisAlbumJSON[track]
                flatTracksList.append(thisTrack["path"])
    return flatTracksList

def getTrackInfoAsList(pathString):
    theList = pathString.split("/")
    theArtist = theList[2]
    theAlbum = theList[3]
    theSong = theList[4].split(" - ")[2]
    return theArtist, theAlbum, theSong


#             for key in thisAlbum:
#                 print(key)
            
#             for track in album:
#                 print(track)
#             for key in album:
#                 print(key)
#                 filePath = key[2]
#                 flatTracksList.append(filePath)
#     return flatTracksList
                
