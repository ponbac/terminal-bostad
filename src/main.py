from typing import Literal
from client import HemnetClient


LOCATIONS: dict[Literal["Sundsvall"], str] = {
    "Sundsvall": "18054",
}


def main():
    hemnet_client = HemnetClient()
    listings = hemnet_client.get_listings(location_ids=[LOCATIONS["Sundsvall"]], page=1)

    for listing in listings:
        print(listing)


if __name__ == "__main__":
    main()
