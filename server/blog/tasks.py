from celery import shared_task
import logging
import asyncio
from prefect.deployments import run_deployment

logger = logging.getLogger('celery')

SERVER_PREFECT = "http://localhost:4200"

async def run_prefect_deployement(flow_name:str, parameters:dict):
    """
    Run a deployement on prefect
    :param flow_name:
    :param parameters:
    :return:
    """
    return await run_deployment(
            name=flow_name,
            parameters=parameters,
            timeout=0,
        )

@shared_task
def create_dataset(flow_name:str, parameters: dict):
    logger.info(f"Launch flow {flow_name} with parameters: {parameters}")
    flow = asyncio.run(run_prefect_deployement(flow_name, parameters))
    return flow
