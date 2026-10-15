# Original statement of the exercise:
# ===================================
# EJERCICIO 5
# -----------
# Desarrolla un script en Python que realice web scraping de una tienda de libros en línea. 
# En este ejercicio, se pide crear un programa que extraiga información sobre libros de la página web "http://books.toscrape.com/". 
# 
# 1.- Utiliza las bibliotecas requests y BeautifulSoup para realizar web scraping de la página principal de "http://books.toscrape.com/". 
# 2.- Extrae el título y el precio de cada libro listado en la página. 
# 
# Para realizarlo tendrás que mirar bien que contiene el Html de la web para saber que contenido extraer. 


# REQUIRES
# ========
# System
# ------
import time
import requests

# Libraries
# ---------
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

# Defines
# -------
from src.config.globals import *

# Helpers functions
# -----------------
from src.helpers import funcs as hlp
  
# ScrapBooksFromPage
# ------------------
# Fetch HTML content from target page and extract book titles and prices.
#
# @param string $pUrl The target URL to scrap book data from.
# @return void
def ScrapBooksFromPage(pUrl: str) -> None:
  hlp.nbsp()
  print(f"+ =========================================================")
  print(f"+ INITIATING WEB SCRAPING FROM: -{pUrl}-")
  print(f"+ ---------------------------------------------------------")
  hlp.LineBreak(1)
  
  # Perform HTTP request to get raw HTML content
  response: requests.Response = requests.get(pUrl)
  
  # Ensure target server responded successfully before parsing
  if 200 != response.status_code: 
    print(f"Error fetching URL: HTTP {response.status_code}")
    print(f"+ ---------------------------------------------------------")
    return

  # Parse raw HTML text using BeautifulSoup html.parser
  soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
  
  # Locate all book container elements in the DOM (<article class="product_pod">)
  bookContainers: ResultSet = soup.find_all("article", class_="product_pod")

  print(f"+ Total books found on page: {len(bookContainers)}")
  print(f"+ ---------------------------------------------------------")
  hlp.nbsp()

  # Iterate through detected book containers to parse title and price attributes
  for book in bookContainers:
    # Extract title from 'title' attribute of anchor inside <h3> to get full unclipped title
    titleTag: Tag = book.find("h3").find("a")
    bookTitle: str = titleTag["title"] if titleTag and "title" in titleTag.attrs else "Title not found"

    # Extract price text from paragraph element with class 'price_color'
    priceTag: Tag = book.find("p", class_="price_color")
    bookPrice: str = priceTag.get_text(strip=True) if priceTag else "Price not found"

    print(f"Book {bookContainers.index(book) + 1}: Title: {bookTitle:<60}   | Price: {bookPrice}")

  # hlp.nbsp(1, "+")
  hlp.nbsp()
  print(f"+ ---------------------------------------------------------")
  print(f"+ WEB SCRAPPING ENDS")
  print(f"+ =========================================================")
    
# EXECUTION ENTRY POINT
# =====================
if __name__ == "__main__":
  ScrapBooksFromPage(TARGET_URL)