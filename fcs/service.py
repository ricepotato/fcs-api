from typing import Optional, Protocol
from fcs import models, repository


class FCSServiceProtocol(Protocol):
    def get_fcs_list(self, offset: int, limit: int) -> models.FCSListResponse:
        ...

    def get_fcs_by_no(self, no: str) -> models.FCS:
        ...

    def set_fcs(self, fcs: models.FCS) -> Optional[models.FCS]:
        ...


class FCSService:
    def __init__(self, repo: repository.Repository):
        self.repo = repo

    def get_fcs_list(self, offset: int, limit: int) -> models.FCSListResponse:
        fcs_list = self.repo.get_fc_list(offset, limit)
        count = self.repo.get_count()
        return models.FCSListResponse(
            items=fcs_list, total=count, offset=offset, limit=limit
        )

    def get_fcs_by_no(self, no: str) -> models.FCS:
        fc_obj = self.repo.get_fc_by_no(no)
        if fc_obj is None:
            raise FCSServiceNotFound(f"{no=}")

        return fc_obj

    def set_fcs(self, fcs: models.FCS) -> Optional[models.FCS]:
        result_id = self.repo.insert_fc(fcs)
        if result_id:
            return self.repo.get_fc(result_id)
        else:
            return None


class FCSServiceError(Exception):
    pass


class FCSServiceNotFound(FCSServiceError):
    pass
