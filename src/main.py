from src.client import HemnetClient


def main():
    hemnet_client = HemnetClient()
    listings = hemnet_client.get_listings(location_ids=["18054"], page="1")

    for listing in listings:
        print(listing)


if __name__ == "__main__":
    main()
