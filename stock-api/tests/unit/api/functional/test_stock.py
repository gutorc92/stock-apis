import json
from tests.unit.api.functional import client

def test_a_stock(client):
    response = client.get('/api/stock/1')
    assert response.status_code == 200
    assert response != None

def test_list_stock(client):
    response = client.get('/api/stock')
    assert response.status_code == 200


def test_create_a_stock(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    stock = {
        'name': 'Teste',
        'base_ticket': 'TEST'
    }
    response = client.post('/api/stock', data=json.dumps(stock), headers=headers)
    assert response.status_code == 200