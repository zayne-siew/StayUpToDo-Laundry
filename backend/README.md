# StayUpToDo-Laundry Backend API

A Flask-RESTful backend for managing laundry machine status.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The server will run on `http://localhost:5000`

## API Endpoints

### Machines

- `GET /api/machines` - Get all machines
  - Query params: `?status=available` or `?type=washer`
- `POST /api/machines` - Create a new machine
- `GET /api/machines/{machine_id}` - Get specific machine
- `DELETE /api/machines/{machine_id}` - Delete a machine

### Machine Status

- `PUT /api/machines/{machine_id}/status` - Update machine status
  ```json
  {
    "status": "inUse",
    "user": "john_doe",
    "remaining_time_seconds": 1800
  }
  ```

### Machine Time

- `PATCH /api/machines/{machine_id}/time` - Update remaining time
  ```json
  {
    "remaining_time_seconds": 900
  }
  ```

### Telegram Messages

- `PUT /api/machines/{machine_id}/telegram` - Add/update Telegram message
  ```json
  {
    "message": "Machine W1 is ready for pickup",
    "message_url": "https://t.me/..."
  }
  ```
- `DELETE /api/machines/{machine_id}/telegram` - Remove Telegram message

### History

- `GET /api/machines/{machine_id}/history` - Get status history

### Initialization

- `POST /api/machines/initialize` - Initialize 12 washers and 12 dryers

## Example Usage

```bash
# Initialize machines
curl -X POST http://localhost:5000/api/machines/initialize

# Get all machines
curl http://localhost:5000/api/machines

# Update machine status
curl -X PUT http://localhost:5000/api/machines/W1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "inUse", "user": "john", "remaining_time_seconds": 1800}'

# Get available machines
curl http://localhost:5000/api/machines?status=available
```

## Machine Status Types

- `available` - Machine is ready to use
- `paidFor` - Payment received, waiting to start
- `inUse` - Currently running
- `pendingUnload` - Finished, waiting for pickup
- `outOfOrder` - Not working
