"""
A script to update the lib folder of the pycom device
"""
import os
from time import sleep
from subprocess import Popen
files = os.listdir('pycom/lib')


# Try to upload library files
retries = {}
for file in files:
    try:
        print(f"> ampy --port COM11 put pycom/lib/{file} lib/{file}")
        process = Popen(f"ampy --port COM11 put pycom/lib/{file} lib/{file}")
        process.wait()
        sleep(2)
    except Exception as e:
        print(f"-- Couldn't upload {file}, will retry.")
        retries[file] = 0


# Attempt to upload library files until 
# ALl have been done, or we've tried to upload that files 3 times

# List of borked file uploads for one reason or another.
borked = []
while len(retries)!=0:
    for file in list(retries.keys()):
        try:
            print(f"> ampy --port COM11 put pycom/lib/{file} lib/{file}")
            process = Popen(f"ampy --port COM11 put pycom/lib/{file} lib/{file}")
            process.wait()
            sleep(2)
            del retries[file]
        except Exception as e:
            print(f"-- Couldn't upload {file}, will retry.")
            retries[file] += 1
            if retries[file] == 3:
                borked.append(retries[file])
                del retries[file]

if len(borked)!=0:
    print("\n The following files could not be uploaded for one reason or another:\n")
    for file in borked:
        print(f"> {file}")