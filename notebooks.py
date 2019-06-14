import openpyxl
import requests
from bs4 import BeautifulSoup
from openpyxl.utils.cell import get_column_letter
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


def getSpecs(url: str, session: requests.Session) -> tuple:
    '''
    Scrapes the spec sheet of the notebook in key, value pairs
    '''
    try:
        with session.get(url) as spec_sheet:
            spec_cells = BeautifulSoup(spec_sheet.text, "html.parser").find("div", {"class": "urunOzellik"}).findAll(
                "td", {"class": "gridAlternateDefault gridAlternateUrunOzellik"})
            content = []
            for cell in spec_cells:
                properties = {}
                properties["name"] = cell.find("div").text.strip()
                for pair in cell.findAll("tr"):
                    k = escapeTUR(pair.findAll("td")[
                                  0].text[:-6].strip().lower())
                    v = escapeTUR(pair.findAll("td")[
                                  1].text[:-6].strip().lower())
                    properties[k] = v
                content.append(properties)
    except Exception as ex:
        print(ex)
    try:
        CPU = content[0]["i̇slemci teknolojisi"] + \
            "-" + content[0]["i̇slemci numarasi"]
        size = content[1]["ekran boyu"]
        resolution = content[1]["cozunurluk (piksel)"]
        storage = str(content[2]["disk kapasitesi"]) + \
            " " + str(content[2]["disk turu"])
        os = content[0]["i̇sletim sistemi"]
        return (CPU, size, resolution, storage, os, content)
    except:
        return None

if __name__ == '__main__':
    # XSLX Sheet
    workbook = openpyxl.load_workbook('template.xlsx')
    out_sheet = workbook[workbook.sheetnames[0]]

    # Requests Library Config
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    base_url = "http://www.vatanbilgisayar.com"

    index = 0
    try:
        for i in range(1, 9):
            web_url = f"http://www.vatanbilgisayar.com/notebook/?page={i}"
            main_page = session.get(web_url)
            vatan = BeautifulSoup(main_page.text, "html.parser")
            print(
                f"Status code for product list {i} is {main_page.status_code}.")
            notebooks = vatan.findAll("div", {"class": "ems-prd-inner"})
            for notebook in notebooks[:-1]:
                index += 1
                properties = {}  # properties of this notebook
                divs = notebook.findAll("div")

                # home page of the product
                url = base_url + divs[0].a["href"]

                # full name of the product
                manufacturer = " ".join(divs[1].find(
                    "div", {"class": "ems-prd-name"}).text.strip().split(' ')[0])

                # price of the product
                price = string(notebook.find("div", {"class": "ems-prd-price"}).find("span", {
                    "class": "ems-prd-price-selling"}).text.replace(" ", ""))

                spec_url = url + "#urun-ozellikleri"
                try:
                    CPU, size, resolution, storage, os, _ = getSpecs(
                        spec_url, session)
                    properties["name"] = manufacturer
                    properties["url"] = url
                    properties["price"] = price
                    properties["CPU"] = CPU
                    out_sheet.cell(row=i+1, column=1, value=manufacturer)
                    out_sheet.cell(row=i+1, column=2, value=price)
                    out_sheet.cell(row=i+1, column=3, value=CPU)
                    out_sheet.cell(row=i+1, column=4, value=size)
                    out_sheet.cell(row=i+1, column=5, value=resolution)
                    out_sheet.cell(row=i+1, column=6, value=storage)
                    out_sheet.cell(row=i+1, column=7, value=os)
                    out_sheet.cell(row=i+1, column=8, value=url)
                except:
                    continue
            break
        workbook.save('outfile.xlsx')
    except Exception as ex:
        print(f"Error encounterd.\n{ex}")
