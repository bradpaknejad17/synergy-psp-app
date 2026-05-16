import json
import pytest
from backend.app import create_app
from backend.persistence.models.db import PSP, PSPStatusEnum
from backend.repository.db import SessionLocal

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


def test_list_psps_can_filter_by_status(client):
    active_payload = {
        'title': 'Active PSP',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31'
    }
    completed_payload = {
        'title': 'Completed PSP',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31'
    }

    active_rv = client.post('/api/psps', json=active_payload)
    completed_rv = client.post('/api/psps', json=completed_payload)
    assert active_rv.status_code == 201
    assert completed_rv.status_code == 201

    completed_id = completed_rv.get_json()['id']
    with SessionLocal() as session:
        psp = session.get(PSP, completed_id)
        psp.status = PSPStatusEnum.COMPLETED
        session.add(psp)
        session.commit()

    rv = client.get('/api/psps?status=COMPLETED')
    assert rv.status_code == 200
    psps = rv.get_json()
    assert isinstance(psps, list)
    assert all(psp['status'] == 'COMPLETED' for psp in psps)
    assert any(psp['id'] == completed_id and psp['title'] == 'Completed PSP' for psp in psps)


def test_delete_psp_marks_status_deleted(client):
    payload = {
        'title': 'Delete Me',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31'
    }
    rv = client.post('/api/psps', json=payload)
    assert rv.status_code == 201
    psp_id = rv.get_json()['id']

    delete_rv = client.delete(f'/api/psps/{psp_id}')
    assert delete_rv.status_code == 200
    deleted = delete_rv.get_json()
    assert deleted['status'] == 'DELETED'

    with SessionLocal() as session:
        psp = session.get(PSP, psp_id)
        assert psp is not None
        assert psp.status == PSPStatusEnum.DELETED
