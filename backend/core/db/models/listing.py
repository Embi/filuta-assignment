from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.db.models.base import Base
from core.db.models.base import vector, latent_vector


class Listing(Base):
    __tablename__ = "listings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand: Mapped[str]
    name: Mapped[str]
    year: Mapped[int]
    selling_price: Mapped[int]
    km_driven: Mapped[int]
    fuel: Mapped[str]
    seller_type: Mapped[str]
    transmission: Mapped[str]
    owner: Mapped[str]

    features: Mapped[vector]
    latent_features: Mapped[Optional[latent_vector]]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "brand": self.brand,
            "name": self.name,
            "year": self.year,
            "selling_price": self.selling_price,
            "km_driven": self.km_driven,
            "fuel": self.fuel,
            "seller_type": self.seller_type,
            "transmission": self.transmission,
            "owner": self.owner,
        }
