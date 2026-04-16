from pydantic import BaseModel, Field, field_validator
from app.models import ShipmentStatus, UserRole

import re

class ShipmentCreate(BaseModel):
    client_id: str = Field(min_length= 6, max_length= 6)
    tracking_number: str = Field(min_length= 1, max_length= 10)
    origin: str = Field(min_length= 2, max_length= 2)
    destination: str = Field(min_length= 2, max_length= 2)

    @field_validator("origin", "destination")
    @classmethod
    def validate_country_code(cls, v):
        if not re.match(r"^[A-Z]{2}$", v):
            raise ValueError("Must be a 2-letter uppercase country code (e.g. PL, DE)")
        return v

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus

class ClientCreate(BaseModel):
    client_id: str = Field(min_length= 6, max_lengths= 6)
    name: str = Field(min_length= 2, max_length= 50)
    address: str = Field(min_length= 2, max_length= 50)
    telephone: str = Field(min_length= 2, mmax_length= 15)
    email: str = Field(min_length= 2, max_length= 25)

class ClientUpdate(BaseModel):
    active: bool


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)
    role: UserRole = Field(default = UserRole.client_user)


class ClientUserCreate(BaseModel):
    user_id: int
    client_id: int

class Token(BaseModel):
    access_token: str
    token_type: str