# FTC Scout API Docs: https://ftcscout.org/api

from typing import Any

import httpx


BASE_URL="https://api.ftcscout.org/rest/v1/"

headers = {
    'Accept': 'application/json'
}

_client: httpx.AsyncClient | None = None

async def get_team_stats(
    teamNumber: int
) -> Any:
    return await _make_api_call(
        f'teams/{teamNumber}/quick-stats'
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
) -> Any:
    """This function sends a request to the provided endpoint and returns the response.

    Args:
        - endpoint: The relative path to be added to the end of `BASE_URL`.
        - params: The query params to be added to the url.

    Returns:
        - object: The server's response in JSON (dict) format

    Raises:
        Any exception related to a non 200 HTTP status code.
    """
    client = _get_client()
    relative_endpoint = endpoint.lstrip('/')
    filtered_params = {key: value for key, value in (params or {}).items() if value is not None}

    response = await client.get(relative_endpoint, params=filtered_params)

    _ = response.raise_for_status()
    return response.json()
