"""
Telegram Message Monitor for Laundry Machine Status Updates

This script monitors a Telegram chat for messages about laundry machine statuses
and automatically updates the machine status in the system using OpenAI for
intelligent message parsing.

Workflow:
1. Connect to Telegram using Telethon
2. Periodically fetch new messages from the specified chat
3. Filter messages for those containing block numbers (55, 57, 59) and/or washer/dryer keywords
4. Use OpenAI API to parse the message and determine if it affects machine status
5. Update the corresponding machine status by sending requests to the API endpoint
6. Log all actions and errors for debugging
"""

import asyncio
from datetime import datetime
from dotenv import load_dotenv  # type: ignore
import json
import logging
import os
import re
import requests  # type: ignore

# Telethon imports
from telethon import TelegramClient  # type: ignore
from telethon.tl.types import Message, PeerChannel  # type: ignore

# OpenAI imports
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/telegram_monitor/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv('.env.local')

# Telegram configuration
try:
    API_ID = int(os.getenv('TELEGRAM_API_ID') or "")
except ValueError:
    logger.error("Invalid TELEGRAM_API_ID in .env.local")
    exit(1)
API_HASH = os.getenv('TELEGRAM_API_HASH')
if not API_HASH:
    logger.error("Missing TELEGRAM_API_HASH in .env.local")
    exit(1)
PHONE = os.getenv('TELEGRAM_PHONE')
if not PHONE:
    logger.error("Missing TELEGRAM_PHONE in .env.local")
    exit(1)
PASSWORD = os.getenv('TELEGRAM_PASSWORD')
if not PASSWORD:
    logger.error("Missing TELEGRAM_PASSWORD in .env.local")
    exit(1)

# Telegram chat configuration
try:
    CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID') or "")
except ValueError:
    logger.error("Invalid TELEGRAM_CHAT_ID in .env.local")
    exit(1)
try:
    TOPIC_ID = int(os.getenv('TELEGRAM_TOPIC_ID') or "")
except ValueError:
    logger.error("Invalid TELEGRAM_TOPIC_ID in .env.local")
    exit(1)

# API endpoint configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("Missing OPENAI_API_KEY in .env.local")
    exit(1)

# Monitoring settings
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '30'))

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)


