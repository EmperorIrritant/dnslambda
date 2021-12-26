import unittest
from unittest.mock import patch
import socket
import sys
#import os
from threading import Thread
import errno
import time

import dnslambda_client


class TestProxyClient(unittest.TestCase):

    def call_main(test_args):
        with patch.object(sys, 'argv', test_args):
            dnslambda_client.main()
#        cmd = "python3 " + " ".join(test_args)
#        os.system("(" + cmd + ") & sleep 5; kill $!")

    def call_main_thread(self, test_args):
        try:
            thread = Thread(target=TestProxyClient.call_main, args=[test_args])
            thread.daemon = True
            thread.start()
            return True
        except Exception as e:
            if e:
                return False

    def check_port_proto(self, port, proto):
        socket_type = proto
        sock = socket.socket(socket.AF_INET, socket_type)
        port_in_use = False
        try:
            sock.bind(("", port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                port_in_use = True
            else:
                print(e)
        finally:
            sock.close()
        return port_in_use

    def check_port(self, port):
        time.sleep(1)       # Waiting for the thread to start
        port = int(port)
        tcp_in_use = self.check_port_proto(port, socket.SOCK_STREAM)
        udp_in_use = self.check_port_proto(port, socket.SOCK_DGRAM)
        if tcp_in_use and udp_in_use:
            return True
        else:
            return False

    def test_main(self):
        test_args = ["dnslambda_client.py", "-p", "9999"]
        self.assertEqual(self.call_main_thread(test_args), self.check_port(test_args[-1]))

if __name__ == '__main__':
    unittest.main()
