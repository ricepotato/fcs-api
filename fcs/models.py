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
    status: Status = Status.present
    related: List["FCS"] = pydantic.Field(default_factory=list)
    description: Optional[str]

    @pydantic.validator("no", always=True)
    def set_name(cls, v, values):
        num = re.findall(r"\d{7}", values["name"])
        if num:
            return num[0]
        return None

    class Config:
        orm_mode = True
        


