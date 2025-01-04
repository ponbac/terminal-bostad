from typing import List, Optional
from pydantic import BaseModel, Field


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
