import logging
from logging import FileHandler
import asyncio
from rich.logging import RichHandler
from prefect import flow
from prefect.logging import get_run_logger
from src.client import RestClient
from src.tasks import *
from src.settings import PARENT_LOGGER
from src.utils.concurence import run_concurrent_tasks
from src.settings import BACKEND_HOST, BACKEND_PORT

logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")

console_handler = RichHandler()

for name in logging.Logger.manager.loggerDict.keys():
    if any(word in name for word in ["src"]):
        logger = logging.getLogger(name)
        logger.handlers.append(FileHandler("prefect.log"))
        logger.handlers.append(console_handler)
        logger.propagate = False
        logger.setLevel(logging.INFO)


@flow(
    log_prints=True,
    name="Extract Dataset",
    # task_runner=DaskTaskRunner(**CLUSTER_OPTS),
)
async def extract_datasets(urls: list):
    logger = get_run_logger()
    client = RestClient(BACKEND_HOST, BACKEND_PORT)
    rep = await client.get("blog/api/datasets/")
    datasets = rep.json()

    errors, data = await run_concurrent_tasks(
        [
            download_from_url_task(url=dataset["url"], name=dataset["name"])
            for dataset in datasets
        ]
    )
    errors, data = await run_concurrent_tasks(
        [
            parse_content_task(content=content, name=dataset["name"])
            for content, dataset in zip(data, datasets)
        ]
    )
    await asyncio.gather(*[d.save() for d in data])
    await asyncio.gather(*[upload_api_task(metadata=d.model_dump(),
                                           name=d.name,
                                           link=ds['link'])
                           for d, ds in zip(data, datasets)])


if __name__ == "__main__":
    asyncio.run(extract_datasets())
