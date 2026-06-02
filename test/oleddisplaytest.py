import board
import busio
import displayio
import terminalio
import i2cdisplaybus
from adafruit_display_text import label
import adafruit_displayio_sh1106

# Always release any previous displays
displayio.release_displays()

# Create the I2C interface
i2c = busio.I2C(board.GP3, board.GP2)  # Uses board.SCL and board.SDA
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)  # Change if needed

# Create the SH1106 display object
display = adafruit_displayio_sh1106.SH1106(
    display_bus,
    width=128,
    height=64
)

# Create a display group
# myGroup = displayio.Group()
# sdisplay.root_group(splash)

def displayTrackInfo(artist, album, track):
    # displays the track info on 3 lines
    # tbd: sideways scrolling assuming this doesn't tie up the CPU too badly
    global display
    
    # row 1, artist
    artistRow = label.Label(
    terminalio.FONT,
    text=artist,
    color=0xFFFFFF,
    x=5,
    y=5
    )
    # row2 , album
    albumRow = label.Label(
    terminalio.FONT,
    text=album,
    color=0xFFFFFF,
    x=5,
    y=25
    )
    # row 3, track
    trackRow = label.Label(
    terminalio.FONT,
    text=track,
    color=0xFFFFFF,
    x=5,
    y=45
    )
    
    splash = displayio.Group()
    splash.append(artistRow)
    splash.append(albumRow)
    splash.append(trackRow)
    display.root_group = splash

# Create a text label
# thisText = label.Label(
#     terminalio.FONT,
#     text="Hello SH1106!",
#     color=0xFFFFFF,
#     x=10,
#     y=10
# )
# 
# # myGroup.append(thisText)
# display.root_group = thisText

displayTrackInfo("Artist", "album", "track")
