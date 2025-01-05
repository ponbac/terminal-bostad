import os
from client import HemnetClient
from time import sleep
from random import uniform
from typing import Optional, TypeVar, Callable, List
import pandas as pd
from datetime import datetime

from models import ListingCard, SaleCard

T = TypeVar("T", ListingCard, SaleCard)

LOCATIONS: list[str] = [
    "474882",
    "474876",
    "944607",
    "474880",
    "947428",
    "474881",
    "474879",
]


def get_paginated_listings(
    fetch_func: Callable[[list[str], int], List[T]],
    start_page: int = 1,
    max_pages: Optional[int] = None,
) -> List[T]:
    """
    Generic function to fetch paginated listings and remove duplicates.

    Args:
        fetch_func: Function that takes location_ids and page number and returns a list of listings

    Returns:
        List of unique listings
    """
    listings = []
    page = start_page
    while True if max_pages is None else page <= max_pages:
        try:
            page_listings = fetch_func(LOCATIONS, page)
            print(
                f"Found {len(page_listings)} listings on page {page}, total listings: {len(listings)}"
            )
            if not page_listings:
                break
            new_listings = [
                listing
                for listing in page_listings
                if listing.id not in [listing.id for listing in listings]
            ]
            listings.extend(new_listings)
            if len(new_listings) == 0:
                break
            page += 1
            # Sleep between 1-5 seconds before next request
            sleep(uniform(1, 5))
        except Exception as e:
            print(f"Error: {e}")
            break

    return listings


def save_listings_to_csv(listings: List[dict], filename_prefix: str) -> None:
    """
    Save listings to a CSV file with timestamp in filename.

    Args:
        listings: List of dictionaries containing listing data
        filename_prefix: Prefix for the CSV filename (e.g., 'for_sale' or 'sold')
    """
    if not listings:
        print(f"No {filename_prefix} listings to save")
        return

    # Create DataFrame directly from the dictionaries
    df = pd.DataFrame(listings)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{filename_prefix}_{timestamp}.csv"

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Save to CSV
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Saved {len(listings)} {filename_prefix} listings to {filename}")


def main():
    hemnet_client = HemnetClient()

    # Get for sale listings
    # for_sale_listings = get_paginated_listings(hemnet_client.get_listings)
    # print(f"Found total {len(for_sale_listings)} for sale listings")
    # save_listings_to_csv(for_sale_listings, "for_sale")

    # Get sold listings
    sold_listings = get_paginated_listings(
        hemnet_client.get_sold_listings, start_page=26, max_pages=None
    )
    print(f"Found total {len(sold_listings)} sold listings")
    save_listings_to_csv([listing.to_csv_row() for listing in sold_listings], "sold")


if __name__ == "__main__":
    main()
