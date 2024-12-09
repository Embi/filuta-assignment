#!/usr/bin/env python3
import pandas
from sqlalchemy import text
from pathlib import Path
import numpy as np

from core.db.models.user import User
from core.db.models.listing import Listing
from core.db.models.base import Base
from core.db.session import get_session, get_engine


def initialize_db():
    with get_session() as session:
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

    Base.metadata.create_all(get_engine())


def populate_with_random_users(count: int):
    def generate_user(user_id: int):
        return {
            "email": f"john{user_id}@example.com",
            "first_name": f"John{user_id}",
            "surname": "Doe",
            "preference": np.random.randint(10, size=50),
        }

    with get_session() as session:
        for i in range(count):
            user = generate_user(i)
            session.add(User(**user))
        session.commit()


def populate_with_listings(listings_path: Path):
    def add_brand(listing):
        """Extract brand from car full name."""
        if "Land" in listing["name"]:
            listing["brand"] = "Land Rover"
        else:
            listing["brand"] = listing["name"].split()[0]
        return listing

    def add_features(listing):
        # TODO extract real features
        # Currently placeholder random features
        listing["features"] = np.random.randint(10, size=50)
        return listing

    df_listings = pandas.read_csv(listings_path)
    listings = df_listings.to_dict(orient="records")
    # add brands
    listings = map(add_brand, listings)
    # add features
    listings = map(add_features, listings)

    with get_session() as session:
        for item in listings:
            session.add(Listing(**item))
        session.commit()


if __name__ == "__main__":
    initialize_db()
    populate_with_random_users(50)
    populate_with_listings(Path("assets/car_data.csv"))
