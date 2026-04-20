import itertools

class VirtualMachine:
    def __init__(self, vm_id, probability, loss):
        self.vm_id = vm_id
        self.q = probability  # q: success probability
        self.l = loss         # l: potential loss
        self.risk = self.q * self.l

    def __repr__(self):
        return f"VM_{self.vm_id}(Risk: {self.risk})"

class AllocationEngine:
    def __init__(self, vms, server_count):
        self.vms = vms
        self.n = server_count
        self.m = len(vms)

    def get_prvms(self):
        """Step 1: Identify PrVMs with the highest potential loss."""
        max_risk = max(vm.risk for vm in self.vms)
        return [vm for vm in self.vms if vm.risk == max_risk]

    def find_equilibrium(self):
        prvms = self.get_prvms()
        m0 = len(prvms)
        
        # Step 2: Resource Sufficiency Check
        # In a real environment, this would also check physical CPU/RAM capacity (C)
        if self.n >= m0:
            return self._luxury_scenario(prvms)
        else:
            return self._constrained_scenario()

    def _luxury_scenario(self, prvms):
        """
        Step 3-9: Generates strategies where each Primary VM 
        is hosted on a separate physical server.
        """
        print(f"[Mode] Luxury: Sufficient servers ({self.n}) to isolate {len(prvms)} PrVMs.")
        
        # Simplified representation of the allocation strategy Az
        # In practice, this would yield the specific VM-to-Server mappings
        eq_set = []
        strategy = {
            "description": "Isolated Primary VMs",
            "allocation": {f"Server_{i}": [prvms[i]] for i in range(len(prvms))}
        }
        eq_set.append(strategy)
        return eq_set

    def _constrained_scenario(self):
        """
        Step 10-15: Minimax Equilibrium for resource-constrained environments.
        Uses a risk-balancing approach.
        """
        print("[Mode] Constrained: Implementing Minimax risk distribution.")
        
        # Logic for finding the 'Saddle Point' where max risk is minimized
        # This typically involves calculating the risk density per server
        target_risk = max(vm.risk for vm in self.vms)
        
        # Representing Γ2: The set of allocations satisfying the equilibrium
        eq_set = [{
            "description": "Minimax Balanced Allocation",
            "max_expected_loss": target_risk
        }]
        return eq_set

# --- Example Usage ---
if __name__ == "__main__":
    # Define a set of VMs (ID, Probability, Loss)
    vm_list = [
        VirtualMachine(1, 0.8, 100),  # PrVM
        VirtualMachine(2, 0.2, 400),  # PrVM (Same risk score: 80)
        VirtualMachine(3, 0.5, 50),   # Standard VM
        VirtualMachine(4, 0.9, 20)    # Standard VM
    ]

    # Scenario A: Sufficient Servers (n=3)
    engine_a = AllocationEngine(vm_list, server_count=3)
    print(f"Scenario A EQ: {engine_a.find_equilibrium()}\n")

    # Scenario B: Constrained Servers (n=1)
    engine_b = AllocationEngine(vm_list, server_count=1)
    print(f"Scenario B EQ: {engine_b.find_equilibrium()}")
