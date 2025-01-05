from typing import List
import requests

from models import ListingCard, HemnetListingsResponse


class HemnetClient:
    """Handles requests to Hemnet's API"""

    BASE_URL = "https://www.hemnet.se/_next/data/ZbTIGtigbip8_BxHWbd_z/bostader.json"

    def __init__(self):
        self.headers = {
            "accept": "*/*",
            "accept-language": "sv-SE,sv;q=0.5",
            "cookie": "force-light-mode=true; hn_uc_consent={}; hn_exp_kpis=366; hn_exp_noi=655; hn_exp_bau=698; hn_exp_copc=667; hn_exp_prd=640; hn_exp_nhc=798; __cfruid=cfc84fa0bbd11dc60cb72bb426ffc133c9909235-1735994010; CF_AppSession=n95f4e1a3f7fd2f56",
            "priority": "u=1, i",
            "referer": "https://www.hemnet.se/bostader",
            "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-nextjs-data": "1",
        }

    def get_listings(
        self, location_ids: list[str], page: str = "1"
    ) -> List[ListingCard]:
        """
        Fetch listings from Hemnet and return a list of ListingCard objects

        Args:
            location_ids: List of location IDs to search in
            page: Page number to fetch

        Returns:
            List of ListingCard objects containing the listing data
        """
        params = {
            "item_types[]": "bostadsratt",
            "location_ids[]": location_ids,
            "page": page,
        }

        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        response.raise_for_status()

        data = HemnetListingsResponse(**response.json())
        apollo_state = data.pageProps.apollo_state

        listings = []
        for key, value in apollo_state.model_dump().items():
            if key.startswith("ListingCard:"):
                listings.append(ListingCard(**value))

        return listings
