import logging
import fitz
import pytesseract
import pandas as pd
from PIL import Image
from typing import List
from ..models import Image, Table, Paragraph, Formula, Title
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

def extract_pdf_content(pdf_path):
    content = []
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            # Extraction texte par paragraphe
            text_blocks = page.get_text("blocks")
            for block in text_blocks:
                x0, y0, x1, y1, text, block_no, block_type = block
                content.append({
                    "page": page_num,
                    "polygon": [(x0, y0), (x1, y1)],
                    "text": text,
                    "content_type": "paragraphe"
                })

            # Extraction des images
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                img_path = f"image_page_{page_num}_{img_index}.png"
                with open(img_path, "wb") as img_file:
                    img_file.write(image_bytes)

                img_text = pytesseract.image_to_string(Image.open(img_path))
                content.append({
                    "page": page_num,
                    "polygon": [],  # Polygon extraction can be implemented if necessary
                    "text": img_text,
                    "content_type": "image"
                })

    return content