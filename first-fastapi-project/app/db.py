from app.schemas.items import ItemRead

# In-memory "database" keyed by item id. Replace with a real DB later.
fake_items_db: dict[int, ItemRead] = {
    1: ItemRead(id=1, name="Foo", price=50.0),
    2: ItemRead(id=2, name="Bar", price=100.0),
    3: ItemRead(id=3, name="Baz", price=150.0),
    4: ItemRead(id=4, name="Bazz", price=200.0),
    5: ItemRead(id=5, name="Gaz", price=250.0),
    6: ItemRead(id=6, name="Daz", price=300.0),
}
