# FTC Events API Docs: https://ftc-events.firstinspires.org/api-docs/index.html

import asyncio
import base64
import os
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
import httpx

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
_ = load_dotenv(dotenv_path=ENV_PATH)

USERNAME = os.environ.get('FTC_EVENTS_API_USERNAME')
API_KEY = os.environ.get('FTC_EVENTS_API_KEY')
BASE_URL = 'https://ftc-api.firstinspires.org/v2.0/'

TournamentLevel = Literal['qual', 'playoff']

if USERNAME is None:
    raise RuntimeError('Invalid FTC Events API username')

if API_KEY is None:
    raise RuntimeError('Invalid FTC Events API key')

TOKEN = base64.b64encode(f'{USERNAME}:{API_KEY}'.encode()).decode()

_client: httpx.AsyncClient | None = None

headers = {
    'Authorization': f'Basic {TOKEN}',
    'Accept': 'application/json'
}


# Advancement API
async def get_event_advancement(
    season: int,
    eventCode: str,
    excludeSkipped: bool | None = None
) -> Any:
    """The event advancement endpoint returns details about teams advancing from a particular event in a particular season.

    Args:
        - season: Numeric year of the event from which the event advancement is requested. Must be 4 digits > 2022
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the advancement results are requested. Must be at least 3 characters.
        - excludeSkipped: `excludeSkipped=true` to exclude skipped advancement slots. Slots are skipped if no team meets the criteria, the team has already advanced, the team declined, or the team was ineligible.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Advancement/paths/~1v2.0~1{season}~1advancement~1{eventCode}/get
    """
    return await _make_api_call(
        f'{season}/advancement/{eventCode}',
        {
            'excludeSkipped': excludeSkipped
        }
    )


async def get_event_advancement_points(
    season: int,
    eventCode: str
) -> Any:
    """The event advancement points endpoint  returns the advancement points earned by each team at an event.

    Args:
        - season: Numeric year of the event from which the event advancement points are requested. Must be 4 digits > 2024
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the advancement points are requested. Must be at least 3 characters.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Advancement/paths/~1v2.0~1{season}~1advancement~1{eventCode}~1points/get
    """
    return await _make_api_call(
        f'{season}/advancement/{eventCode}/points'
    )


async def get_advancement_source(
    season: int,
    eventCode: str,
    includeDeclines: bool | None = None
) -> Any:
    """The advancement source API returns details about where teams advanced to a specified event from.

    Args:
        - season: Numeric year of the event from which the advancement is requested. Must be 4 digits >= 2022
        - eventCode: Case insensitive alphanumeric eventCode of the event for which teams advanced to. Must be at least 3 characters.
        - includeDeclines: Default: `false`. `includeDeclines=true` to include teams that declined their advancement slot to this event.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Advancement/paths/~1v2.0~1{season}~1advancement~1{eventCode}~1source/get
    """
    return await _make_api_call(
        f'{season}/advancement/{eventCode}/source',
        {
            'includeDeclines': includeDeclines
        }
    )


async def get_regional_championship_advancement(
    season: int
) -> Any:
    """The regional advancement API returns details about the Regional Championship allocations for FIRST Championship and Premier Events. Only valid for DECODE and later seasons (2025-2026 and beyond).

    Args:
        - season: Numeric year of the kickoff year for the season requested. Must be 4 digits >= 2025

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Advancement/paths/~1v2.0~1{season}~1advancement/get
    """
    return await _make_api_call(
        f'{season}/advancement'
    )


# Leagues API
async def get_league_listings(
    season: int,
    regionCode: str | None = None,
    leagueCode: str | None = None
) -> Any:
    """The league listings API returns all FTC leagues in a particular season. You can specify a `regionCode` to filter to leagues within a particular region. To filter to a specific league, supply both a `regionCode` and a `leagueCode`. The returned objects have a `parentLeagueCode` field, which indicates the league is a child league if not null and provides the code of the parent league. The `regionCode` of the parent league will always match the child.

    Args:
        - season: Numeric year from which the league listings are requested. Must be 4 digits
        - regionCode: Case-sensitive alphanumeric `regionCode` of a region to filter for.
        - leagueCode: Case-sensitive alphanumeric `leagueCode` of the league within the specified region to query.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Leagues/paths/~1v2.0~1{season}~1leagues/get
    """
    return await _make_api_call(
        f'{season}/leagues',
        {
            'regionCode': regionCode,
            'leagueCode': leagueCode
        }
    )


