"""Main Flask application for StayUpToDo-Laundry backend"""
from datetime import datetime, timezone
from flask import Flask
from flask_restful import Api  # type: ignore
from flask_cors import CORS  # type: ignore

from src.resources import (
    MachineListResource,
    MachineResource,
    MachineStatusResource,
    MachineTimeResource,
    MachineTelegramResource,
    MachineHistoryResource,
    MachineInitializeResource
)
from src.storage import storage
from src.types import MachineStatus

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for Flutter frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configuration
    app.config['RESTFUL_JSON'] = {
        'ensure_ascii': False
    }
    
    # Initialize Flask-RESTful API
    api = Api(app, prefix='/api')
    
    # Register resources
    api.add_resource(MachineListResource, '/machines')  # pyright: ignore[reportUnknownMemberType]
    api.add_resource(MachineResource, '/machines/<string:machine_id>')  # pyright: ignore[reportUnknownMemberType]
    api.add_resource(MachineStatusResource, '/machines/<string:machine_id>/status')  # pyright: ignore[reportUnknownMemberType]
    api.add_resource(MachineTimeResource, '/machines/<string:machine_id>/time')  # pyright: ignore[reportUnknownMemberType]
    api.add_resource(MachineTelegramResource, '/machines/<string:machine_id>/telegram')  # pyright: ignore[reportUnknownMemberType]
    api.add_resource(MachineHistoryResource, '/machines/<string:machine_id>/history')  # pyright: ignore[reportUnknownMemberType]
    api.add_resource(MachineInitializeResource, '/machines/initialize')  # pyright: ignore[reportUnknownMemberType]

    # Initialize default machines on app startup
    initialize_default_machines()

    return app

def initialize_default_machines():
    """Initialize default machines with sample data for all three blocks"""
    # Initialize all machines first
    storage.initialize_default_machines()
    
    # Helper to calculate finish time from seconds
    def get_finish_time(seconds: int) -> str:
        """Calculate UTC finish time from seconds"""
        finish_time = datetime.now(timezone.utc).timestamp() + seconds
        return datetime.fromtimestamp(finish_time, tz=timezone.utc).isoformat()
    
    # Set some sample statuses for demonstration
    sample_data: list[tuple[str, MachineStatus, int | None]] = [  # type: ignore
        ('55W2', MachineStatus.IN_USE, 165),
        ('55W3', MachineStatus.PAID_FOR, None),
        ('55W4', MachineStatus.PENDING_UNLOAD, None),
        ('55W6', MachineStatus.IN_USE, 300),
        ('55W9', MachineStatus.IN_USE, 120),
        ('55W11', MachineStatus.PAID_FOR, None),
        ('55D2', MachineStatus.IN_USE, 420),
        ('55D4', MachineStatus.OUT_OF_ORDER, None),
        ('57W2', MachineStatus.IN_USE, 90),
        ('57W5', MachineStatus.PAID_FOR, None),
        ('57W8', MachineStatus.IN_USE, 200),
        ('57D3', MachineStatus.IN_USE, 350),
        ('59D1', MachineStatus.PAID_FOR, None),
    ]
    
    for machine_id, status, remaining_seconds in sample_data:
        machine = storage.get_by_id(machine_id)
        if machine:
            machine.update_status(status, user="admin")
            if remaining_seconds:
                machine.estimated_finish_time = get_finish_time(remaining_seconds)
            storage.update(machine)

if __name__ == '__main__':
    app = create_app()
    print("Starting StayUpToDo-Laundry Backend Server...")
    print("Server running at: http://localhost:8000")
    print("API endpoints available at: http://localhost:8000/api/machines")
    app.run(debug=True, host='0.0.0.0', port=8000)
