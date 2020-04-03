# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# PCF8574
# This code is designed to work with the PCF8574_LBAR_I2CL I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products

import smbus
import time
import os
import subprocess

# Get I2C bus
bus = smbus.SMBus(0)

# PCF8574 address, 0x20(32) or 0x38 (56)
#		0xFF(255)	All pins configured as inputs
bus.write_byte(0x38, 0xFF)

# PCF8474 interupt declaration of the pine of orange pi pc
# PCF8574 INT wiring to physical pin 5 GPIO 6, PULL-UP resistance of 1khoms
os.system('echo "6" > /sys/class/gpio/export')
time.sleep(0.1)
os.system('echo "in" > /sys/class/gpio/gpio6/direction')
time.sleep(0.1)

# data acquisition variable
etat_pin = [0,0,0,0,0,0,0,0]

# infinite loop
while 1 :
    # Check the status of the interrupt
    interupt = int(subprocess.check_output(["cat","/sys/class/gpio/gpio6/value"]))
    # if change of state we read and store the state in the variable etat_pin
    if interupt == 0 :
        # PCF8574 address, 0x20(32) or 0x38 (56)
        # Read data back, 1 byte
        data = bus.read_byte(0x38)

        # Convert the data
        data = (data & 0xFF)

        for i in range(0, 8) :
            #print (data & (2 ** i))
            if (data & (2 ** i)) == 0 :
                etat_pin[i] = 0
            else :
                etat_pin[i] = 1
                time.sleep(0.01)
        # for debug        
        print (etat_pin)
    time.sleep(0.5)
