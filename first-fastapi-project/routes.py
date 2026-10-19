from typing import Annotated, Literal
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

router = APIRouter()

fake_items_db = [Item(name="Foo", price=50.0), Item(name="Bar", price=100.0), Item(name="Baz", price=150.0), Item(name="Bazz", price=200.0), Item(name="Gaz", price=250.0), Item(name="Daz", price=300.0)]

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

@router.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@router.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@router.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

@router.get("/filtered-items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query