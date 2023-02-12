import datetime
import re
from typing import List, Optional
import pydantic

import enum


class Status(enum.Enum):
    present = "present"
    absent = "absent"
    ignore = "ignore"


class FCS(pydantic.BaseModel):
    id: Optional[str]
    name: str
    no: Optional[str]
    hash: Optional[str]
    status: Status = pydantic.Field(default=Status.present)
    tags: List[str] = pydantic.Field(default_factory=list)
    related: List["FCS"] = pydantic.Field(default_factory=list)
    images: List[pydantic.HttpUrl] = pydantic.Field(default_factory=list)
    description: Optional[str]
    created_at: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )

    @pydantic.validator("no", always=True)
    def set_name(cls, v, values):
        num = re.findall(r"\d{7}", values["name"])
        if num:
            return num[0]
        return None

    @classmethod
    def from_mongo_result(cls, result: dict) -> "FCS":
        fcs_result = cls.parse_obj(result)
        fcs_result.status = Status(fcs_result.status)
        fcs_result.id = str(result["_id"])
        return fcs_result

    class Config:
        orm_mode = True
        use_enum_values = True


class FCSListResponse(pydantic.BaseModel):
    items: List[FCS]
    total: int
    offset: int
    limit: int
