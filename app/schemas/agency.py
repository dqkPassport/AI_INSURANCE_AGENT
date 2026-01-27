from pydantic import BaseModel


class AgencyCreate(BaseModel):
    name: str


class AgencyOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
