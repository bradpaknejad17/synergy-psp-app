from flask import Blueprint, request, jsonify
from ..repository import task_repo

bp = Blueprint('tasks', __name__)


@bp.route('/api/psps/<int:psp_id>/tasks', methods=['POST'])
def create_task(psp_id):
    payload = request.get_json() or {}
    out = task_repo.create_task(psp_id, payload)
    if out is None:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out), 201


@bp.route('/api/psps/<int:psp_id>/tasks/bulk', methods=['POST'])
def create_tasks_bulk(psp_id):
    payload = request.get_json() or []
    if not isinstance(payload, list):
        return jsonify({'error': 'expected a JSON array of tasks'}), 400
    out = task_repo.create_tasks_bulk(psp_id, payload)
    if out is None:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out), 201


@bp.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    payload = request.get_json() or {}
    out = task_repo.update_task(task_id, payload)
    if out is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(out)


@bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    ok = task_repo.delete_task(task_id)
    if not ok:
        return jsonify({'error': 'Task not found'}), 404
    return ('', 204)
