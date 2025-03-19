import httpx
async def fetch(url: str):
    async with httpx.AsyncClient() as client:
        return await client.get(url)