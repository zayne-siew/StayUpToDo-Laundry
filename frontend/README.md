# Running the StayUpToDo-Laundry Frontend

## Prerequisites

1. **Flutter SDK** installed (version 3.10.0 or higher)
2. **Dart SDK** (comes with Flutter)
3. A device or emulator to run the app

## Installation Steps

### 1. Navigate to the frontend directory
```bash
cd frontend
```

### 2. Set up environment variables

Copy the `.env.example` template file to `.env.local` and set up the required environment variables accordingly.

### 3. Install dependencies
```bash
flutter pub get
```

### 4. Check for connected devices
```bash
flutter devices
```

### 5. Run the app
```bash
flutter run
```

Or run on a specific device:
```bash
# Run on Chrome
flutter run -d chrome

# Run on an iOS simulator
flutter run -d iPhone

# Run on an Android emulator
flutter run -d emulator-5554
```

## What You'll See

The home screen displays:

- **Laundry Machine Status** - A grid of machine widgets organized by block
- **Block 55, 57, 59 sections** - Each showing machines from that block
- **Machine widgets** showing:
  - Machine ID (e.g., 55W1, 57D2)
  - Remaining time (for in-use machines)
  - "Out Of Order" message (for broken machines)
  - Color-coded status indicator:
    - 🟢 Green = Available
    - 🔵 Blue = Paid For
    - 🟡 Yellow = Pending Unload
    - 🔴 Red = In Use / Out of Order

### Interactive Features

- **Tap any machine** to see detailed information:
  - Block number
  - Machine type (washer/dryer)
  - Current status
  - Remaining time
  - Complete status history
  - Telegram messages (if any)

## Sample Data

The app currently displays 10 demo machines across blocks 55, 57, and 59 with various statuses.

## Hot Reload

While the app is running, you can make changes to the code and press:
- `r` to hot reload
- `R` to hot restart
- `q` to quit

## Troubleshooting

### If you get package errors:
```bash
flutter clean
flutter pub get
```

### If you get build errors:
```bash
flutter doctor
```

### Check Flutter version:
```bash
flutter --version
```

## Next Steps

To connect to the backend API:
1. Start the Python Flask backend (see `backend/src/README.md`)
2. Update the `baseUrl` in `lib/services/machine.dart` to point to your backend
3. Use `MachineService` to fetch real machine data

## Project Structure

```
frontend/lib/
├── main.dart              # App entry point
├── models/
│   └── machine.dart       # Machine data model
├── screens/
│   └── home_screen.dart   # Main screen with machine grid
├── services/
│   └── machine.dart       # API service for backend
└── widgets/
    └── machine.dart       # Machine widget component
```
