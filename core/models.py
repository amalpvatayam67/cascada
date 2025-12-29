from typing import List, Literal
from pydantic import BaseModel, Field


EntityType = Literal[
    "external", "user", "service", "machine", "role", "data"
]

RelationshipType = Literal[
    "can_access", "runs_on", "assumes", "trusts", "connected_to"
]


class Entity(BaseModel):
    id: str
    type: EntityType


class Relationship(BaseModel):
    source: str = Field(..., alias="from")
    target: str = Field(..., alias="to")
    type: RelationshipType


class SystemModel(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]
    entry_points: List[str]
    targets: List[str]
