from flask import Blueprint, request, jsonify
from ..repository import psp_repo

bp = Blueprint('psp', __name__)


@bp.route('/api/psps', methods=['POST'])
def create_psp():
    payload = request.get_json() or {}
    # validation delegated to repository/schema
    try:
        out = psp_repo.create_psp(payload)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify(out), 201


@bp.route('/api/psps', methods=['GET'])
def list_psps():
    out = psp_repo.list_psps()
    return jsonify(out)


@bp.route('/api/psps/<int:psp_id>', methods=['GET'])
def get_psp(psp_id):
    out = psp_repo.get_psp_with_tasks(psp_id)
    if not out:
        return jsonify({'error': 'PSP not found'}), 404
    return jsonify(out)


@bp.route('/api/psps/<int:psp_id>/report', methods=['GET'])
def get_report(psp_id):
    out = psp_repo.get_psp_with_tasks(psp_id)
    if not out:
        return jsonify({'error': 'PSP not found'}), 404
    # already includes report
    return jsonify(out['report'])
