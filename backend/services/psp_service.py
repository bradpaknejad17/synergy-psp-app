from typing import Any, Dict, List, Optional

from ..api.requests.psp_request import CreatePSPRequest
from ..api.responses.psp_response import PSPDTO, PSPDetailDTO
from ..mappers.psp_mapper import to_detail_dto, to_dto
from ..persistence.models.db import PSPStatusEnum
from ..repository.psp_repo import PSPRepository
from ..repository.psp_repo import aggregate_by_category, compute_psp_percent


class PSPService:
    def __init__(self, repo: PSPRepository):
        self.repo = repo

    def create(self, request: CreatePSPRequest) -> PSPDTO:
        psp = self.repo.create_psp(
            title=request.title,
            contract=request.contract,
            vision=request.vision,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        return to_dto(psp)

    def list(self, status: Optional[PSPStatusEnum] = None) -> List[PSPDTO]:
        return [to_dto(psp) for psp in self.repo.list_psps(status=status)]

    def get_psp_with_tasks(self, psp_id: int) -> Optional[PSPDetailDTO]:
        psp = self.repo.get_psp_with_tasks(psp_id)
        if not psp:
            return None
        return to_detail_dto(
            psp,
            percent_complete=compute_psp_percent(psp),
            by_category=aggregate_by_category(psp),
        )

    def delete(self, psp_id: int) -> Optional[PSPDTO]:
        psp = self.repo.delete_by_id(psp_id)
        if not psp:
            return None
        return to_dto(psp)
