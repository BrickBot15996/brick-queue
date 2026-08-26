import httpx


async def send_webhook_message(url: str, message: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"content": message}
        )

    return response
