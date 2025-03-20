import httpx
from httpx import Response

class RestClient:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.api_url = f"http://{self.host}:{self.port}"
        self.client = httpx.AsyncClient()

    async def get(self, path: str):
        """
        retrieve informations from the API
        :param path:
        :return:
        """
        return await self.client.get(f"{self.api_url}/{path}")

    async def post(self, path: str, data: dict):
        return await self.client.post(f"{self.api_url}/{path}", json=data)

    async def put(self, path: str, data) -> Response:
        return await self.client.put(f"{self.api_url}/{path}", json=data)

    async def patch(self,data:dict, path: str="", link:str = "") -> Response:
        if link:
            response = await self.client.patch(link, json=data)
        else:
            response = await self.client.patch(f"{self.api_url}/{path}", json=data)
        return response

    async def close(self):
        """
        Close the HTTP client session.
        """
        await self.client.aclose()

    async def __aenter__(self):
        """
        Permet l'utilisation avec `async with RestClient(...) as client`
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Fermeture automatique du client HTTP après usage.
        """
        await self.close()