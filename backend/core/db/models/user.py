from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.db.models.base import Base
from core.db.models.base import vector, latent_vector


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str]
    first_name: Mapped[str]
    surname: Mapped[str]
    preference: Mapped[vector]
    latent_preference: Mapped[Optional[latent_vector]]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "surname": self.surname,
            "preference": self.preference,
            "latent_preference": self.latent_preference,
        }
