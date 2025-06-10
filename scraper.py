# Import required modules
import requests  # To make HTTP requests
from bs4 import BeautifulSoup  # To parse HTML content
import csv  # To write data to a CSV file
import time  # To add delay between requests
from urllib.parse import urljoin  # To construct full URLs from relative paths

# Constants
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"  # URL template for paginated book pages
BASE_SITE = "http://books.toscrape.com/"  # Base site URL used to form full product URLs
HEADERS = ["Title", "Price", "Availability", "Rating", "Product URL"]  # Column headers for the CSV
OUTPUT_FILE = "books_data.csv"  # Output file name

# Function to fetch and parse a web page using BeautifulSoup
def get_soup(url):
    try:
        # Make an HTTP GET request to the given URL
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes (e.g., 404, 500)
        response.encoding = "utf-8"  # Ensure proper encoding for parsing
        # Parse the page content using BeautifulSoup and return the soup object
        return BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        # Print error and return None if request fails
        print(f"Error fetching URL {url}: {e}")
        return None

# Function to extract star rating as text (e.g., "Three", "Five") from a book HTML element
def extract_rating(book):
    rating_tag = book.select_one(".star-rating")  # Select the rating element
    if rating_tag:
        # The rating is stored as a class name (e.g., "star-rating Three")
        for cls in rating_tag["class"]:
            if cls != "star-rating":  # Skip the fixed class
                return cls  # Return the dynamic class representing rating
    return "Unknown"  # Return fallback if rating not found

# Function to extract all required information from a single book's HTML
def extract_book_info(book):
    try:
        # Extract the title from the <a> tag inside <h3>
        title = book.h3.a["title"]

        # Extract the price (as text) from the appropriate class
        price = book.select_one(".price_color").text.strip()  # Includes £ symbol

        # Extract the availability status
        availability = book.select_one(".availability").text.strip()

        # Get the rating as a string (e.g., "Three")
        rating = extract_rating(book)

        # Extract relative URL and convert it to absolute URL using urljoin
        relative_url = book.h3.a["href"]
        product_url = urljoin(BASE_SITE + "catalogue/", relative_url)

        # Return all collected data as a list (to match expected format)
        return [title, price, availability, rating, product_url]
    except Exception as e:
        # If any part of the extraction fails, print the error and skip the book
        print("Error reading book info. Skipping...", e)
        return None

# Main scraping function to loop through all pages and collect book data
def scrape_books():
    all_books = []  # List to store data from all pages

    # Loop through all 50 pages (1 to 50)
    for page_num in range(1, 51):
        print(f"Scraping page {page_num}...")  # Feedback in terminal

        # Format the URL with the current page number and get its content
        soup = get_soup(BASE_URL.format(page_num))
        if soup is None:
            continue  # Skip to next page if page failed to load

        # Find all book containers on the page
        books = soup.select("article.product_pod")
        
        # Loop through each book and extract data
        for book in books:
            data = extract_book_info(book)
            if data:
                all_books.append(data)  # Add to master list if data is valid

        time.sleep(1)  # Delay to be polite and avoid overloading the server

    print(f"Scraping done! Total books collected: {len(all_books)}")  # Final feedback
    return all_books  # Return the full list of book data

# Function to write collected book data into a CSV file
def save_to_csv(data, filename):
    try:
        # Open the file in write mode and create a CSV writer
        with open(filename, mode="w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(HEADERS)

            # Write each row of book data
            writer.writerows(data)

        print(f"Data saved to {filename}")  # Confirm save
    except Exception as e:
        # Handle and report file I/O errors
        print(f"Error writing to CSV: {e}")

# Script entry point: this block runs only if the script is executed directly
if __name__ == "__main__":
    books_data = scrape_books()  # Start scraping
    save_to_csv(books_data, OUTPUT_FILE)  # Save results to CSV
