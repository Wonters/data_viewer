import logging
from bs4 import BeautifulSoup
from prefect import task
from prefect.logging import get_run_logger
from ..models import Dataset
from ..settings import PARENT_LOGGER
from ..utils.parse import (extract_images,
                           extract_math_formulas,
                           extract_paragraphs_by_title,
                           extract_tables_with_titles)
logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")


@task(task_run_name="Parse-{name}")  # cache_key_fn=task_input_hash)
async def parse_content_task(content, name: str):
    """

    :param content:
    :param name:
    :return:
    """
    logger = get_run_logger()
    parser = BeautifulSoup(content, "html.parser")
    formulas = extract_math_formulas(parser)
    images = extract_images(parser)
    tables = extract_tables_with_titles(parser)
    paragraphs = extract_paragraphs_by_title(parser)
    logger.info(f"{name} parsed")
    return Dataset(
        name=name,
        formulas=formulas,
        tables=tables,
        images=images,
        paragraphs=paragraphs,
    )
