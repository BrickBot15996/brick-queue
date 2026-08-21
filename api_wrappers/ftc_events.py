import os
import base64
import httpx
import asyncio
import datetime

from dotenv import load_dotenv
from pathlib import Path
from zoneinfo import ZoneInfo

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
_ = load_dotenv(dotenv_path=ENV_PATH)

USERNAME = os.environ.get("FTC_EVENTS_API_USERNAME")
API_KEY = os.environ.get("FTC_EVENTS_API_KEY")
BASE_URL = "https://ftc-api.firstinspires.org/v2.0"

if USERNAME is None:
    raise RuntimeError("Invalid FTC Events API username")

if API_KEY is None:
    raise RuntimeError("Invalid FTC Events API key")

TOKEN = base64.b64encode(f"{USERNAME}:{API_KEY}".encode()).decode()

headers = {
    "Authorization": f"Basic {TOKEN}",
    "Accept": "application/json"
}

async def get_api_data():
    url=f'{BASE_URL}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            _handle_response_code(response.status_code)
            return response.status_code


async def get_team_data(season: str, team_number: str):
    url = f'{BASE_URL}/{season}/teams?teamNumber={team_number}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            _handle_response_code(response.status_code)
            return response.status_code

async def get_team_events(season: int, team_number: int):
    url = f'{BASE_URL}/{season}/events?teamNumber={team_number}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            _handle_response_code(response.status_code)
            return response.status_code

def _handle_response_code(code: int) -> None:
    date_time = datetime.datetime.now(tz=ZoneInfo("Europe/Bucharest"))

    match code:
        case 304:
            print(f'[{date_time}] HTTP 304 - "Not Modified"')
            pass
        case 400:
            print(f'[{date_time}] HTTP 400 - "Invalid Season Requested"/"Malformed Parameter Format In Request"/"Missing Parameter In Request"/"Invalid API Version Requested"')
            pass
        case 401:
            print(f'[{date_time}] HTTP 401 - "Unauthorized"')
            pass
        case 404:
            print(f'[{date_time}] HTTP 404 - "Invalid Event Requested"')
            pass
        case 500:
            print(f'[{date_time}] HTTP 500 - "Internal Server Error"')
            pass
        case 501:
            print(f'[{date_time}] HTTP 501 - "Request Did Not Match Any Current API Pattern"')
            pass
        case 503:
            print(f'[{date_time}] HTTP 503 - "Service Unavailable"')
            pass
        case _:
            pass

if __name__ == "__main__":
    raise RuntimeError("ftc_events.py should not be run as main")
