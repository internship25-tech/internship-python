import unittest
from unittest.mock import patch, Mock
import scraper

class TestBookScraper(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_get_soup_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<html><head></head><body></body></html>'
        mock_get.return_value = mock_response

        soup = scraper.get_soup('http://test.com')
        self.assertIsNotNone(soup)

    @patch('scraper.requests.get')
    def test_get_soup_failure(self, mock_get):
        mock_get.side_effect = Exception("404 error")
        soup = scraper.get_soup('http://badurl.com')
        self.assertIsNone(soup)

    def test_extract_book_info_valid(self):
        html = '''
        <article class="product_pod">
            <h3><a title="Test Book" href="test.html"></a></h3>
            <p class="price_color">£20.00</p>
            <p class="star-rating Three"></p>
            <p class="instock availability">In stock</p>
        </article>
        '''
        soup = scraper.BeautifulSoup(html, 'html.parser')
        book = soup.find('article')
        data = scraper.extract_book_info(book)

        self.assertIsInstance(data, list)
        self.assertEqual(data[0], "Test Book")          # Title
        self.assertEqual(data[1], "£20.00")             # Price
        self.assertIn("In stock", data[2])              # Availability
        self.assertEqual(data[3], "Three")              # Rating
        self.assertTrue(data[4].endswith("test.html"))  # URL

    def test_extract_book_info_missing(self):
        html = '<article class="product_pod"></article>'
        soup = scraper.BeautifulSoup(html, 'html.parser')
        book = soup.find('article')
        data = scraper.extract_book_info(book)
        self.assertIsNone(data)

    def test_save_to_csv_format(self):
        test_data = [[
            'Sample',
            '£10.50',
            'In stock',
            'Four',
            'http://example.com/book1'
        ]]
        test_filename = 'test_books_data.csv'
        scraper.save_to_csv(test_data, filename=test_filename)

        with open(test_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertTrue(lines[0].startswith('Title,Price'))

if __name__ == '__main__':
    unittest.main()
