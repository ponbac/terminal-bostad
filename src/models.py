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
    activePackage: Optional[str]
    askingPrice: Optional[str]
    brokerAgencyLogo: Optional[str]
    brokerAgencyName: Optional[str]
    coordinates: Coordinates
    description: str
    fee: Optional[str]
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
    rooms: Optional[str]
    saved: bool
    showings: List[str]
    slug: str
    squareMeterPrice: Optional[str]
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


class SaleCard(BaseModel):
    """Represents a sold property listing from Hemnet"""

    id: str
    listingId: str
    slug: str
    streetAddress: str
    soldAt: str
    soldAtLabel: str
    askingPrice: str
    finalPrice: str
    livingArea: str
    locationDescription: str
    fee: Optional[str]
    squareMeterPrice: str
    housingForm: HousingForm
    rooms: str
    landArea: Optional[str]
    priceChange: Optional[str]
    coordinates: Coordinates
    brokerAgencyName: str
    brokerAgencyThumbnail: Optional[str]
    brokerThumbnail: Optional[str]
    brokerName: Optional[str]
    labels: List[Label]
    product: str
    recordType: str

    def to_csv_row(self) -> dict:
        # Helper function to clean price strings
        def clean_price(price_str: str) -> Optional[int]:
            # Debug print
            print(f"Price string: '{price_str}'")
            # Handle missing price
            if price_str == "Prissaknas" or price_str == "Pris saknas":
                return None
            # Remove currency symbol, month indicator, spaces (including non-breaking spaces), and convert to int
            return int(
                price_str.replace("kr", "")
                .replace("/mån", "")
                .replace("\xa0", "")
                .replace(" ", "")
            )

        # Helper function to clean percentage strings
        def clean_percentage(pct_str: str) -> float:
            # Handle ±0 case
            if "±0" in pct_str:
                return 0.0
            return float(pct_str.replace("%", "").replace(",", ".").replace("\xa0", ""))

        # Clean numeric values from currency and units
        asking_price = clean_price(self.askingPrice)
        final_price = clean_price(self.finalPrice)
        living_area = float(self.livingArea.replace("m²", "").replace(",", "."))
        fee = clean_price(self.fee) if self.fee else None
        square_meter_price = clean_price(self.squareMeterPrice.replace("kr/m²", ""))
        price_change = clean_percentage(self.priceChange) if self.priceChange else None

        # Convert labels to string format (e.g., "FEATURE:Balkong;FEATURE:Hiss")
        label_str = ";".join(
            f"{label.category}:{label.text}"
            for label in self.labels
            if label.text is not None
        )

        return {
            "id": self.id,
            "listingId": self.listingId,
            "streetAddress": self.streetAddress,
            "soldAt": self.soldAt,
            "soldAtLabel": self.soldAtLabel,
            "askingPrice": asking_price,
            "finalPrice": final_price,
            "livingArea": living_area,
            "locationDescription": self.locationDescription,
            "fee": fee,
            "squareMeterPrice": square_meter_price,
            "rooms": self.rooms,
            "priceChange": price_change,
            "brokerAgencyName": self.brokerAgencyName,
            "brokerName": self.brokerName,
            "labels": label_str,
            "url": f"https://www.hemnet.se/salda/{self.slug}",
        }

    def __str__(self) -> str:
        broker_text = f"\nMäklare: {self.brokerName}" if self.brokerName else ""
        features = [
            label.text
            for label in self.labels
            if label.category == "FEATURE" and label.text is not None
        ]
        features_text = f"\nEgenskaper: {', '.join(features)}" if features else ""

        return f"""
🏠 {self.streetAddress}
📍 {self.locationDescription}
💰 {self.finalPrice} (Utgångspris: {self.askingPrice})
📊 Prisförändring: {self.priceChange}
🏗️  {self.rooms} | {self.livingArea}
💸 Avgift: {self.fee}{broker_text}{features_text}
📅 {self.soldAtLabel}

🔗 https://www.hemnet.se/salda/{self.slug}
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