async def get_league_membership(
    season: int,
    regionCode: str,
    leagueCode: str
) -> Any:
    """The league membership API returns the list of team numbers for the teams that are members of a particular league. Leagues are specified by a `regionCode` in combination with a `leagueCode`.

    Args:
        - season: Numeric year. Must be 4 digits
        - regionCode: Case sensitive alphanumeric `regionCode` of the region the league belongs to.
        - leagueCode: Case sensitive alphanumeric `leagueCode` of the league.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Leagues/paths/~1v2.0~1{season}~1leagues~1members~1{regionCode}~1{leagueCode}/get
    """
    return await _make_api_call(
        f'{season}/leagues/members/{regionCode}/{leagueCode}'
    )


async def get_league_ranking(
    season: int,
    regionCode: str,
    leagueCode: str
) -> Any:
    """The league rankings API returns team ranking detail from a particular league in a particular season. League rankings are only the cumulative rankings from League Meets - they do not include performance at the League Tournament. To get League Tournament Rankings, use the Event Rankings endpoint.

    Args:
        - season: Numeric year. Must be 4 digits
        - regionCode: Case sensitive alphanumeric `regionCode` of the region the league belongs to.
        - leagueCode: Case sensitive alphanumeric `leagueCode` of the league.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Leagues/paths/~1v2.0~1{season}~1leagues~1rankings~1{regionCode}~1{leagueCode}/get
    """
    return await _make_api_call(
        f'{season}/leagues/rankings/{regionCode}/{leagueCode}'
    )


# General API
async def get_api_index() -> Any:
    """Root level call with no parameters.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/General/paths/~1v2.0/get
    """
    return await _make_api_call(
        ''
    )


# Season Data API
async def get_season_summary(
    season: int
) -> Any:
    """The season summary API returns a high level glance of a particular FTC season.

    Args:
        - season: Numeric year of the event from which the season summary is requested. Must be 4 digits.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Season-Data/paths/~1v2.0~1{season}/get
    """
    return await _make_api_call(
        f'{season}'
    )


async def get_event_listings(
    season: int,
    eventCode: str | None = None,
    teamNumber: int | None = None
) -> Any:
    """The event listings API returns all FTC official regional events in a particular season. You can specify an eventCode if you would only like data about one specific event. If you specify an `eventCode` you cannot specify any other optional parameters. Alternately, you can specify a `teamNumber` to retrieve only the listings of events being attended by the particular team. If you specify a `teamNumber` you cannot specify an `eventCode`.

    The response for event listings contains a special field called divisionCode. For example, the FIRST Championship contains two Divisions. As an example of a response, the event listings for a Division will have a divisionCode that matches the FIRST Championship event code (as they are divisions of that event). This allows you to see the full structure of events, and how they relate to each other.

    Args:
        - season: Numeric year from which the event listings are requested. Must be 4 digits
        - eventCode: Case insensitive alphanumeric `eventCode` of the event about which details are requested.
        - teamNumber: Numeric `teamNumber` of the team from which the attending event listings are requested.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Season-Data/paths/~1v2.0~1{season}~1events/get
    """
    return await _make_api_call(
        f'{season}/events',
        {
            'eventCode': eventCode,
            'teamNumber': teamNumber
        }
    )


