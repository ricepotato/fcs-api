from typing import Union
import fastapi
import logging
from fcs import containers, models, service

log = logging.getLogger(f"abc.{__name__}")

router = fastapi.APIRouter()


class CommonQueryParams:
    def __init__(self, no: Union[str, None] = None, offset: int = 0, limit: int = 20):
        self.no = no
        self.offset = offset
        self.limit = limit


@router.get("/")
async def root():
    return {"message": "hello"}


@router.get("/v1/fcs", response_model=models.FCSListResponse)
async def get_fcs_list(
    commons: CommonQueryParams = fastapi.Depends(),
    svc: service.FCSServiceProtocol = fastapi.Depends(
        containers.container.get_fcs_service
    ),
):
    return {}


@router.get("/v1/fcs/{no}", response_model=models.FCS)
async def get_fcs(
    no: str,
    svc: service.FCSServiceProtocol = fastapi.Depends(
        containers.container.get_fcs_service
    ),
):
    return models.FCS(name="FC2PPV-3133751")


@router.post("/v1/fcs", response_model=models.FCS)
async def set_fcs(
    fcs: models.FCS,
    svc: service.FCSServiceProtocol = fastapi.Depends(
        containers.container.get_fcs_service
    ),
):
    return {}
