# n8n Workflow

<div align="center">
  <img src="n8n-workflow.png" alt="n8n Workflow" />
</div>

This n8n workflow supports the [SUTD Laundry Telegram bot](https://t.me/stay_up_to_do_laundry_bot) operations.

## Features

- Commands
    - `/status`
        - Returns current state (idle, running, remaining time) for a specific machine.
    - `/use`
        - Mark a machine as in-use (start).
    - `/finish`
        - Mark a machine as released (end).
    - `/report`
        - Flag a machine whose physical state differs from the tracked state; triggers review workflow and notifications.

- Realtime updates
    - Incoming HTTP requests (Webhook node) or third-party integrations (IoT sensors, booking systems) can push machine status changes into the workflow in real time.
    - When a status change is received, the workflow updates the internal state and pushes notifications to Telegram users or groups via the Telegram node.
    - Use the HTTP Request node to call external APIs (e.g., occupancy sensors) and to acknowledge or correct out-of-sync reports.

## Notes on operation
- Ensure Telegram bot credentials (bot token) and destination chat IDs are configured in n8n credentials after importing the workflow.
- Keep machine identifiers consistent between the Telegram commands and any external integrations to avoid mapping errors.
- Implement rate limiting or confirmation steps for destructive actions (e.g., forcibly marking a machine free).

## Self-hosting n8n Workflow
1. Run or open your n8n Editor (default at http://localhost:5678).
2. Click the menu (top-right) → Import → From File.
3. Select the "SUTD Laundry Bot.json" file and import.
4. After import, open the workflow:
     - Provide or connect required credentials (Telegram bot token, any HTTP/API keys).
     - Inspect webhook/trigger nodes and copy any generated webhook URLs if external services must POST to n8n.
5. Save and activate the workflow.

### Self-hosting minimal example (Docker Compose)
- Create a `docker-compose.yml` with the n8n service and a persistent volume:
    - image: `n8nio/n8n:latest`
    - ports: `5678:5678`
    - environment:
        - `N8N_BASIC_AUTH_ACTIVE=true`
        - `N8N_BASIC_AUTH_USER=<user>`
        - `N8N_BASIC_AUTH_PASSWORD=<password>`
        - `GENERIC_TIMEZONE=UTC`
    - volumes:
        - `~/.n8n:/home/node/.n8n`

- Start:
    - docker-compose up -d

- After n8n is running:
    - Open the Editor, import the JSON, set credentials, and activate the workflow.

### Post-import checklist
- Verify Telegram credentials (Bot token + chat permissions).
- Confirm webhook URLs and configure external integrations to POST to those endpoints.
- Test commands (`/status`, `/use`, `/report`) in a private chat before enabling production notifications.
- Enable backups for the workflow and credentials (store the JSON and credentials securely).
