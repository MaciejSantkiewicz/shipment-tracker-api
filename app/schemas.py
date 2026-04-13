from pydantic import BaseModel, Field, field_validator
from app.models import ShipmentStatus

import re

class ShipmentCreate(BaseModel):
    client_id: str = Field(min_length= 5, max_length= 5)
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
    client_id: str = Field(min_length= 5, max_lengths= 5)
    name: str = Field(min_length= 2, max_length= 50)
    address: str = Field(min_length= 2, max_length= 50)
    telephone: str = Field(min_length= 2, mmax_length= 15)
    email: str = Field(min_length= 2, max_length= 25)

class ClientUpdate(BaseModel):
    active: bool


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)

class Token(BaseModel):
    access_token: str
    token_type: str