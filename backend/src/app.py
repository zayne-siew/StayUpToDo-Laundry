"""Main Flask application for StayUpToDo-Laundry backend"""
from flask import Flask
from flask_restful import Api  # type: ignore
from flask_cors import CORS  # type: ignore

from .resources import (
    MachineListResource,
    MachineResource,
    MachineStatusResource,
    MachineTimeResource,
    MachineTelegramResource,
    MachineHistoryResource,
    MachineInitializeResource
)

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
