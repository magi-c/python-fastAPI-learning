from typing import Literal

from pydantic import BaseModel, Field, computed_field


class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ItemCreate(ItemBase):
    """What the client sends when creating or updating an item (no id)."""


class ItemRead(ItemBase):
    """What the API returns: includes the id and the computed price with tax."""

    id: int

    @computed_field
    @property
    def price_with_tax(self) -> float:
        return self.price + (self.tax or 0)


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
