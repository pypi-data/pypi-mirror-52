import re


class Modalias(object):
    """
    Modalias strings might be a useful way for us to identify hardware.

    http://people.skolelinux.org/pere/blog/Modalias_strings___a_practical_way_to_map__stuff__to_hardware.html
    """
    COMPONENTS = re.compile(r"([a-z]+)([0-9A-F]+)")
    NAMES = {
        "v": "vendor",
        "p": "product",
        "d": "device",
        "sv": "subvendor",
        "sd": "subdevice",
        "bc": "bus_class",
        "sc": "bus_subclass",
        "i": "interface",
        "ic": "interface_class"
    }

    def __init__(self, data):
        self.modalias = data
        self.subtype, contents = data.split(":")

        self.vendor = None
        self.product = None
        self.device = None
        self.subvendor = None
        self.subdevice = None
        self.bus_class = None
        self.bus_subclass = None
        self.interface = None
        self.interface_class = None

        for label, value in Modalias.COMPONENTS.findall(contents):
            if label in Modalias.NAMES:
                setattr(self, Modalias.NAMES[label], value)

    def __repr__(self):
        return self.modalias

    def __str__(self):
        return self.modalias
