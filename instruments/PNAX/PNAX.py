#
# ======================================================
#
# reference the programming manual here: http://na.support.keysight.com/pna/help/index.html?id=1000001808-1:epsg:man
# and specifically here: New Programming Commands:
# http://na.support.keysight.com/pna/help/latest/help.htm
#
# ======================================================
#
__author__ = 'Ge Yang'
from Instruments import SocketInstrument
import time
import numpy as np
import glob
import os.path


def polar2mLog(xs, ys):
    return np.sqrt(xs ** 2 + ys ** 2), np.arctan(ys / xs)


class N5242A(SocketInstrument):
    MAXSWEEPPTS = 1601
    default_port = 5025

    def __init__(self, name="E5071", address=None, enabled=True, **kwargs):
        SocketInstrument.__init__(self, name, address, enabled=enabled, recv_length=2 ** 20, **kwargs)
        self.query_sleep = 0.05

    def get_id(self):
        return self.query('*IDN?')

    def get_query_sleep(self):
        return self.query_sleep

    #### Frequency setup
    def set_start_frequency(self, freq, channel=1):
        self.write(":SENS%d:FREQ:START %f" % (channel, freq))

    def get_start_frequency(self, channel=1):
        return float(self.query(":SENS%d:FREQ:START?" % channel))

    def set_stop_frequency(self, freq, channel=1):
        self.write(":SENS%d:FREQ:STOP %f" % (channel, freq))

    def get_stop_frequency(self, channel=1):
        return float(self.query(":SENS%d:FREQ:STOP?" % channel))

    def set_center_frequency(self, freq, channel=1):
        self.write(":SENS%d:FREQ:CENTer %f" % (channel, freq))

    def get_center_frequency(self, channel=1):
        return float(self.query(":SENS%d:FREQ:CENTer?" % channel))

    def set_span(self, span, channel=1):
        return self.write(":SENS%d:FREQ:SPAN %f" % (channel, span))

    def get_span(self, channel=1):
        return float(self.query(":SENS%d:FREQ:SPAN?" % channel))

    def set_sweep_points(self, numpts=1600, channel=1):
        query = ":sense%d:sweep:points %d" % (channel, numpts)
        print query
        self.write(query)

    def get_sweep_points(self, channel=1):
        data = self.query(":sense%d:sweep:points?" % (channel))
        print 'sweep points query response', [data]
        return int(data)

    #### Averaging
    def set_averages(self, averages, channel=1):
        self.write(":SENS%d:AVERage:COUNt %d" % (channel, averages))

    def get_averages(self, channel=1):
        return int(self.query(":SENS%d:average:count?" % channel))

    def set_average_state(self, state=True, channel=1):
        if state:
            s = "ON"
        else:
            s = "OFF"
        self.write(":SENS%d:AVERage:state %s" % (channel, s))

    def get_average_state(self, channel=1):
        return bool(self.query(":SENS%d:average:state?" % channel))

    def clear_averages(self, channel=1):
        self.write(":SENS%d:average:clear" % channel)

    def set_ifbw(self, bw, channel=1):
        self.write("sens%d:bwid %f" % (channel, bw))

    def get_ifbw(self, channel=1):
        return float(self.query("SENS%d:bwid?" % (channel)))

    def operation_complete(self):
        # if self.query("*OPC?") == '+1\n': return True
        self.query("*OPC?")

    def trigger_single(self, channel=1):
        self.write('initiate%d:immediate' % channel)

    def set_trigger_average_mode(self, state=True):
        if state:
            self.write('sense:AVER ON')
        else:
            self.write('sense:AVER OFF')

    def get_trigger_average_mode(self):
        return bool(self.query('sense:AVER?'))

    def set_trigger_source(self, source="immediate"):  # IMMEDIATE, MANUAL, EXTERNAL
        allowed_sources = ['ext', 'imm', 'man', 'immediate', 'external', 'manual']
        if source.lower() not in allowed_sources:
            raise "source need to be one of " + allowed_sources
        self.write(':TRIG:SEQ:SOUR ' + source)

    def get_trigger_source(self):  # INTERNAL, MANUAL, EXTERNAL,BUS
        return self.query(':TRIG:SEQ:SOUR?').strip()

    #### Source

    def set_power(self, power, channel=1):
        # print ":SOURCE:POWER%d %f" % (channel, power)
        self.write(":SOURCE%d:POWER%d %f" % (channel, channel, power))

    def get_power(self, channel=1):
        return float(self.query(":SOURCE%d:POWER?" % channel))

    def set_output(self, state=True):
        if state or str(state).upper() == 'ON':
            self.write(":OUTPUT ON")
        elif state == False or str(state).upper() == 'OFF':
            self.write(":OUTPUT OFF")

    def get_output(self):
        return bool(self.query(":OUTPUT?"))

    def delete_trace(self, trace=None):
        if trace is None:
            query = "disp:wind:trac:del"
        else:
            query = "disp:wind:trac%d:del" % trace
        self.write(query)

    def delete_measurement(self, name=None):
        if name is None:
            # delete all traces
            self.write(r'calc:par:del:all')
        else:
            self.write("calc:par:del '%s'" % name)

    def define_measurement(self, name, channel, mode):
        query = "calc%d:par:def:ext '%s','%s'" % (channel, name, mode)
        print query
        self.write(query)

    def get_measurements(self):
        data = self.query('calc:par:cat?')
        if data == '"NO CATALOG"\n':
            return None
        else:
            data_list = data.strip().split(',')
            return zip(*[iter(data_list)] * 2)

    def select_measurement(self, name=None, channel=1):
        query = "calc%d:par:sel '%s'" % (channel, name)
        print query
        self.write(query)

    def display_measurement(self, name=None, trace=1):
        query = "disp:wind:trace%d:feed '%s'" % (trace, name)
        self.write(query)

    def auto_scale(self, trace=None):
        """
        Performs an Autoscale on the specified trace in the specified window, providing the best fit display.
        Autoscale is performed only when the command is sent; it does NOT keep the trace autoscaled indefinitely.
        """
        if trace is None:
            query = "DISP:WIND:TRAC:Y:AUTO"
        else:
            query = "disp:wind:trac%d:Y:AUTO" % trace
        self.write(query)

    def set_measure(self, mode='S21', channel=1):
        pass

    #### Trace Operations
    def set_active_trace(self, channel=1, trace=1, fast=False):
        """
        set the active trace, which is required by the
        following commands [get_format, set_format]

        The fast option is OPTIONAL. The PNA display is
        NOT updated. Therefore, do not use this argument when
        an operator is using the PNA display. Otherwise, sending
        this argument results in much faster sweep speeds. There
        is NO other reason to NOT send this argument.
        """
        query_string = "CALC%d:PAR:MNUM %d" % (channel, trace)
        if fast:
            query_string += ",fast"
        # print query_string
        self.write(query_string)

    def get_active_trace(self, channel=1):
        """set the active trace, need to run after the active trace is set."""
        query_string = "calculate%d:parameter:mnumber:select?" % channel
        data = self.query(query_string)
        if data is None:
            return data;
        else:
            return int(data)

    def set_format(self, trace_format='MLOG', trace=1):
        """set_format: need to run after the active trace is set.
        valid options are
        {MLOGarithmic|PHASe|GDELay| SLINear|SLOGarithmic|SCOMplex|SMITh|SADMittance|PLINear|PLOGarithmic|POLar|MLINear|SWR|REAL| IMAGinary|UPHase|PPHase}
        """
        self.write("CALC%d:FORM %s" % (trace, trace_format))

    def get_format(self, trace=1):
        """set_format: need to run after active trace is set.
        valid options are
        {MLOGarithmic|PHASe|GDELay| SLINear|SLOGarithmic|SCOMplex|SMITh|SADMittance|PLINear|PLOGarithmic|POLar|MLINear|SWR|REAL| IMAGinary|UPHase|PPHase}
        """
        data = self.query("CALC%d:FORM?" % (trace))
        if data is None:
            return data
        else:
            return data.strip()

    #### File Operations
    def save_file(self, fname):
        self.write('MMEMORY:STORE:FDATA \"' + fname + '\"')

    # def read_line(self, eof_char='\n', timeout=None):
    #     if timeout is None:
    #         timeout = self.query_timeout
    #     done = False
    #     while done is False:
    #         buffer_str = self.read(timeout)
    #         # print "buffer_str", buffer_str
    #         yield buffer_str
    #         if buffer_str[-1] == eof_char:
    #             done = True

    def read_data(self, channel=1, timeout=None):
        """Read current NWA Data, return fpts,mags,phases"""
        number_of_sweep_points = self.get_sweep_points()
        if timeout is None:
            timeout = self.query_timeout
        self.write("CALC%d:DATA? FDATA" % channel)
        time.sleep(self.query_sleep)
        data_str = ''.join(self.read_line(timeout=timeout))
        # print 'data_str ==>"', data_str, '"'
        data = np.fromstring(data_str, dtype=float, sep=',')
        fpts = np.linspace(self.get_start_frequency(), self.get_stop_frequency(), number_of_sweep_points)
        if len(data) == 2 * number_of_sweep_points:
            data = data.reshape((-1, 2))
            data = data.transpose()
            return np.vstack((fpts, data))
        else:
            return np.vstack((fpts, data))

    #### Meta

    def take_one(self):
        """Tell Network Analyzer to take a single averaged trace and grab data,
        either saving it to fname or returning it.  This function does not set up
        the format or anything else it just starts, blocks, and grabs the next trace."""

        old_trigger_source = self.get_trigger_source()
        self.set_trigger_source("manual")
        time.sleep(self.query_sleep) # test if this is crucial
        old_format = self.get_format()
        if old_format is not 'POL':
            self.set_format('polar')
            time.sleep(self.query_sleep) # test if this is crucial
        self.clear_averages(channel=1)
        self.trigger_single(channel=1)
        time.sleep(self.query_sleep) # test if this is crucial
        self.operation_complete()
        data = self.read_data()
        fpts, xs, ys = data
        self.set_trigger_source(old_trigger_source)
        self.set_format(old_format)
        return fpts, xs, ys

    def take_one_in_mag_phase(self):
        fpts, xs, ys = self.take_one()
        mags, phases = polar2mLog(xs, ys)
        return fpts, mags, phases

    def take_one_with_average(self, avg=None):
        if avg is None:
            return self.take_one()
        else:
            self.set_averages(avg)
            self.set_trigger_average_mode()
            return self.take_one()

    def segmented_sweep(self, start, stop, step, output_format='polar'):
        """Take a segmented sweep to achieve higher resolution"""
        max_sweep_points = 4000
        span = stop - start
        total_sweep_pts = span / step
        if total_sweep_pts <= max_sweep_points:
            print "Segmented sweep unnecessary"
        segments = np.ceil(total_sweep_pts / max_sweep_points)
        segspan = span / segments
        starts = start + segspan * np.arange(0, segments)
        stops = starts + segspan
        print "full span is %f GHz, in %d segments, with a span of %fMHz each" % (span / 1e9, segments, segspan / 1e6)

        time.sleep(self.query_sleep)

        # Set Save old settings and set up for automated data taking
        original_output_format = self.get_format()
        original_timeout = self.get_query_timeout()
        original_trigger_average_mode = self.get_trigger_average_mode()

        self.set_query_timeout(self.query_timeout)
        self.set_trigger_source('manual')
        self.set_active_trace(1)
        # only the polar and smith are outputing two number per data point
        self.set_format(trace_format=output_format)

        self.set_span(segspan)
        segs = []
        for start, stop in zip(starts, stops):
            print '.',
            self.set_start_frequency(start)
            self.set_stop_frequency(stop)

            self.clear_averages()
            self.trigger_single()
            time.sleep(self.query_sleep)
            self.operation_complete()  # Blocks!

            seg_data = self.read_data()

            seg_data = seg_data.transpose()
            last = seg_data[-1]
            seg_data = seg_data[:-1].transpose()
            segs.append(seg_data)
        segs.append(np.array([last]).transpose())
        time.sleep(self.query_sleep)

        self.set_format(trace_format=original_output_format)
        self.set_query_timeout(original_timeout)
        self.set_trigger_average_mode(original_trigger_average_mode)
        self.set_trigger_source('IMM')

        return np.hstack(segs)

    def segmented_sweep2(self, start, stop, step, sweep_pts=None, fname=None, save_segments=True):
        """Take a segmented sweep to achieve higher resolution"""
        span = stop - start
        total_sweep_pts = span / step
        if total_sweep_pts < 1600:
            print "Segmented sweep unnecessary"
            self.set_sweep_points(max(sweep_pts, total_sweep_pts))
            self.set_start_frequency(start)
            self.set_stop_frequency(stop)
            return self.take_one_averaged_trace(fname)
        segments = np.ceil(total_sweep_pts / 1600.)
        segspan = span / segments
        starts = start + segspan * np.arange(0, segments)
        stops = starts + segspan

        #        print span
        #        print segments
        #        print segspan

        # Set Save old settings and set up for automated data taking
        time.sleep(self.query_sleep)
        old_format = self.get_format()
        old_timeout = self.get_query_timeout()
        old_avg_mode = self.get_trigger_average_mode()

        self.set_query_timeout(self.query_timeout)
        self.set_trigger_average_mode(True)
        self.set_trigger_source('BUS')
        self.set_format('mlog')

        self.set_span(segspan)
        segs = []
        for start, stop in zip(starts, stops):
            self.set_start_frequency(start)
            self.set_stop_frequency(stop)

            self.clear_averages()
            self.trigger_single()
            time.sleep(self.query_sleep)
            self.operation_complete()  # Blocks!
            self.set_format('slog')
            seg_data = self.read_data()
            self.set_format('mlog')
            seg_data = seg_data.transpose()
            last = seg_data[-1]
            seg_data = seg_data[:-1].transpose()
            segs.append(seg_data)
            if (fname is not None) and save_segments:
                np.savetxt(fname, np.transpose(segs), delimiter=',')
        segs.append(np.array([last]).transpose())
        time.sleep(self.query_sleep)
        self.set_format(old_format)
        self.set_query_timeout(old_timeout)
        self.set_trigger_average_mode(old_avg_mode)
        self.set_trigger_source('INTERNAL')
        ans = np.hstack(segs)
        if fname is not None:
            np.savetxt(fname, np.transpose(ans), delimiter=',')
        return ans

    def get_settings(self):
        settings = {"start": self.get_start_frequency(), "stop": self.get_stop_frequency(),
                    "power": self.get_power(), "ifbw": self.get_ifbw(),
                    "sweep_points": self.get_sweep_points(),
                    "averaging": self.get_average_state(), "averages": self.get_averages()
                    }
        return settings

    def configure(self, start=None, stop=None, center=None, span=None, power=None, ifbw=None, sweep_pts=None, avgs=None,
                  defaults=False, remote=False):
        if defaults:       self.set_default_state()
        if remote:                          self.set_remote_state()
        if start is not None:            self.set_start_frequency(start)
        if stop is not None:            self.set_stop_frequency(stop)
        if center is not None:          self.set_center_frequency(center)
        if span is not None:            self.set_span(span)
        if power is not None:         self.set_power(power)
        if ifbw is not None:            self.set_ifbw(ifbw)
        if sweep_pts is not None:   self.set_sweep_points(sweep_pts)
        if avgs is not None:            self.set_averages(avgs)

    def set_remote_state(self):
        pass
        # self.set_trigger_source('BUS')
        # self.set_trigger_average_mode(True)
        # self.set_query_timeout(self.query_timeout)
        # self.set_format('slog')

    def set_default_state(self):
        # under construction
        pass
        # self.set_sweep_points()
        # self.set_format()
        # self.set_trigger_source()
        # self.set_trigger_average_mode(False)
        # self.write(":INIT1:CONT ON")