async def get_team_listings(
    season: int,
    teamNumber: int | None = None,
    eventCode: str | None = None,
    state: str | None = None,
    excludeNonCompeting: bool | None = None,
    page: int | None = None
) -> Any:
    """The team listings API returns all FTC official teams in a particular season. If specified, the `teamNumber` parameter will return only one result with the details of the requested `teamNumber`. Alternately, the `eventCode` parameter allows sorting of the team list to only those teams attending a particular event in the particular season. If you specify a `teamNumber` parameter, you cannot additionally specify an `eventCode` and/or state in the same request, or you will receive an HTTP 501. If you specify the `state` parameter, it should be the full legal name of the US state or international state/prov, such as New Hampshire or Ontario. Values on this endpoint are "pass through" values from the TIMS registration system. As such, if the team does not specify a value for a field, it may be presented in the API as null.

    Args:
        - season: Numeric year from which the team listings are requested. Must be 4 digits.
        - teamNumber: Numeric `teamNumber` of the team about which information is requested. Must be 1 to 5 digits.
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which details are requested.
        - state: Full legal name of the US state or international state/prov.
        - excludeNonCompeting: Exclude teams set as NON_COMPETING. This is only valid if an `eventCode` is provided.
        - page: Numeric page of results to return.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Season-Data/paths/~1v2.0~1{season}~1teams/get
    """
    return await _make_api_call(
        f'{season}/teams',
        {
            'teamNumber': teamNumber,
            'eventCode': eventCode,
            'state': state,
            'excludeNonCompeting': excludeNonCompeting,
            'page': page
        }
    )


# Schedule API
async def get_hybrid_schedule(
    season: int,
    eventCode: str,
    tournamentLevel: TournamentLevel,
    start: int | None = None,
    end: int | None = None
) -> Any:
    """The schedule API returns the match schedule for the desired tournament level of a particular event in a particular season in the hybrid format. When a match has been played, the match result related details will be filled. When a match has not yet happened, match result related fields will be null. All parameters, except start and end, are required for the hybrid schedule.

    Args:
        - season: Numeric year of the event from which the hybrid schedule is requested. Must be 4 digits
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the hybrid schedule is requested. Must be at least 3 characters.
        - tournamentLevel: Required tournamentLevel of desired score details.
        - start: `start` match number for subset of results to return (inclusive).
        - end: `end` match number for subset of results to return (inclusive).

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Schedule/paths/~1v2.0~1{season}~1schedule~1{eventCode}~1{tournamentLevel}~1hybrid/get
    """
    return await _make_api_call(
        f'{season}/schedule/{eventCode}/{tournamentLevel}/hybrid',
        {
            'start': start,
            'end': end
        }
    )


async def get_event_schedule(
    season: int,
    eventCode: str,
    tournamentLevel: TournamentLevel | None = None,
    teamNumber: int | None = None,
    start: int | None = None,
    end: int | None = None
) -> Any:
    """The schedule API returns the match schedule for the desired tournament level of a particular event in a particular season. You must also specify a `tournamentLevel` from which to return the results. Alternately, you can specify a `teamNumber` to filter the results to only those in which a particular team is participating. There is no validation that the `teamNumber` you request is actually competing at the event, if they are not, the response will be empty. You can also specify the parameters together, but cannot make a request without at least one of the two.

    Args:
        - season: Numeric year of the event from which the schedule is requested. Must be 4 digits
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the schedule are requested. Must be at least 3 characters.
        - tournamentLevel: Required `tournamentLevel` of desired score details.
        - teamNumber: `teamNumber` to search for within the schedule. Only returns matches in which the requested team participated.
        - start: `start` match number for subset of results to return (inclusive).
        - end: `end` match number for subset of results to return (inclusive).

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Schedule/paths/~1v2.0~1{season}~1schedule~1{eventCode}/get
    """
    return await _make_api_call(
        f'{season}/schedule/{eventCode}',
        {
            'tournamentLevel': tournamentLevel,
            'teamNumber': teamNumber,
            'start': start,
            'end': end
        }
    )


# Rankings API
async def get_event_rankings(
    season: int,
    eventCode: str,
    teamNumber: int | None = None,
    top: int | None = None
) -> Any:
    """The rankings API returns team ranking detail from a particular event in a particular season. Optionally, the `top` parameter can be added to the query string to request a subset of the rankings based on the highest ranked teams at the time of the request. Alternately, you can specify the `teamNumber` parameter to retrieve the ranking on one specific team. You cannot specify both a `top` and `teamNumber` in the same call.

    Args:
        - season: Numeric year of the event from which the rankings are requested. Must be 4 digits
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the rankings are requested. Must be at least 3 characters.
        - teamNumber: Team number of the team whose ranking is requested.
        - top: Number of requested `top` ranked teams to return in result.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Rankings/paths/~1v2.0~1{season}~1rankings~1{eventCode}/get
    """
    return await _make_api_call(
        f'{season}/rankings/{eventCode}',
        {
            'teamNumber': teamNumber,
            'top': top
        }
    )


