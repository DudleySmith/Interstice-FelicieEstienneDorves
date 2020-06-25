# CLASS Control
# A dictionnary to store all controls
#
# Each control is a Board Address + a channel number
#

# import circuit python
from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import time

import threading

# Bus
i2c = busio.I2C(SCL, SDA)
try:
    # All boards
    boards = {
    "0x40":PCA9685(i2c, address=0x40), # Board 0 : Servos
    "0x41":PCA9685(i2c, address=0x41), # Board 1 : Servos
    "0x42":PCA9685(i2c, address=0x42), # Board 2 : Servos
    "0x43":PCA9685(i2c, address=0x43), # Board 3 : Motors
    "0x44":PCA9685(i2c, address=0x44)  # Board 4 : Motors
    }
    
    # set all the same frequency
    for key, board in boards.items():
        board.frequency = 50
    
    # Resume board initialization
    for key, board in boards.items():
        print("board ", key, " : Address {0}".format(board))
    
except Exception as e:
    print("Something went wrong when initializing boards, are they all plugged ?")
    print("Try command : i2cdetect -y 1")
    print("You should see Address reserved from 40 to 44")
    print("{0}".format(e))
    
# For test and/pr check, print all informations
def printControls():
    print("\nI'm logging all servos settings (as dictionnary)")
    for key, controlVal in allControls.items():
        print(key, " : ", controlVal.toString())

def reset():
    
    for key, controlVal in allControls.items():
            
        # check if control exists
        if key in allControls:
            control = allControls.get(key)
            print("Control {0} exists", control.toString(), " set value", format(0))
            control.setValue(0);

    else:
        print("Control does not exist, check OSC Messages")
        
def setValue(addrControl, value):
    
    # check if control exists
    if addrControl in allControls:
        control = allControls.get(addrControl)
        print("Control {0} exists", control.toString(), " set value", format(value))
        control.setValue(value);

    else:
        print("Control does not exist, check OSC Messages")

def send(addrControl):
    
    # check if control exists
    if addrControl in allControls:
        control = allControls.get(addrControl)
        print("Control {0} exists, will send to board", control.toString())
        control.send();

    else:
        print("Control does not exist, check OSC Messages")

def send():

    for key, controlVal in allControls.items():
        #print(key, " : ", controlVal.toString())
        
        # check if control exists
        if key in allControls:
            control = allControls.get(key)
            control.send()
            #print("Control {0} exists, will send to board", control.toString())
#             mySendThread = threading.Thread(target=control.send())
#             mySendThread.start()
            

        else:
            print("Control does not exist, check OSC Messages")

    # Send to board

# -----------------------------------------------------------------------
# Unit class (Parent)
class I2CControl:
    # Constructor
    def __init__(self, cardAddr, channelNr):
        self.cardAddr   = cardAddr
        self.channelNr  = channelNr
        self.value      = 0.0
        self.realValue  = 0.1

    # to string
    def toString(self):
        pass

    def send(self):
        pass
    
    def setValue(self, value):
        self.value = value;

