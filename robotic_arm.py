import usb.core
import usb.util
import sys
import time

# locate the device device
      
dev = usb.core.find(idVendor=0x1267)

# assigns the device to the handle "dev"
# can check the device is visible to Linux with command line command lsusb
# which should report a device with the above vendor and id codes.

# was it found?

if dev is None:
    raise ValueError('Device not found')           # if device not found report an       error


# set the active configuration

dev.set_configuration()

# as no arguments, the first configuration will be the active one
# note as commands are sent to device as commands not data streams 
# no need to define the endpoint


light_on = 0b001
light_off = 0b000
grip_open = 0b010
grip_close = 0b001
wrist_down = 0b1000
wrist_up = 0b0100
elbow_up = 0b010000
elbow_down = 0b100000
shoulder_up = 0b01000000
shoulder_down = 0b01000000

# defines the command packet to send

datapack= grip_open | wrist_up | shoulder_down, 0, 0

# change this packet to make different moves.  
# first byte defines most of the movements, second byte shoulder rotation, third           byte light
# command structure in more detail:
# http://notbrainsurgery.livejournal.com/38622.html?view=93150#t93150

print "requested move",datapack    # reports the requested movement to the user

# send the command

bytesout=dev.ctrl_transfer(0x40, 6, 0x100, 0, datapack, 1000)

# outputs the command to the USB device, using the ctrl_transfer method
# 0x40, 6, 0x100, 0 defines the details of the write - bRequestType, bRequest,    wValue, wIndex
# datapack is our command (3 bytes)
# the final value is a timeout (in ms) which is optional
# bytesout = the number of bytes written (i.e. 3 if successful)

print "Written :",bytesout,"bytes"  # confirm to user that data was sent OK

# wait for a defined period

time.sleep(0.25)    # waits for 0.25 second whilst motors move.

# now STOP the motors

print light_on, light_off, light_off & light_on & grip_open

datapack = 0,0,0

bytesout=dev.ctrl_transfer(0x40, 6, 0x100, 0, datapack, 1000)

if bytesout == 3:
    print "Motors stopped"


