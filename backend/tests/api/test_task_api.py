def test_task_endpoints_use_service_flow(client):
    psp_rv = client.post('/api/psps', json={
        'title': 'Task PSP',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31'
    })
    assert psp_rv.status_code == 201
    psp_id = psp_rv.get_json()['id']

    create_rv = client.post(f'/api/psps/{psp_id}/tasks', json={
        'description': 'Test task',
        'category': 'Finance',
        'start_date': '2026-01-01',
        'completed_value': 0,
        'target_value': 5
    })
    assert create_rv.status_code == 201
    task = create_rv.get_json()
    assert task['description'] == 'Test task'

    update_rv = client.patch(f"/api/psps/{psp_id}/tasks/{task['id']}", json={'completed': True})
    assert update_rv.status_code == 200
    assert update_rv.get_json()['completed'] is True

    delete_rv = client.delete(f"/api/psps/{psp_id}/tasks/{task['id']}")
    assert delete_rv.status_code == 204


def test_task_create_rejects_invalid_dates(client):
    psp_rv = client.post('/api/psps', json={
        'title': 'Invalid Task PSP',
        'start_date': '2026-01-01',
        'end_date': '2026-12-31'
    })
    assert psp_rv.status_code == 201
    psp_id = psp_rv.get_json()['id']

    create_rv = client.post(f'/api/psps/{psp_id}/tasks', json={
        'description': 'Bad task',
        'category': 'Finance',
        'start_date': '2026-02-01',
        'due_date': '2026-01-01'
    })
    assert create_rv.status_code == 400
