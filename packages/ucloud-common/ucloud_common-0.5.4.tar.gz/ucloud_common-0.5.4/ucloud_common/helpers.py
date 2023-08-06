import socket
import logging

from etcd3_wrapper import EtcdEntry


class SpecificEtcdEntryBase:
    def __init__(self, e: EtcdEntry):
        self.key = e.key

        for k in e.value.keys():
            self.__setattr__(k, e.value[k])

    def original_keys(self):
        r = dict(self.__dict__)
        del r["key"]
        return r

    @property
    def value(self):
        return self.original_keys()

    def __repr__(self):
        return str(dict(self.__dict__))



# TODO: Should be removed as soon as migration
#       mechanism is finalized inside ucloud
def get_ipv4_address():
    # If host is connected to internet
    #   Return IPv4 address of machine
    # Otherwise, return 127.0.0.1
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("8.8.8.8", 80))
        except socket.timeout:
            address = "127.0.0.1"
        except Exception as e:
            logging.getLogger().exception(e)
            address = "127.0.0.1"
        else:
            address = s.getsockname()[0]

    return address
