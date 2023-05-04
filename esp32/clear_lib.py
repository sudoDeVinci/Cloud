import os
from subprocess import Popen, PIPE

try:
    process = Popen(f"ampy --port COM6 ls /lib", stdout = PIPE)
    files = process.stdout.read().decode('utf-8').strip()
except Exception as e:
        print(e)  

ls = list(files.split("\r\n"))
print(ls)

for file in ls:
    try:
        process = Popen(f"ampy --port COM6 rm {file}")
        print(f"ampy --port COM6 rm board/lib/{file}")
        process.wait()

    except Exception as e:
        print(e)