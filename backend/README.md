# StayUpToDo-Laundry Backend

A comprehensive backend system for managing laundry machine statuses in SUTD hostel blocks (55, 57, 59). This backend consists of two main components:

1. **Flask REST API** - Provides HTTP endpoints for machine status management
2. **Telegram Monitor** - Automatically monitors Telegram messages and updates machine statuses using AI 

## Features

### 1. Flask REST API

A RESTful API built with Flask-RESTful that manages:
- ✅ Machine inventory (washers and dryers for blocks 55, 57, 59)
- ✅ Real-time status updates (available, in use, paid for, pending unload, out of order)
- ✅ Status history tracking
- ✅ Remaining time management
- ✅ Telegram message references

### 2. Telegram Monitor (AI-Powered)

An intelligent monitoring system that:
- 🤖 Monitors Telegram group chat messages in real-time
- 🎯 Filters messages for laundry-related content
- 🧠 Uses OpenAI GPT-4 to parse natural language messages
- 📝 Automatically updates machine statuses via API
- 🔄 Runs continuously with configurable check intervals
- 📊 Logs all activities for debugging

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Access to a Telegram account (for monitoring)
- OpenAI API key (for AI parsing)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env.local
```

Edit `.env.local` with your credentials:

```bash
# Telegram API credentials (from https://my.telegram.org)
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=+1234567890
TELEGRAM_PASSWORD=your_2fa_password

# Telegram chat to monitor
TELEGRAM_CHAT_ID=-1001234567890

# OpenAI API key (from https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-...

# Backend API URL (default: http://localhost:8000)
API_BASE_URL=http://localhost:8000

# Check interval in seconds (default: 30)
CHECK_INTERVAL=30
```

## Running the Backend

**Important:** Run the Flask API first, then start the Telegram monitor.

### Terminal 1: Start Flask API

```bash
cd backend
python src/app.py
```

The API server will start at `http://localhost:8000`

You should see:
```
Starting StayUpToDo-Laundry Backend Server...
Server running at: http://localhost:8000
API endpoints available at: http://localhost:8000/api/machines
```

### Terminal 2: Start Telegram Monitor

Once the API is running, start the Telegram monitor in a separate terminal:

```bash
cd backend
python telegram_monitor.py
```

On first run, you'll be prompted to:
1. Enter the authentication code sent to your Telegram app
2. Enter your 2FA password (if enabled)

After authentication, the monitor will start processing messages:
```
Starting Telegram monitor...
Successfully connected to Telegram
Monitor started. Checking every 30 seconds...
```

## How It Works

### Telegram Monitor Workflow

```text
┌─────────────────────────────────────────────────┐
│  1. Connect to Telegram                         │
│     - Authenticate using API credentials        │
│     - Create persistent session                 │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  2. Fetch New Messages (every 30 seconds)       │
│     - Get messages since last check             │
│     - Track last message timestamp              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  3. Filter Messages                             │
│     - Contains 55, 57, or 59? ✓                 │
│     - Contains washer/dryer keywords? ✓         │
│     - Skip if no match                          |
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  4. Parse with OpenAI GPT-4                     │
│     - Extract machine_id (e.g., "55W4")         │
│     - Determine status change                   │
│     - Assess confidence level                   │
│     - Return JSON or mark as irrelevant         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  5. Update Machine Status via API               │
│     - GET current machine info from API         │
│     - PUT updated status to API endpoint        │
│     - PUT telegram message reference            │
│     - Add to status history                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  6. Log Result                                  │
│     - ✅ Success: Log update                    │
│     - ❌ Error: Log error and continue          │
│     - Wait for next interval                    │
└─────────────────────────────────────────────────┘
```

### Example Messages

The Telegram monitor can understand natural language messages:

✅ **Will update status:**
- "Block 55 washer 4 is done!" → `55W4` to `available`
- "57W3 not working, do not use" → `57W3` to `outOfOrder`
- "Someone left clothes in 59D2" → `59D2` to `pendingUnload`
- "I paid for 55W7 but haven't started yet" → `55W7` to `paidFor`
- "Using dryer 3 in block 57" → `57D3` to `inUse`

❌ **Will be ignored:**
- "Does anyone have detergent?"
- "What's the wifi password?"
- General chat messages without machine references

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env.local with your credentials
cp .env.example .env.local
nano .env.local

# 3. Terminal 1: Start Flask API
python src/app.py

# 4. Terminal 2: Start Telegram Monitor (after API is running)
python telegram_monitor.py
```

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
curl -X POST http://localhost:8000/api/machines/initialize

# Get all machines
curl http://localhost:8000/api/machines

# Update machine status
curl -X PUT http://localhost:8000/api/machines/W1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "inUse", "user": "john", "remaining_time_seconds": 1800}'

# Get available machines
curl http://localhost:8000/api/machines?status=available
```

## Machine Status Types

- `available` - Machine is ready to use
- `paidFor` - Payment received, waiting to start
- `inUse` - Currently running
- `pendingUnload` - Finished, waiting for pickup
- `outOfOrder` - Not working
