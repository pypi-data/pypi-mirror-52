import smbus2
from collections import namedtuple
import time
from .crc import CRC8

class _cmds():
    """container class for mapping between human readable names and the command values used by the sgp"""
    SGP30Cmd = namedtuple("SGP30Cmd", ["commands", "replylen", "waittime"])
    IAQ_INIT = SGP30Cmd([0x20, 0x03], 0, 10)
    IAQ_MEASURE = SGP30Cmd([0x20, 0x08], 6, 12)
    GET_BASELINE = SGP30Cmd([0x20, 0x15], 6, 120)
    SET_BASELINE = SGP30Cmd([0x20, 0x1e], 0, 10)
    SET_HUMIDITY = SGP30Cmd([0x20, 0x61], 0, 10)
    IAQ_SELFTEST = SGP30Cmd([0x20, 0x32], 3, 520)
    GET_FEATURES = SGP30Cmd([0x20, 0x2f], 3, 3)
    GET_SERIAL = SGP30Cmd([0x36, 0x82], 9, 10)

    @classmethod
    def new_set_baseline(cls, baseline_data):
        cmd = cls.SET_BASELINE
        return cls.SGP30Cmd(cmd.commands + baseline_data, cmd.replylen, cmd.waittime)


class SGP30():

    def __init__(self, bus, address=0x58, baseline=[]):
        self.bus = bus
        self.address = address
        self.baseline = baseline

    SGP30Packet = namedtuple("SGP30Packet", ["data", "raw", "crc_ok"])

    def _raw_validate_crc(s, r):
        a = list(zip(r[0::3], r[1::3]))
        crc = r[2::3] == [CRC8().hash(i) for i in a]
        return(crc, a)

    def read_write(self, cmd):
        write = smbus2.i2c_msg.write(self.address, cmd.commands)
        if cmd.replylen <= 0:
            self.bus.i2c_rdwr(write)
        else:
            read = smbus2.i2c_msg.read(self.address, cmd.replylen)
            self.bus.i2c_rdwr(write)
            time.sleep(cmd.waittime/1000.0)
            self.bus.i2c_rdwr(read)
            r = list(read)
            crc_ok, a = self._raw_validate_crc(r)
            answer = [i << 8 | j for i, j in a]
            return self.SGP30Packet(answer, r, crc_ok)

    def dump_baseline(self):
        baseline = self.read_write(_cmds.GET_BASELINE)
        if baseline.crc_ok == True:
            print(baseline)
        else:
            print("Ignoring baseline due to invalid CRC")

    def set_baseline(self):
        crc, _ = self._raw_validate_crc(self.baseline)
        if len(self.baseline) == 6 and crc == True:
            self.read_write(_cmds.new_set_baseline(self.baseline))
            return True
        else:
            #print("Failed to load baseline, invalid data")
            return False

    def read_measurements(self):
        return self.read_write(_cmds.IAQ_MEASURE)

    def read_selftest(self):
        return self.read_write(_cmds.IAQ_SELFTEST)

    def read_serial(self):
        return self.read_write(_cmds.GET_SERIAL)

    def read_features(self):
        return self.read_write(_cmds.GET_FEATURES)

    def init_sgp(self):
        self.read_write(_cmds.IAQ_INIT)

    def i2c_general_call(self):
        """This attempts to reset _ALL_ devices on the i2c buss

        This command issues the i2c-general call RW command that should result
        in all devices aborting any read/write operations and starting to listen
        for new i2c-commands.

        This will usually un-stick the SGP30, but might reset or otherwise
        affect any device on the bus.
        """
        self.bus.write_byte(0, 0x06)
        time.sleep(0.1)
