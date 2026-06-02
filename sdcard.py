from board import *
from time import *
import busio
import digitalio
import sdcardio
import storage
import os
 
sleep(1)
print("sys init") 
spi = busio.SPI(clock=GP10, MOSI=GP11, MISO=GP12)
cs = GP15
sd = sdcardio.SDCard(spi, cs)
print("file init:",sd)  
vfs = storage.VfsFat(sd)
print("mount:",vfs)
storage.mount(vfs, '/sd')
dirs = os.listdir('/sd')

# 输出所有文件和文件夹
for file in dirs:
   print (file)