def condense_nwa_files(datapath, prefix):
    prefixes, data = load_nwa_dir(datapath)
    np.save(prefix, np.array(data))


def load_nwa_file(filename):
    """return three arrays: frequency magnitude and phase"""
    return np.transpose(np.loadtxt(filename, skiprows=3, delimiter=','))


def load_nwa_dir(datapath):
    fnames = glob.glob(os.path.join(datapath, "*.CSV"))
    fnames.sort()
    prefixes = [os.path.split(fname)[-1] for fname in fnames]
    data = [load_nwa_file(fname) for fname in fnames]
    return prefixes, data


def nwa_watch_temperature_sweep(na, fridge, datapath, fileprefix, windows, powers, ifbws, avgs, timeout=10000, delay=0):
    """nwa_watch_temperature_sweep monitors the temperature (via fridge) and tells the network analyzer (na) to watch certain windows
    at the specified powers, ifbws, and avgs specified
    windows= [(center1,span1),(center2,span2), ...]
    powers= [power1,power2,...]
    ifbws=[ifbw1,ifbw2,...]
    avgs=[avgs1,avgs2,...]"""
    f = open(datapath + fileprefix + ".cfg", 'w')
    f.write('datapath: %s\nfileprefix: %s\n\Window #\tCenter\tSpan\tPower\tIFBW\tavgs' % (datapath, fileprefix))
    for ii, w in enumerate(windows):
        f.write('%d\t%f\t%f\t%f\t%f\t%d' % (windows[ii][0], windows[ii][1], powers[ii], ifbws[ii], avgs[ii]))
    f.close()
    na.set_trigger_average_mode(True)
    na.set_sweep_points()
    na.set_average_state(True)
    na.set_query_timeout(timeout)
    na.set_format('slog')
    na.set_trigger_source('BUS')
    count = 0
    while (True):
        for ii, w in enumerate(windows):
            Temperature = fridge.get_temperature('MC RuO2')
            if not Temperature > 0:
                Temperature = fridge.get_temperature('MC cernox')
            print "Trace: %d\t\tWindow: %d\tTemperature: %3.3f" % (count, ii, Temperature)
            na.set_center_frequency(w[0])
            na.set_span(w[1])
            na.set_power(powers[ii])
            na.set_ifbw(ifbws[ii])
            na.set_averages(avgs)
            na.trigger_single()
            na.operation_complete()  # Blocks!
            na.save_file("%s%04d-%3d-%s-%3.3f.csv" % (datapath, count, ii, fileprefix, Temperature))
            time.sleep(delay)


def convert_nwa_files_to_hdf(nwa_file_dir, h5file, sweep_min, sweep_max, sweep_label="B Field", ext=".CSV"):
    import glob, h5py, csv
    hfile = h5py.File(h5file)
    files = glob.glob(nwa_file_dir + "*" + ext)
    n_files = len(files)
    for j, fn in enumerate(files):
        f = open(fn, 'r')
        # Skip Header
        for i in range(3):
            f.readline()
        rows = np.array((csv.reader(f)))
        if j is 0:
            n_points = len(rows)
            for t in ["mag", "phase"]:
                hfile[t] = np.zeros((n_points, n_files))
                hfile[t].attrs["_axes"] = ((rows[0][0], rows[-1][0]), (sweep_min, sweep_max))
                hfile[t].attrs["_axes_labels"] = ("Frequency", sweep_label, "S21")
        hfile["mag"][:, j] = rows[:, 1]
        hfile["phase"][:, j] = rows[:, 2]


if __name__ == '__main__':
    na = N5242A("N5242A", address="192.168.14.242")
    print na.get_id()
