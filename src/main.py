from scraper import HemnetScraper
from request import HemnetRequest

def scrape():
    scraper = HemnetScraper()
    urls = [
        'https://www.hemnet.se/bostad/example1',
        'https://www.hemnet.se/bostad/example2'
    ]

    all_listings = []
    for url in urls:
        html = scraper.get_page_content(url)
        if html:
            listing_data = scraper.parse_listing(html)
            all_listings.append(listing_data)

    scraper.save_to_csv(all_listings)

def main():
    hemnet = HemnetRequest()
    listings = hemnet.get_listings(location_ids=["18054"], page="1")

    for listing in listings:
        print(listing)

if __name__ == '__main__':
    main()