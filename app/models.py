from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SAEnum

class ShipmentStatus(str, Enum):
    created = "created"
    in_transit = "in_transit"
    delivered = "delivered"
    failed = "failed"



class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True)
    status = Column(SAEnum(ShipmentStatus), default= ShipmentStatus.created)
    origin = Column(String)
    destination = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)