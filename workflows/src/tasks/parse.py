import logging
from bs4 import BeautifulSoup
import pandas as pd
from prefect.tasks import task_input_hash
from prefect import task
from prefect.logging import get_run_logger
from typing import List
from ..models import Dataset, Image, Table, Paragraph, Formula, Title
from ..settings import PARENT_LOGGER

logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")

def extract_math_formulas(soup) -> List[Formula]:
    """
    Retrieve mathematical formulas
    :param soup:
    :return:
    """
    formulas = []
    for math in soup.find_all("math"):
        formulas.append(Formula(content=math.get_text()))
    # Les formules LaTeX sont souvent stockées sous cette forme
    for img in soup.find_all("img"):
        if "math" in img["src"]:
            formulas.append(Formula(url=img["src"]))
    return formulas


def extract_paragraphs_by_title(soup) -> List[Paragraph]:
    """
    Extrait les paragraphes en les indexant par leurs titres
    :param soup:
    :return:
    """
    data = []
    current_title = ""
    for index, tag in enumerate(soup.find_all(["h2", "h3", "h4", "p"])):
        if tag.name in ["h2", "h3", "h4"]:
            current_title = Title(text=tag.get_text(strip=True), index=index)
        elif tag.name == "p":
            text = "".join(tag.find_all(text=True, recursive=False))
            paragraph = Paragraph(title=current_title, content=text)
            data.append(paragraph)
    return data


def extract_tables_with_titles(soup):
    """
    Extrait les tableaux avec leurs titres associés
    :param soup:
    :return:
    """
    tables = []
    for table in soup.find_all("table", {"class": "wikitable"}):

        title = table.find_previous(["h2", "h3", "h4"]).get_text(strip=True)
        df = pd.read_html(str(table))[0]  # Convertit en DataFrame
        tables.append(Table.from_dataframe(title=title, df=df))
    return tables


def extract_images(soup):
    """
    Extrait les images d'une page Wikipédia
    :param soup:
    :return:
    """
    images = []
    for figure in soup.find_all("figure"):
        img_url = "https:" + figure.find("img")["src"]
        description = figure.find("figcaption").get_text()
        # Stocke l'URL de l'image et sa descriptionimg_url
        # On téléchargera les images dans un second temps
        images.append(Image(url=img_url, description=description))
    return images


@task(task_run_name="Parse-{name}")#cache_key_fn=task_input_hash)
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
