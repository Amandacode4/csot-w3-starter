import pytest
from app.main import app, db, Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

def test_version(client):
    response = client.get('/api/version')
    assert response.status_code == 200
    assert "version" in response.get_json()

def test_create_item(client):
    response = client.post('/api/items', json={"name": "test item"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "test item"
    assert "id" in data

def test_create_item_missing_name(client):
    response = client.post('/api/items', json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_list_items(client):
    client.post('/api/items', json={"name": "item 1"})
    client.post('/api/items', json={"name": "item 2"})
    response = client.get('/api/items')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["items"]) == 2
    assert data["items"][0]["name"] == "item 1"
    assert data["items"][1]["name"] == "item 2"
