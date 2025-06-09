import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
BASE_SITE = "http://books.toscrape.com/"
HEADERS = ["Title", "Price", "Availability", "Rating", "Product URL"]
OUTPUT_FILE = "books_data.csv"

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"
        return BeautifulSoup(response.content, "html.parser")  # Use .content to preserve encoding
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def extract_rating(book):
    rating_tag = book.select_one(".star-rating")
    if rating_tag:
        for cls in rating_tag["class"]:
            if cls != "star-rating":
                return cls  # e.g., "Three", "Five"
    return "Unknown"

def extract_book_info(book):
    try:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()#.replace("Â", "")  
        availability = book.select_one(".availability").text.strip()
        rating = extract_rating(book)
        relative_url = book.h3.a["href"]
        product_url = urljoin(BASE_SITE + "catalogue/", relative_url)
        return [title, price, availability, rating, product_url]
    except Exception as e:
        print("Error reading book info. Skipping...", e)
        return None

def scrape_books():
    all_books = []
    for page_num in range(1, 51):  # 50 pages total
        print(f"Scraping page {page_num}...")
        soup = get_soup(BASE_URL.format(page_num))
        if soup is None:
            continue

        books = soup.select("article.product_pod")
        for book in books:
            data = extract_book_info(book)
            if data:
                all_books.append(data)

        time.sleep(1)  # Be polite with requests

    print(f"Scraping done! Total books collected: {len(all_books)}")
    return all_books

def save_to_csv(data, filename):
    try:
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
            writer.writerows(data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

if __name__ == "__main__":
    books_data = scrape_books()
    save_to_csv(books_data, OUTPUT_FILE)
