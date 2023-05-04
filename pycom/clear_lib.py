"""
A script to clear the lib folder of the pycom module
"""
from subprocess import Popen, PIPE

try:
    process = Popen(f"ampy --port COM11 ls /flash/lib", stdout = PIPE)
    files = process.stdout.read().decode('utf-8').strip()
except Exception as e:
        print(e)  

ls = list(files.split("\r\n"))
print(ls)

for file in ls:
    try:
        process = Popen(f"ampy --port COM11 rm {file}")
        print(f"ampy --port COM6 rm {file}")
        process.wait()

    except Exception as e:
        print(e)