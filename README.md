# VatanScrapper

Python script that scrapes useful data from [Vatan Bilgisayar](https://www.vatanbilgisayar.com/)'s web page and stores them in Excel workbook. Data is gathered from the website with a combination of packages [Requests](https://3.python-requests.org/) for making HTTP requests, and [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) for processing returned mark-up from the server. Then, gathered data is stored in Excel workbook, this process is handled by [openpyxl](https://openpyxl.readthedocs.io/en/stable/) module. All of the dependencies can be installed with [pipenv](https://docs.pipenv.org/en/latest/) manager.

## Tech Stack

- [Requests](https://3.python-requests.org/) for making HTTP GET request to the servers, and fetch websites.
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/), used for web scrapping, gathering data from [Vatan Bilgisayar](https://www.vatanbilgisayar.com/).
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) for handling Excel workbooks.

## How to Install

- Make sure you are running Python 3.7.0 or higher and have pip, pipenv packages installed.
- Run following commands from the shell.

```shell
$ pipenv shell #create virtual enviroment
$ pipenv install #install dependencies
$ python notebooks.py #run the virtual enviroment
```