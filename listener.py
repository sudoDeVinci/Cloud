import csv
from multiprocessing.connection import Client
from socket import *
from client import Listener
from datetime import datetime
import os

# Create Initial socket

def listen(s, counter):

    while True:
        print("Listening")
        c,a = s.accept()
        with Listener(c) as l:
            # Print our connected device ip and set filename
            print('Connection from {0}'.format(str(a)))
            
            datestamp = str(datetime.now().strftime("%Y%m%d"))
            filename = f"img{counter}.png"
            # We use today's date as the folder for our readings
            folder = datestamp
            # We need to ccreate it if it doesnt exist
            if not os.path.exists("espimages/"+folder):
                os.mkdir("espimages/"+folder)

            print("Receiving Image..")

            # Attempt to get image data and write to image file
            try:
                data = l.get()
                if not data:
                    print("No Image received")
                else:
                    print("Received")
                    with open("espimages/"+folder+"/"+filename, "wb") as f:
                        f.write(data)
            except Exception as e:
                print(e)
                

            filename = f"readings{datestamp}{counter}.csv"
            headers = ["altitude", "temp", "humidity", "dew_point"]

            # Attempting to get sensor data and write to file
            try:
                print("Receiving sensor data..")
                data = l.get()
                if not data:
                    print("No Sensor data received")
                else:
                    print("Got Readings")
                    # Readings are encoded as csv with '|' delimiter
                    bytestring = data.decode('utf-8')
                    readings = bytestring.split("|")
                    print("Received", readings)
                    # Write to csv file
                    with open("espimages/"+folder+"/"+filename,  'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(headers)
                        writer.writerow(readings)
            except Exception as e:
                print(e, "err")
                if s:
                    s.close()
                raise e
            
        counter += 1
    
def find_count():
    pass


def main():
    counter = find_count()
    s = socket()
    try:
        # Try to let the socket address be reusable
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            # Try to bind the socket to an address and port
            s.bind(('',88))
            s.listen(100)
            # Listen, looping repeatedly
            listen(s, counter)
        except Exception as e:
            print(e, "err")
    except Exception as e:
        print(e)
        if s:
            s.close()

if __name__ == "__main__":
    main()