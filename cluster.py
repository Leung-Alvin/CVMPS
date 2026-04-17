from dataclasses import dataclass,field
from typing import List,Optional

def get_input_with_default(prompt, default_value):
    """Returns user input or a default value if input is empty."""
    user_input = input(f"{prompt} [Default Value: {default_value}]: ").strip()
    return user_input if user_input else default_value

@dataclass
class VM:
    _id_counter = 10000
    def __init__(self,  name: str, grading: str, 
                 capability:float, intent: float, attractiveness: float , 
                 cvss_score: int, asset_val: float, exposure_factor: float
                 ):
        self.vm_id = _id_counter
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
        _id_counter += 1
    def __repr__(self):
        return f"VM(id='{self.vm_id}', name={self.name}, rpp = {self.rpp}, p_c={self.p_c}, criticality={self.criticality})"


@dataclass
class CPU:
    _id_counter = 20000
    def __init__(self,  cpu_model: str, num_threads: int, 
                 clock_frequency: int, cpu_type: str):
        self.cpu_id = CPU._id_counter
        self.cpu_model = cpu_model
        self.cpu_type = cpu_type
        if cpu_type == "hp":
            IPC = 4
        elif cpu_type == "md":
            IPC = 2.5
        elif cpu_type == "mb":
            IPC = 1.5
        elif cpu_type == "lg":
            IPC = 0.75
        self.MIPS = clock_frequency * 1000 * IPC * num_threads
        CPU._id_counter += 1
    def __repr__(self):
        """Official string representation of the CPU instance."""
        return (f"CPU(cpu_id={self.cpu_id!r}, model={self.cpu_model!r}, "
                f"cpu_type={self.cpu_type!r}, MIPs={self.MIPS!r})")
         

@dataclass
class Server:
    _id_counter = 30000
    def __init__(self, name: str, model: str,
               size: int,
               cpu_limit: int):
        self.server_id = Server._id_counter
        self.name = name
        self.model = model
        self.size = size
        self.cpu_limit = cpu_limit
        self.cur_cpu = 0
        self.CPUs = []
        Server._id_counter+=1
               
    def add_cpu_menu(self):
        print("=== NEW CPU ===")
        model = get_input_with_default("What is the CPU's model?", "Unknown")
        size = get_input_with_default("What is the CPU's number of threads (Cores x Threads per Core)?", 2)
        clock_frequency = get_input_with_default("What is the CPU's clock frequency (GHz)?", 3)
        cpu_type = get_input_with_default("What is the type of the CPU? hp = High-Performance, md = Mainstream Desktop, mb = Mobile, lg = Legacy", "md")
        new_cpu = CPU(model, size, clock_frequency, cpu_type)
        self.CPUs.append(new_cpu)
        print(f"Successfully added: {new_cpu}")
        input("\nPress Enter to return to confirm...")

    def add_CPU(self, cpu: CPU):
        if self.cur_cpu >= self.cpu_limit:
            return "Too many CPUs"
        self.cpus.append(cpu)

    def __repr__(self):
        """Official string representation of the Server instance."""
        return (f"Server(server_id={self.server_id!r}, name={self.name!r}, "
                f"model={self.model!r}, size={self.size!r}, "
                f"cpu_limit={self.cpu_limit!r})")
@dataclass
class Rack:
    _id_counter = 40000

    def __init(self, name: str, slot_capacity: int,
               wattage: int):
        self.rack_id = _id_counter
        self.name = name
        self.slot_capacity = slot_capacity
        self.wattage = wattage
        self.Servers = List[Server]
        _id_counter+=1

@dataclass
class Cluster:
    def __init__(self):
        self.racks = []
        self.VMs = []
        self.servers = []
        self.CPUs = []
        self.running = True

    def clear_screen(self):
        # Optional: Clears terminal for a cleaner feel
        print("\033[H\033[J", end="")

    def main_menu(self):
        while self.running:
            self.clear_screen()
            print("=== MAIN MENU ===")
            print("1. Add to Build")
            print("2. Load Build")
            print("3. Display Build")
            print("4. Generate Allocation")
            print("q. Quit")
        
            choice = input("\nSelect: ").lower()

            if choice == '1': self.new_build_menu()
            elif choice == '2': self.load_build_menu()
            elif choice == '3': self.display_build()
            elif choice == '4': self.compute_allocation()
            elif choice == 'q': self.running = False

    def display_build(self):
        print("=== CURRENT BUILD ===")
        print(repr(self))
        input("\nPress Enter to return to confirm...")

    def new_build_menu(self):
        print("=== ADD TO BUILD ===")
        print("1. Add Server Rack")
        print("2. Add Server")
        #print("1. Add CPU")
        print("3. Add VM")
        print("b. Back to Main")
        
        choice = input("\nSelect: ").lower()
        if choice == '2': self.add_server_menu()
        #elif choice == 'b': return "MAIN"

    def compute_allocation(self):
        print("=== SECURE ALLOCATION STRATEGY ===")
        input("\nPress Enter to return to confirm...")

    def add_server_menu(self):
        print("=== NEW SERVER ===")
        name = get_input_with_default("What is the server's name?", "Server's ID")
        model = get_input_with_default("What is the server's model?", "Unknown")
        size = get_input_with_default("What is the server's size (U)?", 1)
        num_cpu = int(get_input_with_default("What is the number of CPUs that the server can hold?", "1"))
        new_server = Server(name, model, size, num_cpu)
        if num_cpu > 0:
            for i in range(0,num_cpu):
                new_server.add_cpu_menu()
                

        self.servers.append(new_server)
        print(f"Successfully added: {new_server}")
        input("\nPress Enter to return to confirm...")
        #return "NEW_BUILD"

    def load_build_menu():
        print("=== LOAD BUILD ===")
        print("1. View Stats")
        print("b. Back to Main")
        
        choice = input("\nSelect: ").lower()
        if choice == 'b': return "MAIN"
        #return "LOAD_BUILD"


    def __repr__(self):
        ret = ""
        ret+="Racks:\n"
        for rack in self.racks:
            ret+=rack
            ret+="\n"
        ret+="\nServers:\n"
        for server in self.servers:
            ret+=repr(server)
            ret+="\n"
            for CPU in server.CPUs:
                ret+=repr(CPU)
                ret+="\n"
        ret+="\nVMs:\n"
        for VM in self.VMs:
            ret+=VM
            ret+="\n"
        return(ret) 
