from network import WLAN
from time import sleep
from gc import collect


# Connect to wifi networks, either open or secured.

def connect(SSID, PASSWORD, wlan):
    if PASSWORD is None:
        wlan.connect(ssid=SSID)
    else:
        wlan.connect(SSID, auth=(WLAN.WPA2, PASSWORD))
    print('connecting..',end='')
    while not wlan.isconnected():
        sleep(1)
        print('.',end='')
    print('Connected on:', wlan.ifconfig()[0])
    return wlan.ifconfig()[3]

# Get valid temp readouts from pysense modules
def readings():
    from pysense import pysense
    py = pysense()

    temp = py.temperature()
    humidity = py.humidity()
    altitude = py.altitude()
    dew_point = py.dew_point()
    
    readings = "{0}|{1}|{2}|{3}".format(altitude, temp, humidity, dew_point)
    # Encode as utf 8 readable bytes to send via socket
    return bytes(readings.encode('utf-8'))

# Receive image from esp32 cam.
def get_image():
    # Esp32 credentials
    SSID = "ImageServer"
    PASSWORD = None
    wlan = WLAN(mode=WLAN.STA)
    
    ip = connect(SSID,PASSWORD,wlan)
    sleep(1)
    print("Requesting..")
    from client import Listener
    try:
        # Self-closing client class
        # to handle socket tranmission
        with Listener(ip, 88) as c:
            print("Receiving..")
            data = c.get()
            if not data:
                print("No Image received")
                
        # Honestly don't know how much this
        # helps but this entire process is
        # very memory intensive so it all counts
        wlan.disconnect()
        del wlan, SSID, PASSWORD, c, ip
        print("Received.")
        collect()
        return data

    except Exception as e:
        if wlan:
            wlan.disconnect()
            sleep(1)
            del wlan
        print(e)
        return None
    
# Send image to listener server.
def send_image(data):
    # Home network credentials
    SSID = "********"         
    PASSWORD = "********"
    wlan = WLAN(mode=WLAN.STA)
    
    connect(SSID,PASSWORD,wlan)
    
    from socket import socket
    import struct
    sleep(1)
    
    # Address hard-coded because I'm not saure how to otherwise
    # Configure it. In my original setting, the server would have simply
    # Sent it's details, with the fipy receiving via LTE.
    addr = "********"
    port = 88
    s = socket()
    
    try:
        s.connect((addr,port))
        sleep(1)
        
        # Sending image data
        length = len(data)
        print("Sending image data ...")
        s.send(struct.pack('<I',length))
        s.sendall(data)
        print("Sent")
        sleep(2)
        
        # Send readings for corresponding image
        r = readings()
        length = len(r)
        print("Sending readings data...")
        s.send(struct.pack('<I',length))
        s.sendall(r)
        sleep(2)
        s.close()
        print("Sent")
        wlan.disconnect()
        del wlan, length, r, s
        collect()
        
    except Exception as e:
        if wlan:
            wlan.disconnect()
            del wlan
        if s:
            s.close()
        print(e)
        return None


def cycle():
    data = get_image()
    collect()
    if data != None:
        print("Image received in full.")
        print("")
        send_image(data)
    else:
        print("No Data Received, check esp Camera")
        print("")
        

