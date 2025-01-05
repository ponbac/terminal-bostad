from client import HemnetClient

SUNDSVALL_LOCATION_ID = "18054"


def main():
    hemnet_client = HemnetClient()
    listings = hemnet_client.get_listings(
        location_ids=[SUNDSVALL_LOCATION_ID], page="1"
    )

    for listing in listings:
        print(listing)


if __name__ == "__main__":
    main()
