from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_items_pagination():
    response = client.get("/items/", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Bar", "Baz"]


def test_create_item_returns_id_and_price_with_tax():
    response = client.post("/items/", json={"name": "New", "price": 10, "tax": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "New"
    assert body["price_with_tax"] == 12
    assert isinstance(body["id"], int)


def test_update_item():
    response = client.put("/items/1", json={"name": "Foo2", "price": 60})
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Foo2"


def test_filtered_items_not_captured_as_item_id():
    response = client.get("/items/filtered/", params={"limit": 5})
    assert response.status_code == 200
    assert response.json()["limit"] == 5