class TelegramMonitor:
    """Monitor Telegram chat for laundry machine status updates"""
    
    def __init__(self):
        """Initialize the Telegram monitor"""

        self.client: TelegramClient | None = None  # type: ignore
        self.last_message_id: int = -1  # type: ignore
        self.is_running = False
        
    async def initialize(self) -> bool:
        """Initialize Telegram client and authenticate"""
        
        try:
            logger.info("Initializing Telegram client...")
            
            # Validate credentials
            if not all([API_ID, API_HASH, PHONE]):
                raise ValueError("Missing Telegram API credentials in .env.local")
            
            # Create Telegram client
            assert isinstance(API_HASH, str)
            self.client = TelegramClient('laundry_monitor_session', API_ID, API_HASH)
            
            # Connect to Telegram
            assert isinstance(PHONE, str)
            assert isinstance(PASSWORD, str)
            await self.client.start(phone=PHONE, password=PASSWORD) # pyright: ignore[reportGeneralTypeIssues]
            logger.info("Successfully connected to Telegram")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Telegram client: {e}")
            return False
    
    def filter_relevant_message(self, message_text: str) -> bool:
        """Filter messages for those containing block numbers (55, 57, 59)
        and/or washer/dryer keywords
        
        Args:
            message_text: The message text to filter
            
        Returns:
            True if the message is relevant, False otherwise
        """

        if not message_text:
            return False
        
        text_lower = message_text.lower()
        
        # Check for block numbers
        has_block = any(block in message_text for block in ['55', '57', '59'])
        
        # Check for washer/dryer keywords
        keywords = ['washer', 'dryer', 'wash', 'dry', 'machine', 'laundry']
        has_keyword = any(keyword in text_lower for keyword in keywords)
        
        return has_block or has_keyword
    
    async def parse_message_with_openai(self, message_text: str) -> dict[str, str]:
        """Use OpenAI API to parse the message and extract machine status information
        
        Args:
            message_text: The message text to parse
            
        Returns:
            Dictionary with machine_id and new_status, or empty dictionary if not relevant
        """
        
        
        logger.info(f"Parsing message with OpenAI: {message_text[:100]}{'...' * (len(message_text) > 100)}")
        
        # Create the prompt for OpenAI
        prompt = f"""
You are analyzing a Telegram message from a hostel laundry room group chat to determine if it reports a status change for a specific washing machine or dryer.

The laundry rooms are in blocks 55, 57, and 59. Each block has:
- Washers numbered W1-W11 (e.g., "55W4" means Block 55, Washer 4)
- Dryers numbered D1-D6 (e.g., "57D3" means Block 57, Dryer 3)

Possible status changes:
- "available": Machine is free/done/clothes removed/ready to use
- "paidFor": Someone paid but hasn't started the machine yet
- "inUse": Machine is currently running
- "pendingUnload": Machine is done but clothes not yet removed
- "outOfOrder": Machine is broken/not working/do not use

Message to analyze:
"{message_text}"

If this message reports a specific machine status change, respond with ONLY a JSON object in this exact format:
{{"machine_id": "55W4", "status": "available", "confidence": "high"}}

Rules:
1. machine_id MUST be in format: <block><type><number> (e.g., "55W4", "57D3", "59W1")
2. status MUST be one of: available, paidFor, inUse, outOfOrder
3. confidence MUST be one of: high, medium, low
4. Only respond if you're at least medium confidence about a specific machine and status
5. If the message doesn't clearly indicate a machine status change, respond with: {{"relevant": false}}

Respond with ONLY the JSON, no other text.
"""
        
        # Initialize response_text variable
        response_text = ""

        try:
            # Call OpenAI API
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a precise JSON parser for laundry machine status updates. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            # Extract the response
            response_text = response.choices[0].message.content  # type: ignore
            if response_text is None:
                error_message = "OpenAI response content is None"
                logger.error(error_message)
                return {"error": error_message}
            logger.info(f"OpenAI response: {response_text}")
            
            # Parse JSON response
            result = json.loads(response_text)
            
            # Check if the message is relevant
            if not result.get('relevant', True):
                error_message = "OpenAI marked message as not relevant"
                logger.info(error_message)
                return {"error": error_message}

            # Validate the response has required fields
            elif 'machine_id' not in result or 'status' not in result:
                error_message = "OpenAI response missing required fields"
                logger.error(error_message)
                return {"error": error_message}

            # Validate machine_id format
            machine_id = result['machine_id']
            if not re.match(r'^(55|57|59)[WD]\d+$', machine_id):
                error_message = f"Invalid machine_id format: {machine_id}"
                logger.error(error_message)
                return {"error": error_message}

            # Validate status
            valid_statuses = ['available', 'paidFor', 'inUse', 'pendingUnload', 'outOfOrder']
            if result['status'] not in valid_statuses:
                error_message = f"Invalid status: {result['status']}"
                logger.error(error_message)
                return {"error": error_message}

            # Check confidence level
            confidence = result.get('confidence', 'medium')
            if confidence == 'low':
                error_message = f"Low confidence parse, skipping: {result}"
                logger.info(error_message)
                return {"error": error_message}

            logger.info(f"Successfully parsed: {result}")
            return result
            
        except json.JSONDecodeError as e:
            error_message = f"Failed to parse OpenAI response as JSON: {e}\nResponse was: {response_text}"
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            error_message = f"Error parsing message with OpenAI: {e}"
            logger.error(error_message)
            return {"error": error_message}

    def update_machine_status(self, machine_id: str, status_str: str, message_text: str, user: str = "") -> bool:
        """
        Update the machine status via API endpoint
        
        Args:
            machine_id: Machine ID (e.g., "55W4")
            status_str: Status string (e.g., "available")
            message_text: Original message text for logging
            user: User who triggered the update (e.g., Telegram username)

        Returns:
            True if update was successful, False otherwise
        """
        
        try:
            # Step 1: Get current machine info from API
            get_url = f"{API_BASE_URL}/api/machines/{machine_id}"
            logger.info(f"Fetching machine info from: {get_url}")
            
            response = requests.get(get_url, timeout=10)
            
            if response.status_code == 404:
                logger.warning(f"Machine {machine_id} not found in API")
                return False
            
            if response.status_code != 200:
                logger.error(f"Failed to get machine {machine_id}: HTTP {response.status_code}")
                return False
            
            machine_data = response.json()
            old_status = machine_data.get('status', 'unknown')
            
            # Step 2: Update machine status via API
            update_url = f"{API_BASE_URL}/api/machines/{machine_id}/status"
            payload = {
                'status': status_str,
                'user': "<unknown>" if not user else f"@{user}" if user != "admin" else user,
            }
            
            logger.info(f"Updating machine status at: {update_url} with payload: {payload}")
            response = requests.put(update_url, json=payload, timeout=10)
            
            if response.status_code != 200:
                logger.error(
                    f"Failed to update machine {machine_id}: HTTP {response.status_code} - {response.text}"
                )
                return False
            
            logger.info(f"Successfully updated {machine_id} status: {old_status} -> {status_str}")
            
            # Step 3: Update telegram message via API
            telegram_url = f"{API_BASE_URL}/api/machines/{machine_id}/telegram"
            telegram_payload = { # pyright: ignore[reportUnknownVariableType]
                'message': message_text[:200],  # Limit message length
                'message_url': None  # URL not available in this context
            }
            
            logger.info(f"Updating telegram message at: {telegram_url}")
            telegram_response = requests.put(telegram_url, json=telegram_payload, timeout=10) # pyright: ignore[reportUnknownArgumentType]
            
            if telegram_response.status_code != 200:
                logger.warning(
                    f"Failed to update telegram message for {machine_id}: HTTP {telegram_response.status_code}"
                )
                # Don't fail the whole update if telegram message update fails
            
            logger.info(
                f"✅ Updated {machine_id} status via API: {old_status} -> {status_str}"
            )
            return True
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while updating machine status for {machine_id}")
            return False
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while updating machine status for {machine_id}. Is the backend running at {API_BASE_URL}?")
            return False
        except Exception as e:
            logger.error(f"Error updating machine status via API: {e}")
            return False
    
    async def process_message(self, message: Message) -> None:
        """Process a single Telegram message
        
        Args:
            message: The Telegram message to process
        """

        logger.info(f"Received message ID {message.id} from Telegram")

        try:
            # Determine if this is a topic message
            # see: https://stackoverflow.com/questions/79157818/how-do-i-get-the-name-of-a-topic-a-message-is-sent-in-with-telethon
            if message.reply_to is None:
                logger.info("Message is not in a forum topic, skipping")
                return
            reply_to = message.reply_to
            if (
                not bool(reply_to.forum_topic)  # type: ignore
                or reply_to.reply_to_msg_id != TOPIC_ID  # type: ignore
            ):
                logger.info("Message is not in Hostel topic, skipping")
                return

            # Get message text
            if not message.message:
                return

            logger.info(f"Processing message: {message.message[:100]}...")

            # Step 1: Filter for relevant messages
            if not self.filter_relevant_message(message.message):
                logger.info("Message not relevant (no block numbers or keywords)")
                return
            
            logger.info("Message passed initial filter")
            
            # Step 2: Parse with OpenAI
            parsed = await self.parse_message_with_openai(message.message)
            if not parsed or 'error' in parsed or not parsed.get('relevant'):
                logger.info("OpenAI determined message has no actionable status change")
                return
            
            # Step 3: Update machine status
            success = self.update_machine_status(
                machine_id=parsed['machine_id'],
                status_str=parsed['status'],
                message_text=message.message
            )
            
            if success:
                logger.info(
                    f"✅ Successfully updated {parsed['machine_id']} to {parsed['status']}"
                )
            else:
                logger.warning(
                    f"❌ Failed to update {parsed['machine_id']} to {parsed['status']}"
                )
                
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
    
    async def check_new_messages(self) -> None:
        """Check for new messages in the Telegram chat"""
        try:
            if not self.client:
                logger.error("Telegram client not initialized")
                return
            
            logger.info(f"Checking for new messages in chat: {CHAT_ID}")

            # Get chat entity
            # assert CHAT_ID is not None
            _dialogs = await self.client.get_dialogs() # pyright: ignore[reportUnknownMemberType]
            try:
                chat = await self.client.get_entity(PeerChannel(CHAT_ID))
            except ValueError:
                logger.error(f"Chat with ID {CHAT_ID} not found among dialogs")
                return

            # Get messages since last check
            messages: list[Message] = []
            async for message in self.client.iter_messages(  # pyright: ignore[reportUnknownVariableType]
                chat, # pyright: ignore[reportArgumentType]
                limit=100,  # max limit: 3000
                min_id=self.last_message_id
            ):
                messages.append(message)  # pyright: ignore[reportUnknownArgumentType]

            logger.info(f"Found {len(messages)} new messages")

            # Process each message
            for message in messages:
                await self.process_message(message)
                self.last_message_id = max(self.last_message_id, message.id)
                
                # Update last message date
                # if message.date:
                #     self.last_message_date = message.date
            
            # if messages:
            #     logger.info(f"Updated last_message_date to {self.last_message_date}")
            if messages:
                logger.info(f"Updated last_message_id to {self.last_message_id}")
            
        except Exception as e:
            logger.error(f"Error checking new messages: {e}", exc_info=True)
    
    async def run(self):
        """Main monitoring loop"""

        logger.info("Starting Telegram monitor...")
        
        # Initialize
        if not await self.initialize():
            logger.error("Failed to initialize Telegram monitor")
            return
        
        self.is_running = True
        logger.info(f"Monitor started. Checking every {CHECK_INTERVAL} seconds...")
        
        # Main loop
        while self.is_running:
            try:
                # Check for new messages
                await self.check_new_messages()
                
                # Wait before next check
                logger.info(f"Waiting {CHECK_INTERVAL} seconds before next check...")
                await asyncio.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                logger.info(f"Waiting {CHECK_INTERVAL} seconds before retrying...")
                await asyncio.sleep(CHECK_INTERVAL)
    
    async def stop(self):
        """Stop the monitor and cleanup"""
        logger.info("Stopping Telegram monitor...")
        self.is_running = False
        
        if self.client:
            await self.client.disconnect() # pyright: ignore[reportGeneralTypeIssues]
            logger.info("Telegram client disconnected")


async def main():
    """Main entry point"""
    
    # Create and run monitor
    monitor = TelegramMonitor()
    
    try:
        await monitor.run()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        await monitor.stop()


if __name__ == '__main__':
    # Run the async main function
    asyncio.run(main())
