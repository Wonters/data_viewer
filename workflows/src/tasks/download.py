import logging

from prefect import task
from prefect.tasks import task_input_hash
import httpx
from ..settings import PARENT_LOGGER
logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")

async def get(url:str):
    async with httpx.AsyncClient() as client:
        return await client.get(url)


@task(task_run_name="Download-{name}", cache_key_fn=task_input_hash)
async def download_from_url(url:str, name:str):
    rep = await get(url)
    return rep.content