# Alliance Selection API
async def get_event_alliances(
    season: int,
    eventCode: str
) -> Any:
    """The alliances API returns details about alliance selection at a particular event in a particular season.

    Args:
        - season: Numeric year of the event from which the event alliances are requested. Must be 4 digits.
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the alliance selection results are requested. Must be at least 3 characters.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Alliance-Selection/paths/~1v2.0~1{season}~1alliances~1{eventCode}/get
    """
    return await _make_api_call(
        f'{season}/alliances/{eventCode}'
    )


async def get_alliance_selection_details(
    season: int,
    eventCode: str
) -> Any:
    """This returns the in-order details of each step through the alliance selection process for a particular event.

    Args:
        - season: Numeric year of the event from which the event alliances are requested. Must be 4 digits.
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the alliance selection results are requested. Must be at least 3 characters.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Alliance-Selection/paths/~1v2.0~1{season}~1alliances~1{eventCode}~1selection/get
    """
    return await _make_api_call(
        f'{season}/alliances/{eventCode}/selection'
    )


# Match Results API
async def get_event_match_results(
    season: int,
    eventCode: str,
    tournamentLevel: TournamentLevel | None = None,
    teamNumber: int | None = None,
    matchNumber: int | None = None,
    start: int | None = None,
    end: int | None = None
) -> Any:
    """The match results API returns the match results for all matches of a particular event in a particular season. Match results are only available once a match has been played, retrieving info about future matches requires the event schedule API. You cannot receive data about a match that is in progress. You can, however, request the Hybrid Schedule if you would like data about upcoming and played matches at the same time.

    If you specify the `matchNumber`, `start` and/or `end` optional parameters, you must also specify a `tournamentLevel`. If you specify the `teamNumber` parameter, you cannot specify a `matchNumber` parameter. If you specify the `matchNumber`, you cannot define a `start` or `end`.

    Note: If you specify `start`, and it is higher than the maximum match number at the event, you will not receive any match results in the response. The same is true in reverse for the `end` parameter.

    Args:
        - season: Numeric year of the event from which the match results are requested. Must be 4 digits.
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the results are requested. Must be at least 3 characters.
        - tournamentLevel: Required `tournamentLevel` of desired score details.
        - teamNumber: `teamNumber` to search for within the results. Only returns match results in which the requested team was a participant.
        - matchNumber: specific single `matchNumber` of result.
        - start: `start` match number for subset of results to return.
        - end: `end` match number for subset of results to return (inclusive).

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Match-Results/paths/~1v2.0~1{season}~1matches~1{eventCode}/get
    """
    return await _make_api_call(
        f'{season}/matches/{eventCode}',
        {
            'tournamentLevel': tournamentLevel,
            'teamNumber': teamNumber,
            'matchNumber': matchNumber,
            'start': start,
            'end': end
        }
    )


async def get_score_details(
    season: int,
    eventCode: str,
    tournamentLevel: TournamentLevel,
    teamNumber: int | None = None,
    matchNumber: int | None = None,
    start: int | None = None,
    end: int | None = None
) -> Any:
    """The score details API returns the score detail for all matches of a particular event in a particular season and a particular tournament level. Score details are only available once a match has been played, retrieving info about future matches requires the event schedule API. You cannot receive data about a match that is in progress.

    Args:
        - season: Numeric year of the event from which the match results are requested. Must be 4 digits.
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the details are requested. Must be at least 3 characters.
        - tournamentLevel: Required `tournamentLevel` of desired score details.
        - teamNumber: `teamNumber` to search for within the results. Only returns details in which the requested team was a participant.
        - matchNumber: Specific single `matchNumber` of result.
        - start: `start` match number for subset of results to return (inclusive).
        - end: `end` match number for subset of results to return (inclusive).

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Match-Results/paths/~1v2.0~1{season}~1scores~1{eventCode}~1{tournamentLevel}/get
    """
    return await _make_api_call(
        f'{season}/scores/{eventCode}/{tournamentLevel}',
        {
            'teamNumber': teamNumber,
            'matchNumber': matchNumber,
            'start': start,
            'end': end
        }
    )


