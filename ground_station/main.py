import time

from display import Display
from datalink import Datalink

link = Datalink("dummy2")
disp = Display()
i = 0

while True:

    # datalink refresh
    start = time.time()
    link.refresh()
    end = time.time()

    disp.latency =  end - start
    
    i += 1
    if i >= 2:
        # refresh excel 
        disp.refresh(link.packets)
        i = 0
    
    #print(link.packets)



x = lambda v: v**2

for i in range(100):
    d.attitude(x(i), i)


