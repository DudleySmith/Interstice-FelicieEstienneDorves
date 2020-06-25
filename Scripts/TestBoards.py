# This example moves a servo its full range (180 degrees by default) and then back.

import time

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# This example also relies on the Adafruit motor library available here:
# https://github.com/adafruit/Adafruit_CircuitPython_Motor
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
# Board 0 ------------------------------
pca0 = PCA9685(i2c)
pca0.frequency = 330
#specific pulse range ---
servo0_7 = servo.Servo(pca0.channels[0], min_pulse=50, max_pulse=2500)

for i in range(60):
    servo0_7.angle = i
    time.sleep(0.01)

time.sleep(1)
for i in range(60,120):
    servo0_7.angle = i
    time.sleep(0.01)

time.sleep(1)
for i in range(120,180):
    servo0_7.angle = i
    time.sleep(0.01)

time.sleep(1)
for i in range(180):
    servo0_7.angle = 180 - i
    time.sleep(0.01)
    
servo0_7.angle = 0

pca0.deinit()

# Board 1 : Address 0x41 ------------------------------
pca1 = PCA9685(i2c, address=0x41)
pca1.frequency = 50
#specific pulse range ---
servo1_7 = servo.Servo(pca1.channels[0], min_pulse=50, max_pulse=2500)

for i in range(180):
    servo1_7.angle = i
for i in range(180):
    servo1_7.angle = 180 - i
    
servo1_7.angle = 0

pca1.deinit()

# Board 1 : Address 0x41 ------------------------------
pca2 = PCA9685(i2c, address=0x42)
pca2.frequency = 50
#specific pulse range ---
servo2_7 = servo.Servo(pca2.channels[0], min_pulse=50, max_pulse=2500)

for i in range(180):
    servo2_7.angle = i
for i in range(180):
    servo2_7.angle = 180 - i
    
servo2_7.angle = 0

pca2.deinit()



