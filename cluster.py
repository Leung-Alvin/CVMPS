from dataclasses import dataclass,field
from typing import List,Optional
import itertools
import copy
import heapq

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
        self.vm_id = VM._id_counter
        self.name = name
        if grading == "c":
            self.rpp = 12000
        elif grading == "s":
            self.rpp = 6000
        elif grading == "u":
            self.rpp = 3000
        threat = capability * intent * attractiveness

        vulnerability = cvss_score/10


        impact = asset_val * exposure_factor

        self.p_c = threat * vulnerability  

        self.criticality = impact
        self.primality = self.p_c * self.criticality
        VM._id_counter += 1
    def __repr__(self):
        return f"VM(id='{self.vm_id}', name={self.name}, MIPs = {self.rpp}, p_c={self.p_c}, criticality={self.criticality}, risk = {self.primality})"


@dataclass
class CPU:
    _id_counter = 20000
    def __init__(self,  cpu_model: str, num_threads: int, 
                 clock_frequency: float, cpu_type: str):
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
        self.VMs = []
        self.MIPs = 0
        self.available_MIPs = 0
        Server._id_counter+=1
        self.risk = 0
               
    def add_cpu_menu(self):
        print("=== NEW CPU ===")
        model = get_input_with_default("What is the CPU's model?", "Unknown")
        size = get_input_with_default("What is the CPU's number of threads (Cores x Threads per Core)?", 2)
        try:
            size = int(size)
        except:
            print("Wrong Type Used. Please enter an integer for the number of threads")
            size = get_input_with_default("What is the CPU's number of threads (Cores x Threads per Core)?", 2)
            size = int(size)


        clock_frequency = get_input_with_default("What is the CPU's clock frequency (GHz)?", 3)
        try:
            clock_frequency = float(clock_frequency)
        except:
            print("Wrong Type Used. Please enter an double for the CPU clock frequency")
            clock_frequency = get_input_with_default("What is the CPU's clock frequency (GHz)?", 3)
            clock_frequency = float(clock_frequency)
        cpu_type = get_input_with_default("What is the type of the CPU? hp = High-Performance, md = Mainstream Desktop, mb = Mobile, lg = Legacy", "md")
        if cpu_type not in ["hp","md","mb","lg"]:
            cpu_type = get_input_with_default("What is the type of the CPU? hp = High-Performance, md = Mainstream Desktop, mb = Mobile, lg = Legacy", "md")
        new_cpu = CPU(model, size, clock_frequency, cpu_type)
        self.CPUs.append(new_cpu)
        self.MIPs += new_cpu.MIPS
        self.available_MIPs += new_cpu.MIPS
        print(f"Successfully added: {new_cpu}")
        input("\nPress Enter to return to confirm...")

    def add_CPU(self, cpu: CPU):
        if self.cur_cpu >= self.cpu_limit:
            return "Too many CPUs"
        self.cpus.append(cpu)

    def add_VM(self, vm:VM):
        if self.available_MIPs - vm.rpp >= 0:
            self.VMs.append(vm)
            self.available_MIPs-= vm.rpp
            self.risk+=vm.primality
        else:
            return -1

     


    def __repr__(self):
        """Official string representation of the Server instance."""
        return (f"Server(server_id={self.server_id!r}, name={self.name!r}, "
                f"model={self.model!r}, size={self.size!r}, "
                f"cpu_limit={self.cpu_limit!r}, total_MIPs={self.MIPs!r}, RISK = {self.risk!r})")
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
            print("4. Change Build")
            print("5. Find Primary VMs")
            print("6. Generate Allocation")
            print("q. Quit")
        
            choice = input("\nSelect: ").lower()

            if choice == '1': self.new_build_menu()
            elif choice == '2': self.load_build_menu()
            elif choice == '3': self.display_build()
            elif choice == '4': self.change_build_menu()
            elif choice == '5': self.find_primaries()
            elif choice == '6': self.compute_allocation()
            elif choice == 'q': self.running = False

    def find_primaries(self):
        if len(self.VMs) > 0:
            max_primality = max(vm.primality for vm in self.VMs)
            primary_VMs = [vm for vm in self.VMs if vm.primality == max_primality]
            for VM in primary_VMs:
                print(repr(VM))
            input("\nPress Enter to return to return to main menu...")
        else:
            print("No VMs detected")
            input("\nPress Enter to return to return to main menu...")


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
        elif choice == '3': self.add_VM_menu()
        #elif choice == 'b': return "MAIN"

    def compute_allocation(self):
        print("=== SECURE ALLOCATION STRATEGY ===")
        if len(self.VMs) > 0 and len(self.servers) > 0:
            max_primality = max(vm.primality for vm in self.VMs)
            primary_VMs = [vm for vm in self.VMs if vm.primality == max_primality]
            max_rpp = max(vm.rpp for vm in primary_VMs)
            count = 0
            for server in self.servers:
                if server.available_MIPs >= max_rpp:
                    count+=1
            if count >= len(primary_VMs):
                self.luxury_allocation()
            else:
                self.constrained_allocation()
        else:
            print("Not enough servers and/or VMs to compute allocation.")
        input("\nPress Enter to return to confirm...")


    def luxury_allocation(self):
        print("=== Attempting Luxury Allocation ===")
        copy_servers = []
        copy_VMs = []
        for server in self.servers:
            copy_servers.append(copy.deepcopy(server))
        for VM in self.VMs:
            copy_VMs.append(copy.deepcopy(VM))

        sorted_servers = sorted(copy_servers, key=lambda x: x.available_MIPs)
        sorted_VMs = sorted(copy_VMs, key = lambda x : x.primality)
        unallocated_VMs = []
        max_primality = max(vm.primality for vm in self.VMs)
        primary_VMs = []
        for VM in sorted_VMs:
            if VM.primality == max_primality:
                primary_VMs.append(copy.deepcopy(VM))
            else:
                unallocated_VMs.append(copy.deepcopy(VM))

        allocation_strategy = []
        for VM in primary_VMs:
            target_rpp = VM.rpp
            for i in range(len(sorted_servers)):
                if sorted_servers[i].available_MIPs >= target_rpp:
                    sorted_servers[i].add_VM(copy.deepcopy(VM))
                    allocation_strategy.append(copy.deepcopy(sorted_servers[i]))
                    sorted_servers.pop(i)
                    break
        server_heap = []
        for server in sorted_servers:
            heapq.heappush(server_heap, (server.risk, copy.deepcopy(server)))
        luxury_allocation_failure = False
        for VM in unallocated_VMs:
            shelved_servers = []
            allocated = False

            while server_heap:
                risk,server = heapq.heappop(server_heap)

                if server.available_MIPs >= VM.rpp:

                    server.add_VM(VM)

                    heapq.heappush(server_heap, (server.risk, server))
                    allocated = True
                    break
                else:
                    shelved_servers.append((risk,server))
            for item in shelved_servers:
                heapq.heappush(server_heap, item)
            if not allocated:
                print("Luxury Allocation Failed. Defaulting to Constrained Allocation due to capacity issues.")
                luxury_allocation_failure = True
                self.constrained_allocation()
                break

        while server_heap:
            risk, server = heapq.heappop(server_heap)
            allocation_strategy.append(copy.deepcopy(server))


        if luxury_allocation_failure == False:
            for server in allocation_strategy:
                print("=== SERVER ===")
                print(repr(server))
                for VM in server.VMs:
                    print("=== VM ===")
                    print(repr(VM), "\n")
                           



    def constrained_allocation(self):
        print("=== Constrained Allocation ===")
        copy_servers = []
        copy_VMs = []
        for server in self.servers:
            copy_servers.append(copy.deepcopy(server))
        for VM in self.VMs:
            copy_VMs.append(copy.deepcopy(VM))

        sorted_servers = sorted(copy_servers, key=lambda x: x.available_MIPs)
        sorted_VMs = sorted(copy_VMs, key = lambda x : x.rpp, reverse=True)
        allocation_strategy = []
        server_heap = []
        for server in sorted_servers:
            heapq.heappush(server_heap, (server.risk, copy.deepcopy(server)))
        for VM in sorted_VMs:
            shelved_servers = []
            allocated = False

            while server_heap:
                risk,server = heapq.heappop(server_heap)

                if server.available_MIPs >= VM.rpp:

                    server.add_VM(VM)

                    heapq.heappush(server_heap, (server.risk, server))
                    allocated = True
                    break
                else:
                    shelved_servers.append((risk,server))
            for item in shelved_servers:
                heapq.heappush(server_heap, item)
            if not allocated:
                print(f"Warning: Could not allocated VM {VM.vm_id} due to capacity.")

        while server_heap:
            risk, server = heapq.heappop(server_heap)
            allocation_strategy.append(copy.deepcopy(server))

        for server in allocation_strategy:
            print("=== SERVER ===")
            print(repr(server))
            for VM in server.VMs:
                print("=== VM ===")
                print(repr(VM), "\n")
                           

    def change_build_menu(self):
        print("=== CHANGE FROM BUILD ===")
        print("1. Change Server Rack")
        print("2. Change Server")
        print("3. Change CPU")
        print("4. Change VM")
        print("b. Back to Main")

        choice = input("\nSelect: ").lower()
        if choice == '1': self.new_build_menu()
        elif choice == '2': self.change_server_menu()
        elif choice == '3': self.display_build()
        elif choice == '4': self.change_build_menu()
        #elif choice == '4': self.compute_allocation()
        #elif choice == 'q': self.running = False

    def add_server_menu(self):
        print("=== NEW SERVER ===")
        name = get_input_with_default("What is the server's name?", "Default Server")
        model = get_input_with_default("What is the server's model?", "Unknown")
        size = get_input_with_default("What is the server's size (U)?", 1)
        num_cpu = int(get_input_with_default("What is the number of CPUs that the server can hold?", "1"))
        quantity = get_input_with_default("What is the quantity of this server?", "1")
        try:
            quantity = int(quantity)
        except:
            quantity = get_input_with_default("What is the quantity of this server?", "1")
            quantity = int(quantity)
        if quantity > 0:
            for i in range(0,quantity):
                new_server = Server(name, model, size, num_cpu)
                if num_cpu > 0:
                    for i in range(0,num_cpu):
                        new_server.add_cpu_menu()
                        

                self.servers.append(new_server)
                print(f"Successfully added: {new_server}")
        input("\nPress Enter to return to confirm...")
        #return "NEW_BUILD"

    def add_VM_menu(self):
        print("=== NEW VM ===")
        name = get_input_with_default("What is the VM's name?", "Default VM")
        vm_grading = get_input_with_default("What is the grading of the VM? c = Critical (12K MIPS), s = Standard (6K MIPS), u = Utility (3K MIPS)", "s")
        if vm_grading not in ["c","s","u"]:
            vm_grading = get_input_with_default("What is the grading of the VM? c = Critical (12K MIPS), s = Standard (6K MIPS), u = Utility (3K MIPS)", "s")
        capability = get_input_with_default("Do you expect your typical attacker to have the capability to attack this VM (0.1-1.0)?", "0.5")
        try:
            capability = float(capability)
        except:
            capability = get_input_with_default("Do you expect your typical attacker to have the capability to attack this VM (0.1-1.0)?", "0.5")
            capability = float(capability)
        intent = get_input_with_default("How motivated are attackers to attack your organization (0.1-1.0)?", "0.5")
        try:
            intent = float(intent)
        except:
            intent = get_input_with_default("How motivated are attackers to attack your organization (0.1-1.0)?", "0.5")
            intent = float(intent)

        attractiveness = get_input_with_default("Grade the value of the data stored on this VM (0.1 is unimportant data and 1.0 is high-value PII or proprietary code) (0.1-1.0)?", "0.5")
        try:
            attractiveness = float(attractiveness)
        except:
            attractiveness = get_input_with_default("Grade the value of the data stored on this VM (0.1 is unimportant data and 1.0 is high-value PII or proprietary code) (0.1-1.0)?", "0.5")
            attractiveness = float(attractiveness)

            cvss_score = get_input_with_default("Take the CVSS test for the VM: https://www.first.org/cvss/calculator/4.0 and provide the VM's score (0.0-10.0)?", "5.0")
        try:
            cvss_score = float(cvss_score)
        except:
            cvss_score = get_input_with_default("Take the CVSS test for the VM: https://www.first.org/cvss/calculator/4.0 and provide the VM's score (0.0-10.0)?", "5.0")
            cvss_score = float(cvss_score)

            asset_val = get_input_with_default("What is the total cost of the VM, labor, and value of the VM? (in USD)", "500.0")
        try:
            asset_val = float(asset_val)
        except:
            asset_val = get_input_with_default("What is the total cost of the VM, labor, and value of the VM? (in USD)", "500.0")
            asset_val = float(asset_val)


            exposure_factor = get_input_with_default("What is the expected percent of the asset loss on a cybersecurity event (0-1)?", "0.8")
        try:
            exposure_factor = float(exposure_factor)
        except:
            exposure_factor = get_input_with_default("What is the expected percent of the asset loss on a cybersecurity event (0-1)?", "0.8")
            exposure_factor = float(exposure_factor)
            quantity = get_input_with_default("What is the quantity of this VM?", "1")
        try:
            quantity = int(quantity)
        except:
            quantity = get_input_with_default("What is the quantity of this VM?", "1")
            quantity = int(quantity)
        if quantity > 0:
            for i in range(0,quantity):
                new_VM = VM(name, vm_grading, capability, intent, attractiveness, cvss_score, asset_val,
                            exposure_factor)
                self.VMs.append(new_VM)
                print(f"Successfully added: {new_VM}")
        input("\nPress Enter to return to confirm...")

    def change_server_menu(self):
        print("=== CHANGE SERVER ===")
        n = 0
        for server in self.servers:
            s = str(n) + ": " + repr(server)
            s.replace("\n","")
            print(s)
            for CPU in server.CPUs:
                print(repr(CPU))
                print("\n")
            n+=1
        num = get_input_with_default("Which server do you want to change?", -1)
        try:
            num = int(num)
        except:
            "Invalid Input"
         
        if num == -1:
            print("Change cancelled")
        if num >= len(self.servers):
            print("Invalid index")        
        else: 
            change = get_input_with_default("Do you want to change (c) or remove (r) the server?", "n")
            if change == "n":
                print("Change Cancelled")
            elif change == "c":
                print("=== CHANGE CPU ===")
                atrs = [a for a in dir(self.servers[num]) if not a.startswith('__')]
                m = 0
                for atr in atrs:
                    print(m, " ")
                    print(atr, "\n")
                    m+=1
                input("\nPress Enter to return to return...")
            elif change == "r":
                self.servers.pop(num)
                print("Server Deleted")
                input("\nPress Enter to return to return...")
            else:
                print("Invalid Input")

    def load_build_menu(self):
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
        server_n = 0
        for server in self.servers:
            ret+="\n"
            ret+= str(server_n)
            ret+= ": "
            ret+=repr(server)
            ret+="\n"
            cpu_n = 0
            for CPU in server.CPUs:
                ret+= str(server_n)
                ret+="."
                ret+=str(cpu_n)
                ret+=": "
                ret+=repr(CPU)
                ret+="\n"
                cpu_n += 1
            server_n+=1
        ret+="\nVMs:\n"
        vm_n = 0
        for VM in self.VMs:
            ret+="\n"
            ret+=str(vm_n)
            ret+=": "
            ret+=repr(VM)
            ret+="\n"
            vm_n+=1
        return(ret) 
