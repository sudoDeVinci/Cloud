from gc import collect
from time import sleep

def server_start():
    SSID = "ImageServer"
    PASSWORD = "12345678"
    from network import WLAN, AP_IF
    
    wlan = WLAN(AP_IF)
    wlan.active(True)
    wlan.config(essid = SSID, password = PASSWORD)
    
    conf = wlan.ifconfig()
    print('Connected, IP address:', conf)
    return wlan

# Initializing the Camera
def camera_init():
    import camera
    # Disable camera initialization
    camera.deinit()
    # Enable camera initialization
    camera.init(0, d0=4, d1=5, d2=18, d3=19, d4=36, d5=39, d6=34, d7=35,
                format=camera.JPEG, framesize=camera.FRAME_VGA,
                xclk_freq=camera.XCLK_20MHz,
                href=23, vsync=25, reset=-1, pwdn=-1,
                sioc=27, siod=26, xclk=21, pclk=22, fb_location=camera.PSRAM)

    camera.framesize(camera.FRAME_VGA) # Set the camera resolution
    # The options are the following:
    # FRAME_96X96 FRAME_QQVGA FRAME_QCIF FRAME_HQVGA FRAME_240X240
    # FRAME_QVGA FRAME_CIF FRAME_HVGA FRAME_VGA FRAME_SVGA
    # FRAME_XGA FRAME_HD FRAME_SXGA FRAME_UXGA
    # Note: The higher the resolution, the more memory is used.
    # Note: And too much memory may cause the program to fail.

    camera.flip(1)                       # Flip up and down window: 0-1
    camera.mirror(0)                     # Flip window left and right: 0-1
    camera.saturation(0)                 # saturation: -2,2 (default 0). -2 grayscale
    camera.brightness(0)                 # brightness: -2,2 (default 0). 2 brightness
    camera.contrast(0)                   # contrast: -2,2 (default 0). 2 highcontrast
    camera.quality(10)                   # quality: # 10-63 lower number means higher quality
    # Note: The smaller the number, the sharper the image. The larger the number, the more blurry the image

    camera.speffect(camera.EFFECT_NONE)  # special effects:
    # EFFECT_NONE (default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO
    camera.whitebalance(camera.WB_NONE)  # white balance
    # WB_NONE (default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

def send(s):
    from struct import pack
    from camera import deinit, capture
    
    while True: 
        camera_init()
        c,a = s.accept()
        print('Connection from {0}'.format(a))
        
        # I capture multiple frames to skip them 
        buf = capture()
        buf = capture()
        buf = capture()
        
        # Originally I had planned to send two 
        # images, finding the velocity vector of
        # the clouds finding their change between frames
        
        length = len(buf)
        data = bytes(buf)
        print("Sending Image data..")
        
        c.send(pack('<I',length)) # send 4-byte length
        c.sendall(data) # send actual message
        
        print("Image sent.")
        sleep(2)
        del c,a, buf, length
        deinit()
        collect()


def serve():
    wlan = server_start()
    from socket import SOL_SOCKET, SO_REUSEADDR, socket
    s = socket()

    try:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            s.bind(('',88))
            s.listen(100)
            send(s)
            # sleep for 1 minute after sending
            sleep(60000)
        except Exception as e:
            print(e, "err")
            if s:
                s.close()
            raise OSError
    except Exception as e:
        print(e)
        if s:
            s.close()
        if wlan:
            wlan.disconnect()
