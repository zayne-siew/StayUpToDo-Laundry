"""Flask-RESTful resources for machine endpoints"""
from flask import request
from flask_restful import Resource # type: ignore

from ..types import MachineStatus
from ..models import Machine, TelegramMessage
from ..storage import storage

class MachineListResource(Resource):
    """Resource for machine collection"""
    
    def get(self):
        """Get all machines or filter by status/type/block"""
        status = request.args.get('status')
        machine_type = request.args.get('type')
        block = request.args.get('block')
        
        if status:
            try:
                status_enum = MachineStatus(status)
                machines = storage.get_by_status(status_enum)
            except ValueError:
                return {'error': 'Invalid status'}, 400
        elif machine_type:
            machines = storage.get_by_type(machine_type)
        elif block:
            try:
                block_number = int(block)
                if block_number not in [55, 57, 59]:
                    return {'error': 'Block number must be 55, 57, or 59'}, 400
                machines = storage.get_by_block(block_number)
            except ValueError:
                return {'error': 'Invalid block number'}, 400
        else:
            machines = storage.get_all()
        
        return [machine.to_dict() for machine in machines], 200
    
    def post(self):
        """Create a new machine"""
        data = request.get_json()
        
        if not data or 'id' not in data:
            return {'error': 'Machine ID is required'}, 400
        
        machine_id = data['id']
        
        if storage.exists(machine_id):
            return {'error': f'Machine {machine_id} already exists'}, 409
        
        try:
            machine = Machine.from_dict(data)
            created_machine = storage.create(machine)
            return created_machine.to_dict(), 201
        except (ValueError, KeyError) as e:
            return {'error': f'Invalid machine data: {str(e)}'}, 400


class MachineResource(Resource):
    """Resource for individual machine"""

    def get(self, machine_id: str):
        """Get a specific machine"""
        machine = storage.get_by_id(machine_id)
        
        if not machine:
            return {'error': f'Machine {machine_id} not found'}, 404
        
        return machine.to_dict(), 200

    def delete(self, machine_id: str):
        """Delete a machine"""
        if not storage.exists(machine_id):
            return {'error': f'Machine {machine_id} not found'}, 404
        
        storage.delete(machine_id)
        return {'success': f'Machine {machine_id} deleted'}, 204


class MachineStatusResource(Resource):
    """Resource for updating machine status"""

    def put(self, machine_id: str):
        """Update machine status"""
        machine = storage.get_by_id(machine_id)
        
        if not machine:
            return {'error': f'Machine {machine_id} not found'}, 404
        
        data = request.get_json()
        
        if not data or 'status' not in data or 'user' not in data:
            return {'error': 'Status and user are required'}, 400
        
        try:
            new_status = MachineStatus(data['status'])
            user = data['user']
            
            machine.update_status(new_status, user)
            
            # Update remaining time if provided
            if 'remaining_time_seconds' in data:
                machine.remaining_time_seconds = data['remaining_time_seconds']
            
            storage.update(machine)
            return machine.to_dict(), 200
        except ValueError as e:
            return {'error': f'Invalid status: {str(e)}'}, 400


class MachineTimeResource(Resource):
    """Resource for updating machine remaining time"""
    
    def patch(self, machine_id: str):
        """Update remaining time"""
        machine = storage.get_by_id(machine_id)
        
        if not machine:
            return {'error': f'Machine {machine_id} not found'}, 404
        
        data = request.get_json()
        
        if not data or 'remaining_time_seconds' not in data:
            return {'error': 'remaining_time_seconds is required'}, 400
        
        try:
            machine.remaining_time_seconds = int(data['remaining_time_seconds'])
            storage.update(machine)
            return machine.to_dict(), 200
        except (ValueError, TypeError):
            return {'error': 'Invalid time value'}, 400


class MachineTelegramResource(Resource):
    """Resource for managing Telegram messages"""

    def put(self, machine_id: str):
        """Add or update Telegram message"""
        machine = storage.get_by_id(machine_id)
        
        if not machine:
            return {'error': f'Machine {machine_id} not found'}, 404
        
        data = request.get_json()
        
        if not data or 'message' not in data:
            return {'error': 'message is required'}, 400
        
        telegram_message = TelegramMessage(
            message=data['message'],
            message_url=data.get('message_url')
        )
        
        machine.telegram_message = telegram_message
        storage.update(machine)
        return machine.to_dict(), 200

    def delete(self, machine_id: str):
        """Remove Telegram message"""
        machine = storage.get_by_id(machine_id)
        
        if not machine:
            return {'error': f'Machine {machine_id} not found'}, 404
        
        machine.telegram_message = None
        storage.update(machine)
        return machine.to_dict(), 200


class MachineHistoryResource(Resource):
    """Resource for machine status history"""

    def get(self, machine_id: str):
        """Get machine status history"""
        machine = storage.get_by_id(machine_id)
        
        if not machine:
            return {'error': f'Machine {machine_id} not found'}, 404
        
        return [entry.to_dict() for entry in machine.status_history], 200


class MachineInitializeResource(Resource):
    """Resource for initializing default machines"""
    
    def post(self):
        """Initialize washers and dryers"""
        machines = storage.initialize_default_machines()
        return [machine.to_dict() for machine in machines], 201


if __name__ == "__main__":
    pass
