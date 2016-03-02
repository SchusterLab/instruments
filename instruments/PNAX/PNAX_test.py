__author__ = 'Ge Yang'

import unittest
import matplotlib.pyplot as plt

from PNAX import N5242A

test_instrument = N5242A("N5242A", address="192.168.14.242")

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.na = test_instrument

    def runTest(self):
        # self.query_timeout_test()
        self.api_test()
        self.read_data_test_MLOG()
        self.read_data_test_Polar()
        self.nwa_segment_sweep_test()

    def query_timeout_test(self):
        #### Test socket timeout
        self.na.set_query_timeout(1000)
        print "sending malformed command"
        self.na.query("malformed command")
        # self.assertTrue(True, 'query timeout works')

    def api_test(self):
        """Test APIs"""
        self.na.set_query_timeout(10000)
        #### Test Driver Methods
        print "test ===> set_default_state()"
        self.na.set_default_state()
        print "test ===> set_power(1, -20)"
        self.na.set_power(-20, 1)
        print "test ===> set_ifbw(1e3)"
        self.na.set_ifbw(1e3)
        print "test ===> get_ifbw()"
        print self.na.get_ifbw()
        print "test ===> set_averages(1)"
        self.na.set_averages(1)

        # Important Note: you have to set an active trace before setting the format of a trace.
        print "test ===> set_active_trace(1)"
        self.na.set_active_trace(1, 1, True)
        print "test ===> set_active_trace(1)"
        self.na.get_active_trace()
        print "test ===> get_format(1)"
        self.na.get_format(1)

        print "test ===> set_trigger_source('Ext')"
        self.na.set_trigger_source('Ext')

    def read_data_test_MLOG(self):
        """Read NWA data and plot results"""
        self.na.set_query_timeout(10e3)
        self.na.set_format('mlog')
        fpts, mags = self.na.read_data()

        plt.figure()
        plt.plot(fpts, mags)
        plt.show()

    def read_data_test_Polar(self):
        """Read NWA data and plot results"""
        self.na.set_query_timeout(10e3)
        self.na.set_format('polar')
        fpts, mags, phases = self.na.read_data()

        plt.figure()
        plt.plot(fpts, mags)
        plt.plot(fpts, phases)
        plt.show()

    def nwa_segment_sweep_test(self):
        """Test segmented Sweep"""
        self.na.set_default_state()
        self.na.set_power(-35, 1)
        self.na.set_ifbw(1e3)
        self.na.set_averages(1)

        self.na.get_start_frequency()
        self.na.get_stop_frequency()

        fpts, mags, phases = self.na.segmented_sweep(2.45e9, 2.55e9, 50e3, 'polar')

        plt.figure()
        plt.plot(fpts, mags)
        plt.show()

    def nwa_test3(self):
        self.na.set_trigger_average_mode(False)
        self.na.set_power(-20)
        self.na.set_ifbw(1e3)
        self.na.set_sweep_points()
        self.na.set_averages(10)
        self.na.set_average_state(True)

        print self.na.get_settings()
        self.na.clear_averages()
        self.na.take_one_averaged_trace("test.csv")

if __name__ == '__main__':
    unittest.main()
