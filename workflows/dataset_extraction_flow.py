import logging
import asyncio
from logging import FileHandler, StreamHandler

from prefect import flow
from src.client import RestClient
from src.tasks.download import download_from_url
from src.tasks.parse import parse_content_task
from src.settings import PARENT_LOGGER

logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")

for name in logging.Logger.manager.loggerDict.keys():
    if any(word in name for word in ["src", "prefect"]):
        logger = logging.getLogger(name)
        logger.handlers.extend([
            FileHandler('prefect.log'),
            StreamHandler()
        ])
        logger.propagate = False
        logger.setLevel(logging.INFO)


@flow(log_prints=True,
    name="Extract Dataset",
    #task_runner=DaskTaskRunner(**CLUSTER_OPTS),
      )
async def extract_datasets():
    client = RestClient("localhost", 8000)
    rep = await client.get("api/blog/")
    datasets = rep.json()
    tasks = [asyncio.create_task(download_from_url(url=dataset["url"],
                                                   name=dataset["name"]))
             for dataset in datasets]

    for task in tasks:
        result = await task
        d = await parse_content_task(result, task.get_name())
        logger.info(d.images)



if __name__ == "__main__":
    asyncio.run(extract_datasets())