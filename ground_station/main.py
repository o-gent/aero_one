import time

from display import Display
from datalink import datalink_setup

#link = Datalink("client")

disp = Display()
i = 0

with datalink_setup("client") as link:
    while True:

        # datalink refresh
        link.put(1,[0,69])
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

