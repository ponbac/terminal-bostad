from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import requests
import json


class Coordinates(BaseModel):
    """Represents geographical coordinates"""

    lat: float
    long: float


class HousingForm(BaseModel):
    """Represents the type of housing"""

    symbol: str


class Label(BaseModel):
    """Represents a label on the listing"""

    text: Optional[str]
    identifier: str
    category: str


class ListingCard(BaseModel):
    """Represents a single listing from Hemnet"""

    id: str
    activePackage: str
    askingPrice: str
    brokerAgencyLogo: str
    brokerAgencyName: str
    coordinates: Coordinates
    description: str
    fee: str
    floor: Optional[str]
    housingForm: HousingForm
    labels: List[Label]
    landArea: Optional[str]
    livingAndSupplementalAreas: str
    locationDescription: str
    newConstruction: bool
    projectId: Optional[str]
    publishedAt: str
    recordType: str
    removedBeforeShowing: bool
    rooms: str
    saved: bool
    showings: List[str]
    slug: str
    squareMeterPrice: str
    streetAddress: str
    thumbnails: List[str] = Field(alias='thumbnails({"format":"ITEMGALLERY_CUT"})')
    upcoming: bool

    def __str__(self) -> str:
        floor_text = f", {self.floor}" if self.floor else ""
        showings_text = (
            f"\nVisning: {', '.join(self.showings)}" if self.showings else ""
        )
        features = [
            label.text
            for label in self.labels
            if label.category == "FEATURE" and label.text is not None
        ]
        features_text = f"\nEgenskaper: {', '.join(features)}" if features else ""

        return f"""
🏠 {self.streetAddress}{floor_text}
📍 {self.locationDescription}
💰 {self.askingPrice} ({self.squareMeterPrice})
🏗️  {self.rooms} | {self.livingAndSupplementalAreas}
💸 Avgift: {self.fee}{showings_text}{features_text}

{self.description}

🔗 https://www.hemnet.se/bostad/{self.slug}
"""


class ApolloState(BaseModel):
    """Represents the Apollo state cache data"""

    class Config:
        extra = "allow"  # Allows additional fields not defined in the model


class PageProps(BaseModel):
    """Represents the page props containing Apollo state"""

    apollo_state: ApolloState = Field(alias="__APOLLO_STATE__")

    class Config:
        populate_by_name = True


class HemnetListingsResponse(BaseModel):
    """Root model for the JSON response"""

    pageProps: PageProps

    class Config:
        populate_by_name = True


class HemnetRequest:
    """Handles requests to Hemnet's API"""

    BASE_URL = "https://www.hemnet.se/_next/data/JOwnZSqZ4XsxrYZXuSlZe/bostader.json"

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

        print(json.dumps(apollo_state.model_dump(), indent=4, ensure_ascii=False))

        listings = []
        for key, value in apollo_state.model_dump().items():
            if key.startswith("ListingCard:"):
                listings.append(ListingCard(**value))

        return listings
