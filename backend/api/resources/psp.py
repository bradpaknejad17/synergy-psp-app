from typing import List

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from ..error_handlers import normalize_validation_error
from ...persistence.models.db import PSPStatusEnum
from ...repository.psp_repo import PSPRepository
from ...services.psp_service import PSPService
from ..requests.psp_request import CreatePSPRequest


bp = Blueprint('psp', __name__)
service = PSPService(PSPRepository())


@bp.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify({"error": normalize_validation_error(error)}), 400


@bp.post('/api/psps')
def create_psp():
    payload = request.get_json() or {}
    create_request = CreatePSPRequest.model_validate(payload)

    try:
        psp = service.create(create_request)
        return jsonify(psp.model_dump(mode="json")), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.get('/api/psps')
def list_psps():
    status_param = request.args.get("status")
    if status_param:
        try:
            status = PSPStatusEnum(status_param.upper())
        except ValueError:
            allowed = [status.value for status in PSPStatusEnum]
            return jsonify({"error": f"invalid status '{status_param}'", "allowed": allowed}), 400
    else:
        status = None

    psps = [psp.model_dump(mode="json") for psp in service.list(status=status)]
    return jsonify(psps)


@bp.get('/api/psps/<int:psp_id>')
def get_psp(psp_id):
    out = service.get_psp_with_tasks(psp_id)
    if not out:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out.model_dump(mode="json"))


@bp.get('/api/psps/<int:psp_id>/report')
def get_report(psp_id):
    out = service.get_psp_with_tasks(psp_id)
    if not out:
        return jsonify({'error': 'PSP not found'}), 404
    # already includes report
    return jsonify(out.report.model_dump(mode="json"))


@bp.delete('/api/psps/<int:psp_id>')
def delete_psp(psp_id):
    out = service.delete(psp_id)
    if not out:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out.model_dump(mode="json"))
