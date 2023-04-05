from typing import AsyncGenerator, Dict, List, Optional

def mux(sources: Dict[int, "HydroflowSource"]) -> "HydroflowSource": ...

def demux(mapping: Dict[int, "HydroflowSink"]) -> "HydroflowSink": ...

def null() -> "HydroflowNull": ...

class HydroflowSource(object):
    pass

class HydroflowSink(object):
    pass

class Deployment(object):
    def __init__(self) -> None: ...

    def Localhost(self) -> "LocalhostHost": ...

    def GCPComputeEngineHost(self, project: str, machine_type: str, image: str, region: str, network: "GCPNetwork") -> "GCPComputeEngineHost": ...

    def CustomService(self, on: "Host", external_ports: List[int]) -> "CustomService": ...

    def HydroflowCrate(self, src: str, on: "Host", example: Optional[str] = None, features: Optional[List[str]] = None, args: Optional[List[str]] = None) -> "HydroflowCrate": ...

    async def deploy(self): ...

    async def start(self): ...

class Host(object):
    pass

class LocalhostHost(Host):
    def client_only() -> "LocalhostHost": ...

class GCPNetwork(object):
    def __init__(self, project: str, existing: Optional[str] = None) -> None: ...

class GCPComputeEngineHost(Host):
    internal_ip: str
    external_ip: Optional[str]
    ssh_key_path: str

class Service(object):
    async def stop(self) -> None: ...

class MuxSource(object):
    def send_to(self, other: HydroflowSink) -> None: ...

class CustomService(Service):
    def client_port(self) -> "CustomServicePort": ...

class CustomServicePort(HydroflowSink):
    def send_to(self, other: HydroflowSink) -> None: ...
    async def server_port(self) -> ServerPort: ...

class HydroflowCrate(Service):
    ports: HydroflowCratePorts
    async def stdout(self) -> AsyncGenerator[str, None]: ...
    async def stderr(self) -> AsyncGenerator[str, None]: ...
    async def exit_code(self) -> int: ...

class HydroflowCratePorts(object):
    def __getattribute__(self, __name: str) -> HydroflowCratePort: ...

class HydroflowCratePort(HydroflowSink):
    def send_to(self, other: HydroflowSink) -> None: ...
    def merge(self) -> "HydroflowCratePort": ...

class HydroflowNull(HydroflowSink):
    def send_to(self, other: HydroflowSink) -> None: ...

class ServerPort(object):
    def json() -> object: ...
    async def into_sink() -> "PythonSink": ...
    async def into_source() -> "PythonStream": ...

class PythonSink(object):
    async def send(self, data: bytes) -> None: ...

class PythonStream(object):
    async def next(self) -> Optional[bytes]: ...
