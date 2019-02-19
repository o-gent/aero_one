from datalink import Datalink
import time

def main():
    # fetches and processes data, returns array with payload only
    #link.send(message = [0,1,2,3,4,5,6,7,8,9])
    link.serial_handler()
    print(link.get(id_=1))
    print(link.get(id_=2))

    link.send(2, [800,0,0])

    print("LOOP!")
    
    # do stuff


if __name__ == "__main__":
    # start communication

    port = 1
    link = Datalink(port)
    
    while True:
        main()