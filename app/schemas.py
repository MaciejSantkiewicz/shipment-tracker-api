from pydantic import BaseModel
from app.models import ShipmentStatus

class ShipmentCreate(BaseModel):
    client_id: str
    tracking_number: str
    origin: str
    destination: str

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus

class ClientCreate(BaseModel):
    client_id: str
    name: str
    address: str
    telephone: str
    email: str