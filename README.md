# internship-python
# 📘 Book Scraper Project

A Python web scraper that extracts book information from [books.toscrape.com](http://books.toscrape.com) and saves it into a structured CSV file. Ideal for data analysis, market research, or practicing web scraping and testing skills.

# Features
- Scrapes 50 pages of book listings
- Extracts:
  -  Title
  -  Price
  -  Availability
  -  Rating
  -  Product URL
- Saves results to `books_data.csv`
- Includes full unit testing (`unittest + mock`)
- Handles missing data and HTTP errors gracefully

---

##  Tech Stack
- **Language**: Python 3
- **Libraries**:
  - `requests` – fetch web pages
  - `BeautifulSoup` – parse HTML
  - `csv` – write to CSV
  - `unittest` – test core logic
  - `unittest.mock` – simulate requests

---

##  Project Structure
book_scrap/
├── scraper.py # Core scraping logic
├── tester.py # Unit tests
├── books_data.csv # Output data (after running the scraper)
├── README.md # Project documentation

INSTALLATION
1. Clone this repository:
 git clone https://github.com/internship25-tech/book_scrap.git
2. Install dependencies:

Detailed explanation of scraper.py
# scraper.py overview

def get_soup(url):
    """Sends a request to a URL and returns BeautifulSoup object. Returns None on error."""

def extract_rating(book):
    """Reads rating class from HTML and returns string like 'One', 'Three', etc."""

def extract_book_info(book):
    """Extracts title, price, availability, rating, and URL from a single book entry."""

def scrape_books():
    """Loops through all 50 pages, collects book info, and returns a list of data."""

def save_to_csv(data, filename):
    """Writes the collected data into a CSV file with headers."""

# Script Entry Point
if __name__ == "__main__":
    books_data = scrape_books()
    save_to_csv(books_data, OUTPUT_FILE)

Detailed explanation of tester.py
# tester.py tests the following:
- test_get_soup_success: Checks valid HTML is returned by get_soup()
- test_get_soup_failure: Simulates a request failure
- test_extract_book_info_valid: Parses valid book HTML
- test_extract_book_info_missing: Handles missing data correctly
- test_save_to_csv_format: Verifies CSV structure is correct

# Flow 
 Objective: Collect structured data from an e-commerce site

User Action: Runs scraper.py

 Process:

Visits each page

Extracts book data

Appends to a list

Writes to a CSV

Output: A clean books_data.csv with book listings




