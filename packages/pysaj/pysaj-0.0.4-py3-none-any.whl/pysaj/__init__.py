"""PySAJ interacts as a library to communicate with SAJ inverters"""
import logging
import xml.etree.ElementTree as ET
import urllib.request

_LOGGER = logging.getLogger(__name__)


class Sensor(object):
    """Sensor definition"""

    def __init__(self, key, name, unit):
        self.key = key
        self.name = name
        self.unit = unit
        self.value = None


class Sensors(object):
    """SAJ sensors"""

    def __init__(self):
        self.__s = []
        self.add(
            (
                Sensor("p-ac", "current_power", "W"),
                Sensor("e-today", "today_yield", "kWh"),
                Sensor("e-total", "total_yield", "kWh"),
                Sensor("maxPower", "today_max_current", "W"),
                Sensor("t-today", "today_time", "h"),
                Sensor("t-total", "total_time", "h"),
                Sensor("CO2", "total_co2_reduced", "kg"),
                Sensor("temp", "temperature", "°C"),
                Sensor("state", "state", "")
            )
        )

    def __len__(self):
        """Length."""
        return len(self.__s)

    def __contains__(self, key):
        """Get a sensor using either the name or key."""
        try:
            if self[key]:
                return True
        except KeyError:
            return False

    def __getitem__(self, key):
        """Get a sensor using either the name or key."""
        for sen in self.__s:
            if sen.name == key or sen.key == key:
                return sen
        raise KeyError(key)

    def __iter__(self):
        """Iterator."""
        return self.__s.__iter__()

    def add(self, sensor):
        """Add a sensor, warning if it exists."""
        if isinstance(sensor, (list, tuple)):
            for sss in sensor:
                self.add(sss)
            return

        if not isinstance(sensor, Sensor):
            raise TypeError("pysaj.Sensor expected")

        if sensor.name in self:
            old = self[sensor.name]
            self.__s.remove(old)
            _LOGGER.warning("Replacing sensor %s with %s", old, sensor)

        if sensor.key in self:
            _LOGGER.warning("Duplicate SMA sensor key %s", sensor.key)

        self.__s.append(sensor)


class SAJ(object):
    """Provides access to SAJ inverter data"""

    class ConnectionError(Exception):
        """Exception for connections"""
        def __init__(self):
            Exception.__init__(self,
                               "Connection to SAJ inverter not possible. " +
                               "Please check hostname/ip address.")

    def __init__(self, host):
        self.host = host

    async def read(self, sensors):
        """Returns necessary sensors from SAJ inverter"""

        try:
            self.xml = ET.ElementTree(file=urllib.request.urlopen(
                                 "http://%s/real_time_data.xml" % self.host))
            root = self.xml.getroot()

            for sen in sensors:
                sen.value = root.find(sen.key).text

            return True
        except urllib.error.URLError:
            _LOGGER.error("Connection to SAJ inverter not possible. " +
                          "Please check hostname/ip address.")
            return False
