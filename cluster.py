from dataclasses import dataclass,field
from typing import List,Optional

@dataclass
class VM:
    def __init__(self, vm_id: str, name: str, grading: str, 
                 capability:float, intent: float, attractiveness: float , 
                 cvss_score: int, asset_val: float, exposure_factor: float
                 ):
        self.vm_id = vm_id
        self.name = name
        if grading == "critical":
            self.rpp = 12000
        elif grading == "standard":
            self.rpp = 6000
        elif grading == "utility":
            self.rpp = 3000
        threat = capability * intent * attractiveness

        vulnerability = cvss_score/10


        impact = asset_val * exposure_factor

        self.p_c = threat * vulnerability  

        self.criticality = impact
    def __repr__(self):
        return f"VM(id='{self.vm_id}', name={self.name}, rpp = {self.rpp}, p_c={self.p_c}, criticality={self.criticality})"


@dataclass
class CPU:
    def __init__(self, cpu_id: str, cpu_model: str, num_threads: int, 
                 clock_frequency: int, cpu_type: str):
        self.cpu_id = cpu_id
        self.cpu_model = cpu_model
        if cpu_type == "hp":
            IPC = 4
        elif cpu_type == "md":
            IPC = 2.5
        elif cpu_type == "mb":
            IPC = 1.5
        elif cpu_type == "lg":
            IPC = 0.75
        MIPS = clock_frequency * 1000 * IPC * num_threads

@dataclass
class Server:
    def __init(self, server_id: str, name: str, model: str,
               cpu_limit: int):
        self.server_id = server_id
        self.name = name
        self.model = model
        self.cpu_limit = cpu_limit
        self.cur_cpu = 0
        self.cpus = List[CPU]
               
    def add_CPU(self, cpu: CPU):
        if self.cur_cpu >= self.cpu_limit:
            return "Too many CPUs"


@dataclass
class Rack:
    rack_id: str
    slot_capacity: int
#    servers: List[Server] = field(default_factory=list)
    wattage: int

