from pysense import pysense
from time import sleep_ms

py = pysense()
for i in range(10):
    temp = py.temperature()
    humidity = py.humidity()
    pressure = py.pressure()
    altitude = py.altitude()
    dew_point = py.dew_point()
    print("{0}|{1}|{2}|{3}|{4}".format(altitude, temp, humidity, pressure, dew_point))
    sleep_ms(1000)
