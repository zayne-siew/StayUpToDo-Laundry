# Quick Start Guide

## Run the Frontend

```bash
cd frontend
flutter pub get
flutter run
```

Choose your target device when prompted (Chrome, iOS Simulator, Android Emulator, etc.)

## What You'll See

A laundry machine status dashboard with:
- **10 demo machines** across blocks 55, 57, and 59
- **Color-coded status indicators**:
  - 🟢 Green = Available
  - 🔵 Blue = Paid For  
  - 🟡 Yellow = Pending Unload
  - 🔴 Red = In Use / Out of Order
- **Interactive machine cards** - tap to see details

## Run the Backend

```bash
cd backend
pip install -r requirements.txt
python3 -m src.app
```

Backend will run on `http://localhost:8000`

## Initialize Backend Data

```bash
# Initialize all machines
curl -X POST http://localhost:8000/api/machines/initialize

# Get all machines
curl http://localhost:8000/api/machines

# Get machines by block
curl http://localhost:8000/api/machines?block=55
```

## Project Features

### ✅ Completed
- Machine model with block numbers (55, 57, 59)
- Machine widget with status indicators
- Home screen with machine grid
- Backend API with Flask-RESTful
- In-memory storage
- API endpoints for CRUD operations

### 🎨 Machine Display
- Shows machine ID (e.g., 55W1, 57D2)
- Real-time countdown for in-use machines
- "Out Of Order" message for broken machines
- Tap to view full details and status history

### 🔧 API Integration Ready
- MachineService implemented in Flutter
- Backend API with filtering by block, type, and status
- JSON serialization/deserialization
- Telegram message integration support

## File Structure

```
frontend/lib/
├── main.dart              # App entry point
├── models/machine.dart    # Machine data model
├── screens/home_screen.dart   # Main screen
├── services/machine.dart  # API service
└── widgets/machine.dart   # Machine component

backend/src/
├── app.py                 # Flask app
├── models/                # Data models
├── resources/machine.py   # API endpoints
└── storage.py             # In-memory storage
```

## Next Steps

1. **Connect Frontend to Backend**: Update `baseUrl` in `machine.dart` service
2. **Add Real-time Updates**: Implement WebSocket for live machine status
3. **User Authentication**: Add login/registration
4. **Telegram Bot Integration**: Automate status updates from Telegram group
5. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
