import logging

from prefect import task
from prefect.tasks import task_input_hash
from prefect.logging import get_run_logger
from ..utils.request import fetch

@task(task_run_name="Download-{name}", cache_key_fn=task_input_hash)
async def download_from_url(url: str, name: str):
    logger = get_run_logger()
    logger.info(f"Downloading {url}")
    rep = await fetch(url)
    return rep.content
