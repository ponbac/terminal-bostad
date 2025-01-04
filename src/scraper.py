import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class HemnetScraper:
    def __init__(self):
        # Headers to make our requests look like they're coming from a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_page_content(self, url):
        """Fetch the HTML content of a page"""
        try:
            # Add a delay to be respectful to the website
            time.sleep(2)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def parse_listing(self, html):
        """Parse a single listing page"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Initialize dictionary to store listing data
        listing_data: dict[str, str | None] = {
            'title': None,
            'price': None,
            'address': None,
            'size': None
        }
        
        # Define mapping of data fields to their HTML selectors
        selectors = {
            'title': ('h1', 'listing-title'),
            'price': ('div', 'price-tag'),
            'address': ('div', 'address'),
            'size': ('div', 'size')
        }
        
        try:
            for field, (tag, class_name) in selectors.items():
                element = soup.find(tag, {'class': class_name})
                listing_data[field] = element.text.strip() if element else None
        except AttributeError as e:
            print(f"Error parsing listing: {e}")
        
        return listing_data

    def save_to_csv(self, data, filename='hemnet_listings.csv'):
        """Save the scraped data to a CSV file"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")