import asyncio
import api_wrappers.ftc_events

async def main():
    output = await api_wrappers.ftc_events.get_team_events(2025, 15996)
    print(output)

if __name__ == "__main__":
    asyncio.run(main())
