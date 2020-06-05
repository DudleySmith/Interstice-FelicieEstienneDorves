import logging
import sys

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

#setup Logging
logging.basicConfig(
filename='ReceiveOSCSendI2C.log',
format='%(asctime)s - %(levelname)s : %(message)s',
datefmt='%m/%d/%Y %I:%M:%S %p',
level=logging.DEBUG)

logging.info('Start OSC -> I2C : ')
logging.info('===========================================\n')


# Control the motors
# Arguments attendus
# 1 : String : Numéro du moteur
# 2 : Value : Valeur de vitesse
# ++++++++++++++++++++++++++++++++++++++++++++++++
def getControl(address, *args):
    # Vérification des paramètres
    if not len(args) == 2 or type(args[1]) is not float:
        return

    number = args[0]
    value = args[1]

    addrElements = address.split("/")
    #print(addrElements)

    if(addrElements[-1])=="servo":
        # SERVO ========================================================
        servoControl(number, value)

    elif(addrElements[-1])=="motor":
        # MOTOR ========================================================
        motorControl(number, value)

    else:
        # OTHER ========================================================
        print(f"Control unknown {address}: {args}")
        logging.info(f"Control unknown {address}: {args}")

# ------------------------------------------------

# Control the motors
# Arguments attendus
# 1 : String : Numéro du moteur
# 2 : Value : Valeur de vitesse
# ++++++++++++++++++++++++++++++++++++++++++++++++
def motorControl(number, value):

    # Print and wait for the real stuff
    print("Controlling motor [" + number + "] with speed = " + str(value))
# ------------------------------------------------


# Control the servos
# Arguments attendus
# 1 : String : Numéro du servo
# 2 : Value : Valeur d'angle
# ++++++++++++++++++++++++++++++++++++++++++++++++
def servoControl(number, value):

    # Print and wait for the real stuff
    print("Controlling servo [" + number + "] with angle = " + str(value))

# ------------------------------------------------

# Default message catch
# ++++++++++++++++++++++++++++++++++++++++++++++++
def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
# ------------------------------------------------


# ================================================
dispatcher = Dispatcher()
dispatcher.map("/control/*", getControl)
dispatcher.set_default_handler(default_handler)

ip = "192.168.0.101"
port = 9000

server = BlockingOSCUDPServer((ip, port), dispatcher)

logging.info('Launch server OSC ' + ip + ":" + str(port))
server.serve_forever()  # Blocks forever
