from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SAEnum

class ShipmentStatus(str, Enum):
    created = "created"
    in_transit = "in_transit"
    delivered = "delivered"
    failed = "failed"


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True)
    active = Column(Boolean, default=True)
    name = Column(String)
    address = Column(String)
    telephone = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, default=None)




class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True)
    status = Column(SAEnum(ShipmentStatus), default= ShipmentStatus.created)
    origin = Column(String)
    destination = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    client_id = Column(Integer, ForeignKey("clients.id"))

