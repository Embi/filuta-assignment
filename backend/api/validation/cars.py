from pydantic import BaseModel


class ListingDetailResponse(BaseModel):
    brand: str
    name: str
    year: int
    selling_price: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "brand": "Skoda",
                    "name": "Skoda Octavia",
                    "year": 2017,
                    "selling_price": 420000,
                    "km_driven": 50000,
                    "fuel": "Diesel",
                    "seller_type": "Individual",
                    "transmission": "Manual",
                    "owner": "First Owner",
                }
            ]
        }
    }


class ListingShortResponse(BaseModel):
    id: int
    brand: str
    name: str
    selling_price: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 12,
                    "brand": "Skoda",
                    "name": "Skoda Octavia",
                    "selling_price": 420000,
                }
            ]
        }
    }


class ListingSearchResponse(BaseModel):
    listings: list[ListingShortResponse]


class ListingRecommendationResponse(BaseModel):
    recommended: list[ListingShortResponse]
