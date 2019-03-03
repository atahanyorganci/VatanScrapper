# Web Scrapper for Vatan Bilgisayar
Python application that uses Beautiful Soup 4 for parsing web pages into useful data. VatanScrapper gathers data from from Vatan Computer’s website a famous electronics store in Turkey, such as price and specs of products. Gathered data is placed in notebooks sub folder directory as JSON files, images are placed accordingly into subfolders as well.  

## Tech Stack
- [Beautifoul Soup 4](https://www.crummy.com/software/BeautifulSoup/), used for web scrapipng, gathering data from [Vatan Bilgisayar](https://www.vatanbilgisayar.com/).

## How to Install

- Make sure you are running Python 3.7.0 or higher and have pip, pipenv packages installed.
- Run following commands from the shell.

```shell
$ pipenv shell #create virtual enviroment
$ pipenv install #install dependencies
$ python notebooks.py #run the virtual enviroment
```