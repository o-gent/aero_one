from datalink import Datalink
import time 

d = Datalink("dummy1")
i = 1
b = 2

while True:
    i += 1
    if i > 100:
        i = 0
    b += 2

    d.put(2, [i, i-10,i-20,i -30])
    d.put(3, [b, i])
    d.put(5, [0,0,0,0,0,0,0])
    d.refresh()
