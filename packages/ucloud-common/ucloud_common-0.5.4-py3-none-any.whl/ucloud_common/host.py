from typing import List
from datetime import datetime
from os.path import join

from .helpers import SpecificEtcdEntryBase


class HostStatus:
    """Possible Statuses of ucloud host."""

    alive = "ALIVE"
    dead = "DEAD"


class HostEntry(SpecificEtcdEntryBase):
    """Represents Host Entry Structure and its supporting methods."""

    def __init__(self, e):
        self.specs = None  # type: dict
        self.hostname = None  # type: str
        self.status = None  # type: str
        self.last_heartbeat = None  # type: str
        
        super().__init__(e)

    def update_heartbeat(self):
        self.status = HostStatus.alive
        self.last_heartbeat = datetime.utcnow().isoformat()

    def is_alive(self):
        last_heartbeat = datetime.fromisoformat(self.last_heartbeat)
        delta = datetime.utcnow() - last_heartbeat
        if delta.total_seconds() > 60:
            return False
        return True

    def declare_dead(self):
        self.status = HostStatus.dead
        self.last_heartbeat = datetime.utcnow().isoformat()


class HostPool:
    def __init__(self, etcd_client, host_prefix):
        self.client = etcd_client
        self.prefix = host_prefix

    @property
    def hosts(self) -> List[HostEntry]:
        _hosts = self.client.get_prefix(self.prefix, value_in_json=True)
        return [HostEntry(host) for host in _hosts]

    def get(self, key):
        if not key.startswith(self.prefix):
            key = join(self.prefix, key)
        v = self.client.get(key, value_in_json=True)
        if v:
            return HostEntry(v)
        return None

    def put(self, obj: HostEntry):
        self.client.put(obj.key, obj.value, value_in_json=True)

    def by_status(self, status, _hosts=None):
        if _hosts is None:
            _hosts = self.hosts
        return list(filter(lambda x: x.status == status, _hosts))
