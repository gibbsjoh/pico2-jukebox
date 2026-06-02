# button testing
import board
import digitalio
import time

menuUpPin = board.GP8
menuUpButton = digitalio.DigitalInOut(menuUpPin)
#menuUpButton.direction = digitalio.Direction.OUTPUT
menuUpButton.pull = digitalio.Pull.UP

menuDownPin = board.GP7
menuDownButton = digitalio.DigitalInOut(menuDownPin)
#menuDownButton.direction = digitalio.Direction.OUTPUT
menuDownButton.pull = digitalio.Pull.UP
# 
# while True:
#     if menuUpButton.value == True:
#         print("Menu Up button")
#     if menuDownButton.value == True:
#         print("Menu Up button")
#     time.sleep(0.2)