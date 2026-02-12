"""In-memory storage for machines (can be replaced with database)"""
from .types import MachineStatus
from .models import Machine

class MachineStorage:
    """In-memory storage for machines"""
    def __init__(self):
        self._machines: dict[str, Machine] = {}  # type: ignore

    def get_all(self) -> list[Machine]:
        """Get all machines"""
        return list(self._machines.values())
    
    def get_by_id(self, machine_id: str) -> Machine | None:
        """Get machine by ID"""
        return self._machines.get(machine_id)
    
    def create(self, machine: Machine) -> Machine:
        """Create a new machine"""
        self._machines[machine.id] = machine
        return machine
    
    def update(self, machine: Machine) -> Machine:
        """Update an existing machine"""
        self._machines[machine.id] = machine
        return machine
    
    def delete(self, machine_id: str) -> bool:
        """Delete a machine"""
        if machine_id in self._machines:
            del self._machines[machine_id]
            return True
        return False
    
    def get_by_status(self, status: MachineStatus) -> list[Machine]:
        """Get machines by status"""
        return [m for m in self._machines.values() if m.status == status]
    
    def get_by_type(self, machine_type: str) -> list[Machine]:
        """Get machines by type (washer/dryer)"""
        type_char = 'W' if machine_type.lower() == 'washer' else 'D'
        return [m for m in self._machines.values() if type_char in m.id]
    
    def get_by_block(self, block_number: int) -> list[Machine]:
        """Get machines by block number"""
        return [m for m in self._machines.values() if m.block_number == block_number]
    
    def exists(self, machine_id: str) -> bool:
        """Check if machine exists"""
        return machine_id in self._machines
    
    def initialize_default_machines(
        self,
        *,
        washers_55: int = 11,
        washers_57: int = 11,
        washers_59: int = 11,
        dryers_55: int = 6,
        dryers_57: int = 6,
        dryers_59: int = 6,
    ) -> list[Machine]:
        """Initialize washers and dryers for each block (55, 57, 59)"""
        machines: list[Machine] = []
        blocks = [
            (55, washers_55, dryers_55),
            (57, washers_57, dryers_57),
            (59, washers_59, dryers_59),
        ]

        for block, washers, dryers in blocks:
            # Create washers for this block
            for i in range(1, washers + 1):
                machine = Machine(
                    id=f'{block}W{i}',
                    block_number=block,
                    status=MachineStatus.AVAILABLE
                )
                self._machines[machine.id] = machine
                machines.append(machine)

            # Create dryers for this block
            for i in range(1, dryers + 1):
                machine = Machine(
                    id=f'{block}D{i}',
                    block_number=block,
                    status=MachineStatus.AVAILABLE
                )
                self._machines[machine.id] = machine
                machines.append(machine)
        
        return machines


if __name__ == '__main__':
    # Global storage instance
    storage = MachineStorage()
