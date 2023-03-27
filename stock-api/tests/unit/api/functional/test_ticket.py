import json
from tests.unit.api.functional import client

def test_ticket(client):
    response = client.get('/api/ticket/')
    assert response.status_code == 200

def test_create_a_ticket(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    ticket = {
        'ticket': 'TEST4',
        'market': 'normal',
        'stock_id': 1
    }
    response = client.post('/api/ticket/', data=json.dumps(ticket), headers=headers)
    assert response.status_code == 200
    assert response.data