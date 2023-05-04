from time import sleep_ms
import pycom
from pycoproc_2 import Pycoproc
import machine

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
    raise Exception('Not a Pysense')

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True


mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
li = LIS2HH12(py)

for i in range(100):
    print("Acceleration: " + str(li.acceleration()) + " | Roll: " + str(li.roll()) + " | Pitch: " + str(li.pitch()), end = '\r')
    sleep_ms(200)
    
# print("MPL3115A2 temperature: " + str(mp.temperature()))
# print("Altitude: " + str(mp.altitude()))
# mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
# print("Pressure: " + str(mpp.pressure()))
