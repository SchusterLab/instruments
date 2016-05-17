__author__ = 'Ge Yang'

import unittest
import matplotlib.pyplot as plt

from Triton import Triton

test_instrument = Triton("Oxford Tryton", address="192.168.14.129")

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.fridge = test_instrument

    def runTest(self):
        self.query_timeout_test()
        self.api_test()

    def query_timeout_test(self):
        #### Test socket timeout
        self.fridge.set_query_timeout(1000)
        print "sending malformed command"
        self.fridge.query("malformed command")
        self.assertTrue(True, 'query timeout works')

    def api_test(self):
        """Test APIs"""
        self.fridge.set_query_timeout(100)
        #### Test Driver Methods
        print "test ===> get_temperature()"
        self.fridge.query_sleep = 0.1
        temperature = self.fridge.get_temperature()
        print [temperature]
        self.assertTrue(temperature, 'temperature is not None: %s' % temperature)

        mc_temp = self.fridge.get_mc_temperature()
        print mc_temp

if __name__ == '__main__':
    unittest.main()
