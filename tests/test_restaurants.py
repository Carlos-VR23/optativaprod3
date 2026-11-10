# tests/test_restaurants.py
# Requiere el emulador de Firestore corriendo: firebase emulators:start --only firestore
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
API = "/api/v1/restaurants"

PAYLOAD = {"name": "Restaurante Test", "category": "TestCat", "city": "TestCity", "price": 2}


@pytest.fixture
def restaurant():
    """Crea un restaurante y lo borra al terminar la prueba."""
    response = client.post(API, json=PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    yield data
    client.delete(f"{API}/{data['id']}")


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_restaurant(restaurant):
    assert restaurant["name"] == "Restaurante Test"
    assert restaurant["avgRating"] == 0
    assert restaurant["numRatings"] == 0
    assert restaurant["id"]


def test_get_restaurant(restaurant):
    response = client.get(f"{API}/{restaurant['id']}")
    assert response.status_code == 200
    assert response.json()["city"] == "TestCity"


def test_get_restaurant_not_found():
    assert client.get(f"{API}/no-existe-123").status_code == 404


def test_list_and_filters(restaurant):
    response = client.get(API, params={"city": "TestCity", "category": "TestCat", "price": 2})
    assert response.status_code == 200
    ids = [r["id"] for r in response.json()]
    assert restaurant["id"] in ids

    # Un precio distinto no debe devolver el restaurante
    response = client.get(API, params={"city": "TestCity", "category": "TestCat", "price": 3})
    assert restaurant["id"] not in [r["id"] for r in response.json()]


def test_update_restaurant(restaurant):
    response = client.patch(f"{API}/{restaurant['id']}", json={"name": "Nombre Nuevo", "price": 3})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Nombre Nuevo"
    assert body["price"] == 3
    assert body["city"] == "TestCity"  # lo no enviado no cambia


def test_update_ignores_non_editable_fields(restaurant):
    client.patch(f"{API}/{restaurant['id']}", json={"name": "X", "avgRating": 5})
    assert client.get(f"{API}/{restaurant['id']}").json()["avgRating"] == 0


def test_update_empty_body(restaurant):
    assert client.patch(f"{API}/{restaurant['id']}", json={}).status_code == 400


def test_update_not_found():
    assert client.patch(f"{API}/no-existe-123", json={"name": "X"}).status_code == 404


def test_delete_restaurant():
    created = client.post(API, json=PAYLOAD).json()
    assert client.delete(f"{API}/{created['id']}").status_code == 204
    assert client.get(f"{API}/{created['id']}").status_code == 404
    assert client.delete(f"{API}/{created['id']}").status_code == 404


@pytest.mark.parametrize("bad", [
    {**PAYLOAD, "price": 10},
    {**PAYLOAD, "price": 0},
    {**PAYLOAD, "name": ""},
    {"category": "X", "city": "Y", "price": 1},  # falta name
])
def test_invalid_payloads(bad):
    assert client.post(API, json=bad).status_code == 422


def test_html_pages(restaurant):
    assert client.get("/").status_code == 200
    assert client.get("/restaurants/new").status_code == 200
    assert client.get(f"/restaurants/{restaurant['id']}").status_code == 200
    assert client.get(f"/restaurants/{restaurant['id']}/edit").status_code == 200
    assert client.get("/restaurants/no-existe-123").status_code == 404
