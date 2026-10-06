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
import time
import requests
from pathlib import Path

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

# HELPERS FUNCTIONS
# =================
def LineBreak(pHowMany: int = 1):
  for i in range(0, pHowMany):
    print(f"+ ")

def SectionBreak():
  LineBreak(1)
  print(f"+ ---------------------------------------------------------")
  LineBreak(1)
  
# CONSTANTS
# =========
TARGET_URL: str = "http://books.toscrape.com/"

# HELPERS FUNCTIONS
# =================
def LineBreak(pHowMany: int = 1) -> None:
  for i in range(0, pHowMany): print("+ ")

def SectionBreak() -> None:
  LineBreak(1)
  print("+ ---------------------------------------------------------")
  LineBreak(1)

# CUSTOM FUNCTIONS
# ================
#
# ScrapBooksFromPage
# ------------------
# Fetch HTML content from target page and extract book titles and prices.
#
# @param string $pUrl The target URL to scrap book data from.
# @return void
def ScrapBooksFromPage(pUrl: str) -> None:
  # Perform HTTP request to obtain raw HTML content
  response: requests.Response = requests.get(pUrl)
  
  # Ensure target server responded successfully before parsing
  if response.status_code != 200: print(f"Error fetching URL: HTTP {response.status_code}"); return

  # Parse raw HTML text using BeautifulSoup html.parser
  soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
  
  # Locate all book container elements in the DOM (<article class="product_pod">)
  bookContainers: ResultSet = soup.find_all("article", class_="product_pod")

  print(f"+ =========================================================")
  print(f"+ WEB SCRAPING RESULTS: -{pUrl}-")
  print(f"+ Total books found on page: {len(bookContainers)}")
  print(f"+ ---------------------------------------------------------")
  LineBreak(1)

  # Iterate through detected book containers to parse title and price attributes
  for book in bookContainers:
    # Extract title from 'title' attribute of anchor inside <h3> to get full unclipped title
    titleTag: Tag = book.find("h3").find("a")
    bookTitle: str = titleTag["title"] if titleTag and "title" in titleTag.attrs else "Title not found"

    # Extract price text from paragraph element with class 'price_color'
    priceTag: Tag = book.find("p", class_="price_color")
    bookPrice: str = priceTag.get_text(strip=True) if priceTag else "Price not found"

    print(f"Title: {bookTitle:<60} | Price: {bookPrice}")

  SectionBreak()

# EXECUTION ENTRY POINT
# =====================
if __name__ == "__main__":
  ScrapBooksFromPage(TARGET_URL)