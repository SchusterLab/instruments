__author__ = 'Ge Yang'

from unittest import TestCase, skip, main
import matplotlib.pyplot as plt
from time import sleep

from PNAX import N5242A

test_instrument = N5242A("N5242A", address="192.168.14.249")


class MyTestCase(TestCase):
    def setUp(self):
        self.na = test_instrument

    def  runTest(self):
        # self.read_data_test_MLOG()
        # self.take_one()
        self.take_one_in_mag_phase()

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

        # Important Note: you have to set an active trace before setting the format of a trace
        print "test ===> set_active_trace(1)"
        self.na.set_active_trace(1, 1, True)
        print "test ===> set_active_trace(1)"
        self.na.get_active_trace()
        # this is always going to give an error message regardless
        print "test ===> delete all traces"
        self.na.delete_trace()

        print "test ===> delete all measurement names"
        self.na.delete_measurement()

        print "test ===> define the measurement"
        self.na.define_measurement('S21', channel=1, mode='S21')
        print "test ===> display the measurement"
        self.na.display_measurement('S21')
        print "test ===> select measurement"
        self.na.select_measurement('S21')

        sleep(0.5)

        print "test ===> auto scale all of the traces"
        self.na.auto_scale()


        print "test ===> set_default_state()"
        self.na.set_default_state()
        print "test ===> set_power(1, -20)"
        self.na.set_power(-20, 1)
        print "test ===> set_sweep_points(3000)"
        self.na.set_sweep_points(3000)
        print "test ===> get_sweep_points()"
        self.na.get_sweep_points()
        print "test ===> set_ifbw(1e3)"
        self.na.set_ifbw(1e3)
        print "test ===> get_ifbw()"
        print self.na.get_ifbw()
        print "test ===> set_averages(1)"
        self.na.set_averages(1)

        print "test ===> get_electrical_delay()"
        delay = self.na.get_electrical_delay()
        self.assertTrue(delay is not None, "delay should be a number")

        print "test ===> set_electrical_delay(5E-9)"
        self.na.set_electrical_delay(5e-9)

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

        # print "test ===> set_measure('S21')"
        # self.na.set_measure('S21')

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
        self.na.set_sweep_points(3000)

        self.na.delete_trace()
        self.na.delete_measurement()

        self.na.define_measurement('S21', channel=1, mode='S21')
        self.na.display_measurement('S21')
        self.na.select_measurement('S21')
        sleep(0.5)
        # Important Note: you have to set an active trace before setting the format of a trace
        self.na.set_active_trace(1, 1, True)
        self.na.get_active_trace()
        self.na.auto_scale()

        fpts, xs, ys = self.na.take_one()

        plt.figure()
        plt.plot(fpts, xs)
        plt.plot(fpts, ys)
        plt.show()

    def take_one_in_mag_phase(self):
        self.na.set_query_timeout(10000)

        # this is always going to give an error message regardless
        self.na.delete_trace()
        self.na.delete_measurement()

        self.na.define_measurement('S21', channel=1, mode='S21')
        self.na.display_measurement('S21')
        self.na.select_measurement('S21')
        sleep(0.5)
        # Important Note: you have to set an active trace before setting the format of a trace
        self.na.set_active_trace(1, 1, True)
        self.na.get_active_trace()
        sleep(1)
        self.na.auto_scale()

        self.na.set_center_frequency(6.160574e9)
        self.na.set_span(10e6)
        self.na.set_power(-5, 1)
        self.na.set_ifbw(1e3)
        self.na.set_sweep_points(3000)
        sleep(0.1)
        sweep_points = self.na.get_sweep_points()
        self.assertTrue(sweep_points, "sweep points need to be a number")

        fpts, mags, phases = self.na.take_one_in_mag_phase()

        plt.figure()
        plt.plot(fpts, mags)
        plt.plot(fpts, phases)
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
        self.na.set_sweep_points(3000)
        self.na.set_averages(10)
        self.na.set_average_state(True)

        print self.na.get_settings()
        self.na.clear_averages()
        self.na.take_one_averaged_trace("test.csv")


if __name__ == '__main__':
    main()
