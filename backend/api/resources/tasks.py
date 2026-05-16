from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from ..error_handlers import normalize_validation_error
from ..requests.task_request import CreateTaskRequest, UpdateTaskRequest
from ...repository.task_repo import TaskRepository
from ...services.task_service import TaskService

bp = Blueprint('tasks', __name__, url_prefix='/api/psp')
service = TaskService(TaskRepository())


@bp.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify({"error": normalize_validation_error(error)}), 400


@bp.post('/<int:psp_id>/tasks')
def create_task(psp_id):
    payload = request.get_json() or {}
    create_request = CreateTaskRequest.model_validate(payload)

    out = service.create(psp_id, create_request)
    if out is None:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out.model_dump(mode="json")), 201


@bp.post('/<int:psp_id>/tasks/bulk')
def create_tasks_bulk(psp_id):
    payload = request.get_json() or []
    if not isinstance(payload, list):
        return jsonify({'error': 'expected a JSON array of tasks'}), 400
    create_requests = [CreateTaskRequest.model_validate(item) for item in payload]

    out = service.create_bulk(psp_id, create_requests)
    if out is None:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify([task.model_dump(mode="json") for task in out]), 201


@bp.patch('/<int:psp_id>/tasks/<int:task_id>')
def update_task(psp_id, task_id):
    payload = request.get_json() or {}
    update_request = UpdateTaskRequest.model_validate(payload)

    out = service.update(psp_id, task_id, update_request)
    if out is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(out.model_dump(mode="json"))


@bp.delete('/<int:psp_id>/tasks/<int:task_id>')
def delete_task(psp_id, task_id):
    ok = service.delete(psp_id, task_id)
    if not ok:
        return jsonify({'error': 'Task not found'}), 404
    return ('', 204)