# Awards API
async def get_award_listings(
    season: int
) -> Any:
    """The award listings API returns a listing of the various awards that can be distributed in the requested season. This is especially useful in order to avoid having to use the name field of the event awards API to know which award was won. Instead the awardId field can be matched between the two APIs.

    Args:
        - season: Numeric year of the event from which the award listings are requested. Must be 4 digits

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Awards/paths/~1v2.0~1{season}~1awards~1list/get
    """
    return await _make_api_call(
        f'{season}/awards/list'
    )


async def get_team_awards(
    season: int,
    teamNumber: int,
    eventCode: str | None = None
) -> Any:
    """The event awards API returns details about awards presented at a particular event in a particular season. Return values may contain either `teamNumber` or person values, and if the winner was a person, and that person is from a team, the `teamNumber` value might be set with their `teamNumber`. You must specify either an `eventCode` or a `teamNumber` or both. If you specify the `teamNumber` parameter, you will receive only awards where the team was listed as the winner, regardless of whether or not the person field is null or empty. If you specify only the `eventCode` field, you will receive all award listings for the requested event. If you specify both, you will receive all awards won by the `teamNumber` at the `eventCode`.

    Args:
        - season: Numeric year of the event from which the award listings are requested. Must be 4 digits
        - teamNumber: `teamNumber` to search for within the results.
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the awards are requested.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Awards/paths/~1v2.0~1{season}~1awards~1{teamNumber}/get
    """
    return await _make_api_call(
        f'{season}/awards/{teamNumber}',
        {
            'eventCode': eventCode
        }
    )


async def get_event_awards(
    season: int,
    eventCode: str,
    teamNumber: int | None = None,
) -> Any:
    """The event awards API returns details about awards presented at a particular event in a particular season. Return values may contain either `teamNumber` or person values, and if the winner was a person, and that person is from a team, the `teamNumber` value might be set with their `teamNumber`. You must specify either an `eventCode` or a `teamNumber` or both. If you specify the `teamNumber` parameter, you will receive only awards where the team was listed as the winner, regardless of whether or not the person field is null or empty. If you specify only the `eventCode` field, you will receive all award listings for the requested event. If you specify both, you will receive all awards won by the `teamNumber` at the `eventCode`.

    Args:
        - season: Numeric year of the event from which the award listings are requested. Must be 4 digits
        - eventCode: Case insensitive alphanumeric `eventCode` of the event from which the awards are requested.
        - teamNumber: `teamNumber` to search for within the results.

    Returns:
        https://ftc-events.firstinspires.org/api-docs/index.html#tag/Awards/paths/~1v2.0~1{season}~1awards~1{eventCode}/get
    """
    return await _make_api_call(
        f'{season}/awards/{eventCode}',
        {
            'teamNumber': teamNumber
        }
    )



# Client functions
def _get_client() -> httpx.AsyncClient:
    """Lazily initialize and return the shared HTTP client."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=headers,
            timeout=10.0
        )
    return _client


async def close_client() -> None:
    """Close the shared HTTP client session."""
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()
        _client = None

# FTC Events API call function
async def _make_api_call(
    endpoint: str,
    params: dict[str, Any] | None = None,
    max_retries: int = 3
) -> Any:
    """This function sends a request to the provided endpoint and returns the response.

    Args:
        - endpoint: The relative path to be added to the end of `BASE_URL`.
        - params: The query params to be added to the url.
        - max_retries: The maximum number of retries to be done in case of rate-limiting.

    Returns:
        - object: The server's response in JSON (dict) format

    Raises:
        Any exception related to a non 200 HTTP status code.
    """
    client = _get_client()
    relative_endpoint = endpoint.lstrip('/')
    filtered_params = {key: value for key, value in (params or {}).items() if value is not None}

    for attempt in range(max_retries):
        response = await client.get(relative_endpoint, params=filtered_params)

        # Handle transient rate limits / server errors
        if response.status_code in (429, 503) and attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)
            continue

        _ = response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    raise RuntimeError('ftc_events.py should not be run as main')
