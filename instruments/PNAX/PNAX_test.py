__author__ = 'Ge Yang'

from unittest import TestCase, skip
import matplotlib.pyplot as plt

from PNAX import N5242A

test_instrument = N5242A("N5242A", address="192.168.14.249")


class MyTestCase(TestCase):
    def setUp(self):
        self.na = test_instrument

    def query_timeout_test(self):
        #### Test socket timeout
        self.na.set_query_timeout(1000)
        print "sending malformed command"
        self.na.query("malformed command")
        self.assertTrue(True, 'query timeout works')

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
        print "test ===> set_trigger_average_mode(True)"
        self.na.set_trigger_average_mode(True)
        print "test ===> set_trigger_average_mode(False)"
        self.na.set_trigger_average_mode(False)
        print "test ===> get_trigger_average_mode()"
        print self.na.get_trigger_average_mode()

        print "test ===> set_measure('S21')"
        self.na.set_measure('S21')

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

    def take_one_averaged(self):
        """should be able to clear average and take averaged trace"""
        self.na.set_default_state()
        self.na.set_center_frequency(6.160574e9)
        self.na.set_span(10e6)
        self.na.set_power(-5, 1)
        self.na.set_ifbw(1e3)

        self.na.set_query_timeout(40e3)
        set_format = self.na.set_format('polar')
        print "set_format returned: ", set_format
        self.na.set_trigger_source("manual")
        self.na.set_averages(10)
        self.na.set_trigger_average_mode()

        self.na.clear_averages(channel=1)
        self.na.trigger_single(channel=1)
        fpts, xs, ys = self.na.read_data()
        #
        plt.figure()
        plt.plot(fpts, xs)
        plt.plot(fpts, ys)
        plt.show()

    def take_one(self):
        self.na.set_center_frequency(6.160574e9)
        self.na.set_span(10e6)
        self.na.set_power(-5, 1)
        self.na.set_ifbw(1e3)

        fpts, xs, ys = self.na.take_one()

        plt.figure()
        plt.plot(fpts, xs)
        plt.plot(fpts, ys)
        plt.show()


    @skip('skip segment sweep, not really needed with PNA-X because of the large memory')
    def nwa_segment_sweep_test(self):
        """Test segmented Sweep"""
        self.na.set_default_state()
        self.na.set_power(-35, 1)
        self.na.set_ifbw(1e3)
        self.na.set_averages(1)

        self.na.get_start_frequency()
        self.na.get_stop_frequency()

        self.na.set_query_timeout(40e3)
        set_format = self.na.set_format('mlog')
        fpts, mags, phases = self.na.segmented_sweep(2.3e9, 2.5e9, 5e3, 'polar')

        plt.figure()
        plt.plot(fpts, mags)
        plt.plot(fpts, phases)
        plt.show()

    @skip('skip redundant test')
    def nwa_test3(self):
        pass
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
