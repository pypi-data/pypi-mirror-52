from contextlib import contextmanager
from datetime import datetime
from .helpers import SpecificEtcdEntryBase
from os.path import join


class VMStatus:
    # Must be only assigned to brand new VM
    requested_new = "REQUESTED_NEW"

    # Only Assigned to already created vm
    requested_start = "REQUESTED_START"

    # These all are for running vms
    requested_shutdown = "REQUESTED_SHUTDOWN"
    requested_migrate = "REQUESTED_MIGRATE"
    requested_delete = "REQUESTED_DELETE"
    # either its image is not found or user requested
    # to delete it
    deleted = "DELETED"
    
    stopped = "STOPPED"  # After requested_shutdown
    killed = "KILLED"  # either host died or vm died itself

    running = "RUNNING"

    error = "ERROR"  # An error occurred that cannot be resolved automatically


class VMEntry(SpecificEtcdEntryBase):
    
    def __init__(self, e):
        self.owner = None  # type: str
        self.specs = None  # type: dict
        self.hostname = None  # type: str
        self.status = None  # type: str
        self.image_uuid = None  # type: str
        self.log = None  # type: list
        self.in_migration = None  # type: bool
        
        super().__init__(e)

    @property
    def uuid(self):
        return self.key.split("/")[-1]

    def declare_killed(self):
        self.hostname = ""
        self.in_migration = False
        if self.status == VMStatus.running:
            self.status = VMStatus.killed

    def declare_stopped(self):
        self.hostname = ""
        self.in_migration = False
        self.status = VMStatus.stopped

    def add_log(self, msg):
        self.log = self.log[:5]
        self.log.append("{} - {}".format(datetime.now().isoformat(), msg))

    @property
    def path(self):
        return "rbd:uservms/{}".format(self.uuid)


class VmPool:
    def __init__(self, etcd_client, vm_prefix):
        self.client = etcd_client
        self.prefix = vm_prefix

    @property
    def vms(self):
        _vms = self.client.get_prefix(self.prefix, value_in_json=True)
        return [VMEntry(vm) for vm in _vms]

    def by_host(self, host, _vms=None):
        if _vms is None:
            _vms = self.vms
        return list(filter(lambda x: x.hostname == host, _vms))

    def by_status(self, status, _vms=None):
        if _vms is None:
            _vms = self.vms
        return list(filter(lambda x: x.status == status, _vms))

    def except_status(self, status, _vms=None):
        if _vms is None:
            _vms = self.vms
        return list(filter(lambda x: x.status != status, _vms))

    def get(self, key):
        if not key.startswith(self.prefix):
            key = join(self.prefix, key)
        v = self.client.get(key, value_in_json=True)
        if v:
            return VMEntry(v)
        return None

    def put(self, obj: VMEntry):
        self.client.put(obj.key, obj.value, value_in_json=True)

    @contextmanager
    def get_put(self, key) -> VMEntry:
        # Updates object at key on exit
        obj = self.get(key)
        yield obj
        if obj:
            self.put(obj)
