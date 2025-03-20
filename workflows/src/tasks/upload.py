from prefect import task
from prefect.logging import get_run_logger
from ..client import RestClient
from ..settings import BACKEND_PORT, BACKEND_HOST


@task(task_run_name="upload-api-{name}")  # cache_key_fn=task_input_hash)
async def upload_api_task(metadata, name: str, link: str):
    """
    Upload the metadata on the backend
    :param metadata:
    :param name:
    :return:
    """
    logger = get_run_logger()
    async with RestClient(BACKEND_HOST, BACKEND_PORT) as client:
        await client.patch(link=link, data={'metadata': metadata})
        logger.info(f"Uploading metadata for {name} on {link}")
    return
