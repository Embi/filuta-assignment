from pydantic import BaseModel


class ListingDetailResponse(BaseModel):
    brand: str = "Skoda"
    name: str = "Skoda Octavia"
    year: int = 2017
    selling_price: int = 420000
    km_driven: int = 50000
    fuel: str = "Diesel"
    seller_type: str = "Individual"
    transmission: str = "Manual"
    owner: str = "First Owner"


class ListingShortResponse(BaseModel):
    id: int = 12
    brand: str = "Skoda"
    name: str = "Skoda Octavia"
    selling_price: int = 420000


class ListingSearchResponse(BaseModel):
    listings: list[ListingShortResponse]


class ListingRecommendationResponse(BaseModel):
    recommended: list[ListingShortResponse]
