import asyncio
import os

from dotenv.main import load_dotenv

from messages.webhook import send_webhook_message


async def main():
    _ = load_dotenv()

    brickbot_webhook_url = os.environ.get('BRICKBOT_WEBHOOK_URL')

    if brickbot_webhook_url is None:
        raise ValueError('BRICKBOT_WEBHOOK_URL not found in .env.')

    _ = await send_webhook_message(brickbot_webhook_url, 'The wrapper also works')

if __name__ == '__main__':
    asyncio.run(main())
