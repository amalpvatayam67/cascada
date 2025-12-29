from typing import List
from pydantic import BaseModel, Field, validator


# -----------------------------
# Allowed vocab (ontology)
# -----------------------------
ALLOWED_ENTITY_TYPES = {
    "network",     # internet, vpc, subnet
    "service",     # api, web_app
    "compute",     # vm, worker, machine
    "identity",    # user, service_account
    "data",        # db, storage
    "role",        # iam role
    "external"     # external internet-like entities
}

ALLOWED_RELATION_TYPES = {
    "connected_to",
    "can_access",
    "trusts",
    "assumes",
    "runs_on"
}


# -----------------------------
# Models
# -----------------------------
class Entity(BaseModel):
    id: str
    type: str

    @validator("type")
    def validate_entity_type(cls, v):
        if v not in ALLOWED_ENTITY_TYPES:
            raise ValueError(f"Unknown entity type: {v}")
        return v


class Relationship(BaseModel):
    # JSON uses "from", Python cannot → alias required
    from_: str = Field(..., alias="from")
    to: str
    type: str

    @validator("type")
    def validate_relation_type(cls, v):
        if v not in ALLOWED_RELATION_TYPES:
            raise ValueError(f"Unknown relationship type: {v}")
        return v

    class Config:
        populate_by_name = True


class SystemModel(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]
    entry_points: List[str]
    targets: List[str]

    # -----------------------------
    # Validators
    # -----------------------------
    @validator("entities")
    def validate_unique_entities(cls, entities):
        ids = [e.id for e in entities]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate entity IDs detected")
        return entities

    @validator("relationships")
    def validate_relationship_refs(cls, relationships, values):
        entity_ids = {e.id for e in values.get("entities", [])}
        for r in relationships:
            if r.from_ not in entity_ids:
                raise ValueError(
                    f"Relationship 'from' unknown entity: {r.from_}"
                )
            if r.to not in entity_ids:
                raise ValueError(
                    f"Relationship 'to' unknown entity: {r.to}"
                )
        return relationships

    @validator("entry_points", "targets")
    def validate_refs_exist(cls, refs, values):
        entity_ids = {e.id for e in values.get("entities", [])}
        for ref in refs:
            if ref not in entity_ids:
                raise ValueError(f"Unknown reference: {ref}")
        return refs
