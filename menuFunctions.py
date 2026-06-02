# functions for menu generation

import board
import displayio
import digitalio
import terminalio
import busio
from adafruit_display_text import label
import adafruit_displayio_sh1106
import i2cdisplaybus
import os
import json
import time
from rainbowio import colorwheel
import neopixel

nn=1
pixels = neopixel.NeoPixel(board.GP22, nn, brightness=0.1, auto_write=False)

# -------------------------
#  DISPLAY INITIALISATION
# -------------------------
# displayio.release_displays()
# 
# i2c = busio.I2C(board.GP3, board.GP2) 
# display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)  # Change if needed
# 
# # Create the SH1106 display object
# display = adafruit_displayio_sh1106.SH1106(
#     display_bus,
#     width=128,
#     height=64
# )

def displayTrackInfo(artist, album, track):
    # displays the track info on 3 lines
    # tbd: sideways scrolling assuming this doesn't tie up the CPU too badl
    
    # row 1, artist
    artistRow = label.Label(
    terminalio.FONT,
    text=artist,
    color=0xFFFFFF,
    x=1,
    y=10
    )
    # row2 , album
    albumRow = label.Label(
    terminalio.FONT,
    text=album,
    color=0xFFFFFF,
    x=3,
    y=25
    )
    # row 3, track
    trackRow = label.Label(
    terminalio.FONT,
    text=track,
    color=0xFFFFFF,
    x=5,
    y=40
    )
    
    splash = displayio.Group()
    splash.append(artistRow)
    splash.append(albumRow)
    splash.append(trackRow)
    display.root_group = splash

# # -------------------------
#  Just for fun
#  On the Seengood board, make the rgb cycle when playing
# -------------------------
async def rainbow_cycle(wait):
    for j in range(255):
        for i in range(nn):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        await asyncio.sleep(wait)

# *************************************************************#
# the buttons/track menu logic is WIP so commented out for now.
# at the moment, we'll just show the track that's playing.
# *************************************************************#

# # -------------------------
# #  DEFINE BUTTONS HERE
# #  NOTE: the pushbuttons I used don't work right when used as input, even with a resistor.
# #  They work perfectly in reverse, so using the "pressed" value as False
# # -------------------------
# menuUpPin = board.GP8
# menuUpButton = digitalio.DigitalInOut(menuUpPin)
# # menuUpButton.direction = digitalio.Direction.INPUT
# menuUpButton.pull = digitalio.Pull.UP
# 
# menuDownPin = board.GP7
# menuDownButton = digitalio.DigitalInOut(menuDownPin)
# # menuDownButton.direction = digitalio.Direction.INPUT
# menuDownButton.pull = digitalio.Pull.UP
# 
# menuEnterPin = board.GP9
# menuEnterButton = digitalio.DigitalInOut(menuEnterPin)
# # menuEnterButton.direction = digitalio.Direction.INPUT
# menuEnterButton.pull = digitalio.Pull.UP
# 
# menuExitPin = board.GP10
# menuExitButton = digitalio.DigitalInOut(menuExitPin)
# # menuExitButton.direction = digitalio.Direction.INPUT
# menuExitButton.pull = digitalio.Pull.UP
# 
# # -------------------------
# #  MENU DATA
# #  Pulling this in from a file on the board for the moment to test, but we'll pass the track dictionary going forward.
# # -------------------------
# # MENU = {
# #     "Test Menu 1": ["Test Submenu 1a", "Test Submenu 1b"],
# #     "Test Menu 2": ["Test Submenu 2a", "Test Submenu 2b"]
# # }
# 
# with open("tracks.json", "r") as f:
#     MENU = f.read()
#     f.close()
# 
# MENU = json.loads(MENU)
# 
# menu_stack = []          # Tracks where we are in the hierarchy
# current_items = list(MENU.keys())
# cursor = 0
# 
# # -------------------------
# #  RENDERING
# # -------------------------
# def render_menu():
#     splash = displayio.Group()
#     display.root_group = splash
# 
#     title = " / ".join(menu_stack) if menu_stack else "Main Menu"
# 
#     title_label = label.Label(
#         terminalio.FONT,
#         text=title,
#         color=0xFFFFFF,
#         x=5,
#         y=5
#     )
#     splash.append(title_label)
# 
#     y = 20
#     for i, item in enumerate(current_items):
#         prefix = "> " if i == cursor else "  "
#         item_label = label.Label(
#             terminalio.FONT,
#             text=prefix + item,
#             color=0xFFFFFF,
#             x=5,
#             y=y
#         )
#         splash.append(item_label)
#         y += 12
# 
#     display.refresh
# 
# # -------------------------
# #  NAVIGATION LOGIC
# # -------------------------
# 
# def move_up():
#     print("buttonUp")
#     global cursor
#     cursor = (cursor - 1) % len(current_items)
#     render_menu()
# 
# def move_down():
#     print("buttonDown")
#     global cursor
#     cursor = (cursor + 1) % len(current_items)
#     render_menu()
# 
# def enter_item():
#     print("buttonEnter")
#     global current_items, cursor
# 
#     selected = current_items[cursor]
# 
#     # Walk down the JSON tree according to menu_stack
#     node = MENU
#     for level in menu_stack:
#         node = node[level]
# 
#     # If selected item is a submenu (dict)
#     if isinstance(node[selected], dict):
#         print("going into", selected)
#         menu_stack.append(selected)
#         current_items = list(node[selected].keys())
#         cursor = 0
#         render_menu()
#         return
# 
#     # Otherwise it's a leaf → play MP3
#     leaf_json = node[selected]
#     print("Selected leaf:", selected)
#     print("Passing JSON to playMP3:", leaf_json)
#     playMP3(leaf_json)
# 
# 
# def go_up_level():
#     print("buttonExit")
#     global current_items, cursor
# 
#     if not menu_stack:
#         return  # Already at top level
# 
#     menu_stack.pop()
# 
#     # Recompute current_items based on new stack
#     node = MENU
#     for level in menu_stack:
#         node = node[level]
# 
#     current_items = list(node.keys())
#     cursor = 0
#     render_menu()
# 
# 
# 
# # -------------------------
# #  INITIAL DRAW
# # -------------------------
# render_menu()
# 
# # -------------------------
# #  MAIN LOOP (BUTTONS LATER)
# # -------------------------
# while True:
#     # Replace these with your real button checks
#     # Example:
#     if menuUpButton.value == False: move_up()
#     if menuDownButton.value == False: move_down()
#     if menuEnterButton.value == False: enter_item()
#     if menuExitButton.value == False: go_up_level()
#     pass
# 

