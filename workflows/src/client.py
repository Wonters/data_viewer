import httpx
from contextlib import asynccontextmanager

class RestClient:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.api_url = f"http://{self.host}:{self.port}"

    @asynccontextmanager
    async def client(self):
        async with httpx.AsyncClient() as client:
            yield client

    async def get(self, path: str):
        """
        retrieve informations from the API
        :param path:
        :return:
        """
        async with self.client() as client:
            return await client.get(f"{self.api_url}/{path}")

    async def post(self, path:str):
        async with self.client() as client:
            return await client.post(f"{self.api_url}/{path}")
