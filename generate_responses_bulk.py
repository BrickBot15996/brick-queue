import asyncio
import json

from api_usage.ftc_events import (
    get_advancement_source,
    get_alliance_selection_details,
    get_api_index,
    get_award_listings,
    get_event_advancement,
    get_event_advancement_points,
    get_event_alliances,
    get_event_awards,
    get_event_listings,
    get_event_match_results,
    get_event_rankings,
    get_event_schedule,
    get_hybrid_schedule,
    get_league_listings,
    get_league_membership,
    get_league_ranking,
    get_regional_championship_advancement,
    get_score_details,
    get_season_summary,
    get_team_awards,
    get_team_listings,
)
from api_usage.ftc_scout import get_team_stats

SEASON = 2025
EVENT_CODE = 'FTCCMP1GOOD'
EXCLUDE_SKIPPED = False
INCLUDE_DECLINES = False
REGION_CODE = 'RO'
LEAGUE_CODE = 'E'
TEAM_NUMBER = 15996
STATE='VN'
EXCLUDE_NON_COMPETING = False
PAGE = 1
TOURNAMENT_LEVEL = 'qual'
START = 0
END = 999
TOP = 999
MATCH_NUMBER = 7

async def main():
    data = await get_event_advancement(SEASON, "ROCMP", EXCLUDE_SKIPPED)
    with open('response_examples/ftc_events_api/get_event_advancement.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_advancement_points(SEASON, "ROCMP")
    with open('response_examples/ftc_events_api/get_event_advancement_points.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_advancement_source(SEASON, "ROCMP", INCLUDE_DECLINES)
    with open('response_examples/ftc_events_api/get_advancement_source.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_regional_championship_advancement(SEASON)
    with open('response_examples/ftc_events_api/get_regional_championship_advancement.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_league_listings(SEASON, REGION_CODE)
    with open('response_examples/ftc_events_api/get_league_listings.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_league_membership(SEASON, REGION_CODE, LEAGUE_CODE)
    with open('response_examples/ftc_events_api/get_league_membership.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_league_ranking(SEASON, REGION_CODE, LEAGUE_CODE)
    with open('response_examples/ftc_events_api/get_league_ranking.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_api_index()
    with open('response_examples/ftc_events_api/get_api_index.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_season_summary(SEASON)
    with open('response_examples/ftc_events_api/get_season_summary.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_listings(SEASON, teamNumber=TEAM_NUMBER)
    with open('response_examples/ftc_events_api/get_event_listings.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_team_listings(SEASON, TEAM_NUMBER)
    with open('response_examples/ftc_events_api/get_team_listings.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_hybrid_schedule(SEASON, EVENT_CODE, TOURNAMENT_LEVEL)
    with open('response_examples/ftc_events_api/get_hybrid_schedule.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_schedule(SEASON, EVENT_CODE, teamNumber=TEAM_NUMBER)
    with open('response_examples/ftc_events_api/get_event_schedule.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_rankings(SEASON, EVENT_CODE)
    with open('response_examples/ftc_events_api/get_event_rankings.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_alliances(SEASON, EVENT_CODE)
    with open('response_examples/ftc_events_api/get_event_alliances.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_alliance_selection_details(SEASON, "ROCMPCND")
    with open('response_examples/ftc_events_api/get_alliance_selection_details.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_match_results(SEASON, EVENT_CODE, teamNumber=TEAM_NUMBER)
    with open('response_examples/ftc_events_api/get_event_match_results.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_score_details(SEASON, EVENT_CODE, 'playoff', matchNumber=14)
    with open('response_examples/ftc_events_api/get_score_details.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_award_listings(SEASON)
    with open('response_examples/ftc_events_api/get_award_listings.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_team_awards(SEASON, TEAM_NUMBER)
    with open('response_examples/ftc_events_api/get_team_awards.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_event_awards(SEASON, EVENT_CODE)
    with open('response_examples/ftc_events_api/get_event_awards.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    data = await get_team_stats(TEAM_NUMBER)
    with open('response_examples/ftc_scout_api/get_team_stats.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
