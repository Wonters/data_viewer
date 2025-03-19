import asyncio
from typing import Tuple
from .clean import clean_gather_results

async def run_concurrent_tasks(tasks)-> Tuple[list, list]:
    results = await asyncio.gather(*tasks)
    return clean_gather_results(results)