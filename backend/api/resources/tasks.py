from flask import Blueprint, request, jsonify

from ...repository.task_repo import TaskRepository
from ...services.task_service import TaskService

bp = Blueprint('tasks', __name__)
service = TaskService(TaskRepository())


@bp.post('/api/psps/<int:psp_id>/tasks')
def create_task(psp_id):
    payload = request.get_json() or {}
    out = service.create(psp_id, payload)
    if out is None:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out.model_dump(mode="json")), 201


@bp.post('/api/psps/<int:psp_id>/tasks/bulk')
def create_tasks_bulk(psp_id):
    payload = request.get_json() or []
    if not isinstance(payload, list):
        return jsonify({'error': 'expected a JSON array of tasks'}), 400
    out = service.create_bulk(psp_id, payload)
    if out is None:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify([task.model_dump(mode="json") for task in out]), 201


@bp.patch('/api/tasks/<int:task_id>')
def update_task(task_id):
    payload = request.get_json() or {}
    out = service.update(task_id, payload)
    if out is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(out.model_dump(mode="json"))


@bp.delete('/api/tasks/<int:task_id>')
def delete_task(task_id):
    ok = service.delete(task_id)
    if not ok:
        return jsonify({'error': 'Task not found'}), 404
    return ('', 204)
