from request import HemnetRequest


def main():
    hemnet = HemnetRequest()
    listings = hemnet.get_listings(location_ids=["18054"], page="1")

    for listing in listings:
        print(listing)


if __name__ == "__main__":
    main()
