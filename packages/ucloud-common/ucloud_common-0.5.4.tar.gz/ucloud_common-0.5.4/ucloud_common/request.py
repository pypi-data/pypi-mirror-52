import json

from decouple import config
from etcd3_wrapper.etcd3_wrapper import PsuedoEtcdEntry
from uuid import uuid4
from .helpers import SpecificEtcdEntryBase
from os.path import join


class RequestType:
    CreateVM = "CreateVM"
    ScheduleVM = "ScheduleVM"
    StartVM = "StartVM"
    StopVM = "StopVM"
    InitVMMigration = "InitVMMigration"
    TransferVM = "TransferVM"
    DeleteVM = "DeleteVM"


class RequestEntry(SpecificEtcdEntryBase):
    
    def __init__(self, e):
        self.type = None  # type: str
        self.migration = None  # type: bool
        self.destination = None  # type: str
        self.uuid = None  # type: str
        self.hostname = None  # type: str
        
        super().__init__(e)
        

    @classmethod
    def from_scratch(cls, **kwargs):
        e = PsuedoEtcdEntry(join(config("REQUEST_PREFIX"), uuid4().hex), value=json.dumps(kwargs).encode("utf-8"),
                            value_in_json=True)
        return cls(e)


class RequestPool:
    def __init__(self, etcd_client, request_prefix):
        self.client = etcd_client
        self.prefix = request_prefix

    def put(self, obj: RequestEntry):
        if not obj.key.startswith(self.prefix):
            obj.key = join(self.prefix, obj.key)

        self.client.put(obj.key, obj.value, value_in_json=True)
