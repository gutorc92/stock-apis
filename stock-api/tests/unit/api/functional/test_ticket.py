import json
from tests.unit.api.functional import client

def test_ticket(client):
    response = client.get('/api/ticket/')
    assert response.status_code == 200