from typing_extensions import Annotated

from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import DeclarativeBase
import numpy as np

FEATURES = 50
LATENT_FEATURES = 100
# Annotated[np.array, <vetor-size>, <min-value>, <max-value>]
vector = Annotated[np.array, FEATURES, 0, 10]
latent_vector = Annotated[np.array, LATENT_FEATURES, 0, 10]


class Base(DeclarativeBase):
    type_annotation_map = {
        vector: Vector(FEATURES),
        latent_vector: Vector(LATENT_FEATURES),
    }
