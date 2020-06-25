import logging
import sys
import threading

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.osc_server import AsyncIOOSCUDPServer

import asyncio
import I2CControl

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

    if(addrElements[-1] in {"servo","motor"}):
        # SERVO ========================================================
        #I2CControl.send(number, value)
        mySendThread = threading.Thread(target=I2CControl.send(number, value))
        mySendThread.start()

    else:
        # OTHER ========================================================
        print(f"Control unknown {address}: {args}")
        logging.info(f"Control unknown {address}: {args}")

# Default message catch
# ++++++++++++++++++++++++++++++++++++++++++++++++
def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
# ------------------------------------------------


# ================================================
dispatcher = Dispatcher()
dispatcher.map("/control/*", getControl)
dispatcher.set_default_handler(default_handler)

# Init controls
I2CControl.printControls()

# Init server ------------------------------------
try:
    ip = "192.168.0.101"
    port = 9000
    
#     server = BlockingOSCUDPServer((ip, port), dispatcher)
#
#     logging.info('Launch server OSC ' + ip + ":" + str(port))
#
#     print("Server started ++")
#     server.serve_forever()  # Blocks forever

    async def loop():
        """Example main loop that only runs for 10 iterations before finishing"""
#         for i in range(10):
#             print(f"Loop {i}")
#             await asyncio.sleep(1)
        
        while True:
            await asyncio.sleep(0)


    async def init_main():
        server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

        await loop()  # Enter main loop of program

        transport.close()  # Clean up serve endpoint

    asyncio.run(init_main())

except OSError as e:
    print("Wrong address ??? : {0}".format(e))

except:
    print("Error : {0}".format(e))

print("Server didn't start")
