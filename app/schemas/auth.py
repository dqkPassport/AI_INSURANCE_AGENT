from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=72)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=72)
    agency_id: int
    role: str = "agent"


class UserOut(BaseModel):
    id: int
    email: str
    agency_id: int
    role: str

    model_config = {"from_attributes": True}
