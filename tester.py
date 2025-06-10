# Import testing libraries
import unittest  # Python's built-in testing framework
from unittest.mock import patch, Mock  # To mock network requests
import scraper  # The scraper module we're testing

class TestBookScraper(unittest.TestCase):
    """
    This test class verifies the behavior of key functions from scraper.py:
    - get_soup()
    - extract_book_info()
    - save_to_csv()
    """

    @patch('scraper.requests.get')
    def test_get_soup_success(self, mock_get):
        """
        Test if get_soup() returns a valid BeautifulSoup object
        when the HTTP request succeeds.
        """
        # Set up a mock response object with dummy HTML content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><head></head><body></body></html>'
        mock_get.return_value = mock_response

        # Call the function and assert the soup is not None
        soup = scraper.get_soup('http://test.com')
        self.assertIsNotNone(soup)

    @patch('scraper.requests.get')
    def test_get_soup_failure(self, mock_get):
        """
        Test if get_soup() returns None when the HTTP request fails.
        """
        # Simulate a request error (like a 404 or connection issue)
        mock_get.side_effect = Exception("404 error")

        # Function should return None gracefully
        soup = scraper.get_soup('http://badurl.com')
        self.assertIsNone(soup)

    def test_extract_book_info_valid(self):
        """
        Test if extract_book_info() correctly parses a valid HTML snippet
        and returns a list of book details.
        """
        # Sample HTML structure for a single book (same as site)
        html = '''
        <article class="product_pod">
            <h3><a title="Test Book" href="test.html"></a></h3>
            <p class="price_color">£20.00</p>
            <p class="star-rating Three"></p>
            <p class="instock availability">In stock</p>
        </article>
        '''
        # Convert HTML string to a BeautifulSoup object
        soup = scraper.BeautifulSoup(html, 'html.parser')
        book = soup.find('article')

        # Call the extraction function
        data = scraper.extract_book_info(book)

        # Assert expected values in the returned list
        self.assertIsInstance(data, list)
        self.assertEqual(data[0], "Test Book")          # Title
        self.assertEqual(data[1], "£20.00")             # Price
        self.assertIn("In stock", data[2])              # Availability
        self.assertEqual(data[3], "Three")              # Rating
        self.assertTrue(data[4].endswith("test.html"))  # URL

    def test_extract_book_info_missing(self):
        """
        Test if extract_book_info() handles missing fields
        (e.g., empty HTML structure) and returns None.
        """
        # HTML with missing title, price, etc.
        html = '<article class="product_pod"></article>'
        soup = scraper.BeautifulSoup(html, 'html.parser')
        book = soup.find('article')

        # Should handle gracefully and return None
        data = scraper.extract_book_info(book)
        self.assertIsNone(data)

    def test_save_to_csv_format(self):
        """
        Test if save_to_csv() writes the correct header and data to a file.
        """
        # Test data in list format (same as returned by extract_book_info)
        test_data = [[
            'Sample',
            '£10.50',
            'In stock',
            'Four',
            'http://example.com/book1'
        ]]
        test_filename = 'test_books_data.csv'

        # Call the function to save the test data
        scraper.save_to_csv(test_data, filename=test_filename)

        # Open the CSV and verify it starts with expected headers
        with open(test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertTrue(lines[0].startswith('Title,Price'))

# Entry point for running the test file directly
if __name__ == '__main__':
    unittest.main()  # Runs all test cases
