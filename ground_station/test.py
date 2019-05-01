from threading import Thread
from time import sleep

from client import Client
from server import Server

import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_main(self):

        def test_client(self):
            conn = Client('127.0.0.1')
            self.assertEqual( conn.recieve(), "1_[1, 2, ]")

        def test_server(self):
            conn = Server()
            conn.send(1, [1,2,3])
        
        thread1 = Thread(target = test_client)
        thread2 = Thread(target = test_server)

        thread1.start()
        thread2.start()


def test_main():
        def client():
            conn = Client('127.0.0.1')
            conn.recieve()
            conn.recieve()
            conn.recieve()
            conn.recieve()
            print(conn.data)

        def server():
            conn = Server()
            conn.send(1, [1,2,3])
            conn.send(2, [1,2,3])
            conn.send(1, [2,3,4])
            conn.send(4, [123123,123123,21312,31])
        
        thread1 = Thread(target = client)
        thread2 = Thread(target = server)

        thread1.start()
        thread2.start()

if __name__ == '__main__':
    #unittest.main()

    test_main()