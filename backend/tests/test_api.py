import json
import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'ok'

def test_create_and_list_psp(client):
    payload = {
        'title': 'My PSP',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31'
    }
    rv = client.post('/api/psps', json=payload)
    assert rv.status_code == 201
    psp = rv.get_json()
    assert psp['title'] == 'My PSP'

    rv = client.get('/api/psps')
    assert rv.status_code == 200
    psps = rv.get_json()
    assert isinstance(psps, list)
    assert any(p['title'] == 'My PSP' for p in psps)