# -----------------------------------------------------------------------
# Servo class
# Value is an angle value and doesn't use the same lib as the motors
class Servo(I2CControl):
    def toString(self):
        return "Servo [" + format(hex(self.cardAddr)) + ":" + format(self.channelNr) + "]"

    def send(self):
        # Control as a Servo
        #print("Controlling servo [" + format(hex(self.cardAddr)) + ":" + format(self.channelNr) + "] with angle = " + str(value))
        
        if abs(self.realValue - self.value) < 0.1:
            self.realValue = self.value
            return
        
        myCardAddr = hex(self.cardAddr)
        if(boards.get(myCardAddr)):
            
            #print("Board found ++++++++++++++")
            #specific pulse range ---
            try:
                
                # Frequency
                boards[myCardAddr].frequency = 50
                
                # initiate servo variable
                theServo = servo.Servo(boards[myCardAddr].channels[self.channelNr], min_pulse=50, max_pulse=2500)

                stepValue = 5
                
                if self.realValue < self.value:
                    self.realValue += stepValue
                        
                elif self.realValue > self.value:
                    self.realValue -= stepValue
                
                if abs(self.realValue - self.value) < stepValue:
                    self.realValue = self.value
                
                # Finaly the good angle
                #print("values= {0}".format(self.realValue) ,",{0}".format(self.value), " Actual angle= {0}".format(theServo.angle))
                theServo.angle = self.realValue
                    

            except Exception as e:
                print(format(e))
            
            except:
                pass
                    
        else:
            print("No board matching --------")
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
# MOTOR class
# Value is a speed value and use another lib
class Motor(I2CControl):
    def toString(self):
        return "Motor [" + format(hex(self.cardAddr)) + ":" + format(self.channelNr) + "]"

    def send(self):
        
        if abs(self.realValue - self.value) < 0.1:
            self.realValue = self.value
            return
        
        
        myCardAddr = hex(self.cardAddr)
        if(boards.get(myCardAddr)):
            
            #specific pulse range ---
            try:
                # Frequency
                boards[myCardAddr].frequency = 1600
                
                # simple multiplication
                # Limite haute de courant
                floatValue = self.value
                boards[myCardAddr].channels[self.channelNr].duty_cycle = int(floatValue * float(0xFFFF))
                print("Controlling motor [" + format(hex(self.cardAddr)) + ":" + format(self.channelNr) + "] with speed = " + str(self.value))
        
                self.realValue = self.value
                
            
            except Exception as e:
                print(format(e))
            
            except:
                pass
        else:
            print("No boards matching")
# -----------------------------------------------------------------------


# # -------------------------------------------------------------------
# # Init all controls
allControls = {
    
# Motor (Board 4)
"M00":Motor(0x43, 0),
"M01":Motor(0x43, 2),
"M02":Motor(0x43, 3),
"M03":Motor(0x43, 4),
"M04":Motor(0x43, 5),
"M05":Motor(0x43, 6),
"M06":Motor(0x43, 7),
"M07":Motor(0x43, 8),
"M08":Motor(0x43, 9),
"M09":Motor(0x43, 10),
"M10":Motor(0x43, 11),
"M11":Motor(0x43, 12),
"M12":Motor(0x43, 13),
"M13":Motor(0x43, 14),
"M14":Motor(0x43, 15),

# Motor (Board 5)
"M15":Motor(0x44, 0),
"M16":Motor(0x44, 2),
"M17":Motor(0x44, 3),

# Servo (Board 1)
"B2":Servo(0x40, 0),
"C2":Servo(0x40, 1),
"F2":Servo(0x40, 2),
"G2":Servo(0x40, 3),
"B3":Servo(0x40, 4),
"C3":Servo(0x40, 5),
"D3":Servo(0x40, 6),
"E3":Servo(0x40, 7),
"F3":Servo(0x40, 8),
"G3":Servo(0x40, 9),
"A4":Servo(0x40, 10),
"B4":Servo(0x40, 11),
"C4":Servo(0x40, 12),
"D4":Servo(0x40, 13),
"E4":Servo(0x40, 14),
"F4":Servo(0x40, 15),

# Servo (Board 2)
"G4":Servo(0x41, 0),
"H4":Servo(0x41, 1),
"A5":Servo(0x41, 2),
"B5":Servo(0x41, 3),
"C5":Servo(0x41, 4),
"D5":Servo(0x41, 5),
"E5":Servo(0x41, 6),
"F5":Servo(0x41, 7),
"G5":Servo(0x41, 8),
"H5":Servo(0x41, 9),
"B6":Servo(0x41, 10),
"C6":Servo(0x41, 11),
"D6":Servo(0x41, 12),
"E6":Servo(0x41, 13),
"F6":Servo(0x41, 14),
"G6":Servo(0x41, 15),

# Servo (Board 3),
"B7":Servo(0x42, 0),
"C7":Servo(0x42, 1),
"D7":Servo(0x42, 2),
"E7":Servo(0x42, 3),
"F7":Servo(0x42, 4),
"G7":Servo(0x42, 5),
"D8":Servo(0x42, 6),
"E8":Servo(0x42, 7)

}
