import logging
import requests
import shutil
import json
from bs4 import BeautifulSoup as soup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



def string(raw):
    '''
    Replaces the whitespaces with under scores, all lowercase letters
    '''
    return raw.strip().lower().replace(" ", "_")


def escapeDOS(string):
    '''
    Escapes the literal that are not allowed to be file names in DOS file systems
    '''
    out = string[:]
    if "\\" in string:
        out = out.replace('\\', "_")
    if "/" in string:
        out = out.replace('/', "_")
    if ":" in string:
        out = out.replace(':', "_")
    if '*' in string:
        out = out.replace('*', "_")
    if '?' in string:
        out = out.replace('?', "_")
    if '"' in string:
        out = out.replace('"', "_")
    if '<' in string:
        out = out.replace('<', "_")
    if '>' in string:
        out = out.replace('>', "_")
    if '|' in string:
        out = out.replace('|', "_")
    return out


def escapeTUR(string):
    '''
    Escapes the literals that are exclusively Turkish
    '''
    out = string[:]
    if "ö" in string:
        out = out.replace('ğ', "o")
    if "ü" in string:
        out = out.replace('ü', "u")
    if "ş" in string:
        out = out.replace('ş', "s")
    if 'ı' in string:
        out = out.replace('ı', "i")
    if 'ö' in string:
        out = out.replace('ö', "o")
    if 'ç' in string:
        out = out.replace('ç', "c")
    return out


def downloadImage(url, directory, session):
    try:
        with session.get(url, stream=True) as image:
            image_dir = directory + ".jpg"
            with open(image_dir, 'wb') as out:
                image.raw.decode = True
                shutil.copyfileobj(image.raw, out)
    except Exception as ex:
        logging.error("Image download failed. " + str(ex))


def getSpecs(url, session):
    '''
    Scrapes the spec sheet of the notebook in key, value pairs
    '''
    try:
        with session.get(url) as spec_sheet:
            spec_cells = soup(spec_sheet.text, "html.parser").find("div", {"class": "urunOzellik"}).findAll(
                "td", {"class": "gridAlternateDefault gridAlternateUrunOzellik"})
            content = []
            for cell in spec_cells:
                properties = {}
                properties["name"] = cell.find("div").text.strip()
                for pair in cell.findAll("tr"):
                    k = escapeTUR(pair.findAll("td")[0].text[:-6].strip().lower())
                    v = escapeTUR(pair.findAll("td")[1].text[:-6].strip().lower())
                    properties[k] = v
                content.append(properties)
            return content
    except Exception as ex:
        logging.error("Spec sheet parsing failed. " + str(ex))


def main():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    base_url = "http://www.vatanbilgisayar.com"
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    index = 0
    try:
        for i in range(1, 9):
            web_url = "http://www.vatanbilgisayar.com/notebook/?page={}".format(
                i)
            main_page = session.get(web_url)
            vatan = soup(main_page.text, "html.parser")
            logging.debug("Status code for product list {} is {}.".format(i, main_page.status_code))
            notebooks = vatan.findAll("div", {"class": "ems-prd-inner"})
            for notebook in notebooks[:-1]:
                index += 1
                properties = {}  # properties of this notebook
                # image name will be saved in form
                code = "notebook-" + str(index).rjust(3, "0")
                divs = notebook.findAll("div")
                url = base_url + divs[0].a["href"]  # home page of the product
                # full name of the product
                name = string(divs[1].find(
                    "div", {"class": "ems-prd-name"}).text)
                price = string(notebook.find("div", {"class": "ems-prd-price"}).find("span", {
                    "class": "ems-prd-price-selling"}).text.replace(" ", ""))  # price of the product
                image_url = divs[0].a.img["data-original"]  # icon image url
                image_dir = "images\\" + code
                spec_url = url + "#urun-ozellikleri"
                spec_sheet = getSpecs(spec_url, session)
                properties["name"] = name
                properties["url"] = url
                properties["price"] = price
                properties["image_dir"] = "images\\" + code + ".jpg"
                properties["specs"] = spec_sheet
                downloadImage(image_url, image_dir, session)
                with open("notebooks\\" + code + ".json", "w", encoding="utf-8") as out:
                    json.dump(properties, out, ensure_ascii=False, indent="\t")
                    logging.info("{} -- is complete {}.".format(name, url))
    except Exception as ex:
        logging.critical("Error encounterd. " + str(ex))


if __name__ == '__main__':
    logging.debug("main() Started.")
    main()
    logging.debug("main() Ended.")
