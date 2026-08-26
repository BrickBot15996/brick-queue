import asyncio

from asyncio.selector_events import os
import httpx

from api_usage.ftc_scout import headers
from classes.event import TrackedEvent
from classes.team import TrackedTeam
from data_access.access_team_data import get_active_event
from dotenv import load_dotenv

from messages.webhook import send_webhook_message


async def main():
    _ = load_dotenv()

    brickbot_webhook_url = os.environ.get('BRICKBOT_WEBHOOK_URL')

    webhook_urls: dict[int, list[str]] = {15996: [brickbot_webhook_url]}

    _ = send_webhook_message(brickbot_webhook_url, 'Merge wrapper-ul')

    untracked_teams: set[int] = {15996}
    tracked_teams: dict[int, TrackedTeam] = {}
    events: dict[str, TrackedEvent] = {}

    # Go through the teams not yet at a tracked event
    updated_untracked_teams = set()
    for team in untracked_teams:
        active_event_code = get_active_event(team)

        # If a team still doesn't have an active event, keep it untracked
        if active_event_code is None:
            updated_untracked_teams.add(team)
        else:
            tracked_team = TrackedTeam(team)
            tracked_teams[team] = tracked_team
            if active_event_code in events:


if __name__ == '__main__':
    asyncio.run(main())
