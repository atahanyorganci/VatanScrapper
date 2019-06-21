<h1 align="center">VatanScrapper</h1>

<div align="center">

  [![GitHub Issues](https://img.shields.io/badge/python-3.7.3-brightgreen.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)

</div>

<p align="center">
    Python script that scrapes useful data from Vatan Bilgisayar's web page and stores them in Excel workbook.
</p>

<hr>

## Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## About <a name = "about"></a>

Python script that scrapes useful data from [Vatan Bilgisayar](https://www.vatanbilgisayar.com/)'s web page and stores them in Excel workbook. Data is gathered from the website with a combination of packages [Requests](https://3.python-requests.org/) for making HTTP requests, and [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) for processing returned mark-up from the server. Then, gathered data is stored in Excel workbook, this process is handled by [openpyxl](https://openpyxl.readthedocs.io/en/stable/) module. All of the dependencies can be installed with [pipenv](https://docs.pipenv.org/en/latest/) manager.

## Getting Started <a name = "getting_started"></a>
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Make sure you are running Python 3.7.0 or higher and have pip, pipenv packages installed.
- Run following commands from the shell.

### How to Install

```shell
$ pipenv shell #create virtual enviroment
$ pipenv install #install dependencies
$ python notebooks.py #run the virtual enviroment
```

## Usage <a name="usage"></a>
Application can be run by following commands.
```shell
$ pipenv shell # activate virtual env if you haven't
$ python notebooks.py #run the virtual enviroment
```

## Built Using <a name = "built_using"></a>

- [Requests](https://3.python-requests.org/) for making HTTP GET request to the servers, and fetch websites.
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/), used for web scrapping, gathering data from [Vatan Bilgisayar](https://www.vatanbilgisayar.com/).
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) for handling Excel workbooks.

## Authors <a name = "authors"></a>
- [@atahanyorganci](https://github.com/atahanyorganci) - Idea & Implementation
