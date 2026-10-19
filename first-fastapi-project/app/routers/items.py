from typing import Annotated

from fastapi import APIRouter, Query

from app.db import fake_items_db
from app.schemas.items import FilterParams, ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/")
async def read_items(skip: int = 0, limit: int = 10) -> list[ItemRead]:
    return list(fake_items_db.values())[skip : skip + limit]


# Must be declared before "/{item_id}", otherwise "filtered" would be
# captured as an item_id.
@router.get("/filtered/")
async def read_filtered_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query


@router.get("/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@router.post("/")
async def create_item(item: ItemCreate) -> ItemRead:
    new_id = max(fake_items_db, default=0) + 1
    created = ItemRead(id=new_id, **item.model_dump())
    fake_items_db[new_id] = created
    return created


@router.put("/{item_id}")
async def update_item(item_id: int, item: ItemCreate) -> ItemRead:
    updated = ItemRead(id=item_id, **item.model_dump())
    fake_items_db[item_id] = updated
    return updated
