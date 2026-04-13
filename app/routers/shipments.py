from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from typing import Optional
from datetime import datetime

from app import models
from app.models import ShipmentStatus
from app.database import get_db, execute_with_sql

from app.schemas import ShipmentUpdate, ShipmentCreate


router = APIRouter()

@router.post("/shipments/", status_code=201)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    client_stmt = select(models.Client).where(models.Client.client_id == shipment.client_id)
    client_result = db.execute(client_stmt).scalars().first()

    if not client_result:
        raise HTTPException(status_code=400, detail="Client ID not found")

    shipment_stmt = select(models.Shipment).where(models.Shipment.tracking_number == shipment.tracking_number)
    shipment_result = db.execute(shipment_stmt).scalars().first()

    if shipment_result:
        raise HTTPException(status_code=400, detail="Tracking number already exists")

    
    db_shipment = models.Shipment(**shipment.model_dump())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


@router.get("/shipments/")
def get_all_shipments(status: Optional[ShipmentStatus] = None, db: Session = Depends(get_db)):
    stmt = select(models.Shipment)
    if status:
            stmt = stmt.where(models.Shipment.status == status)
    
    return execute_with_sql(db, stmt, False)


@router.get("/shipments/stats")
def shipments_stats(db: Session = Depends(get_db)):
    stmt = select(models.Shipment.status, func.count("*").label("shipment_count")).select_from(models.Shipment).group_by(models.Shipment.status)

    return execute_with_sql(db, stmt, mapping=True)

@router.get("/shipments/stats/filtered")
def shipments_status_count_check(min_count: int, db: Session = Depends(get_db)):
    stmt = select(models.Shipment.status, func.count("*").label("shipment_count")).select_from(models.Shipment).group_by(models.Shipment.status).having(func.count("*") >= min_count)

    return execute_with_sql(db, stmt, mapping=True)



@router.get("/shipments/with-clients")
def get_shipments_with_clients(db: Session = Depends(get_db)):
    stmt = select(models.Shipment.tracking_number, models.Shipment.status,models.Client.name, models.Client.email, models.Client.client_id).join(
        models.Client, models.Client.client_id == models.Shipment.client_id
    )
    return execute_with_sql(db, stmt, True)
 


@router.get("/shipments/{tracking_number}")
def get_shipment(tracking_number: str, db: Session = Depends(get_db)):
    stmt = select(models.Shipment).where(models.Shipment.tracking_number == tracking_number)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return execute_with_sql(db, stmt, False, True)


@router.patch("/shipments/{tracking_number}/status")
def update_status(tracking_number: str, update: ShipmentUpdate, db: Session = Depends(get_db)):
    stmt = select(models.Shipment).where(models.Shipment.tracking_number == tracking_number)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")

    result.status = update.status
    result.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(result)
    return result


@router.delete("/shipments/{tracking_number}", status_code=204)
def delete_shipment(tracking_number: str, db: Session = Depends(get_db)):
    stmt = select(models.Shipment).where(models.Shipment.tracking_number == tracking_number)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    db.delete(result)
    db.commit()


@router.get("/shipments/clients/{client_id}")
def get_all_client_shipments(client_id: str, db: Session = Depends(get_db)):
    client = select(models.Client).where(models.Client.client_id == client_id)
    result = db.execute(client).scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail="Client not found")
    
    stmt = select(models.Client.client_id, models.Shipment.tracking_number, models.Shipment.status, models.Shipment.origin,
                  models.Shipment.destination).join(models.Client, models.Shipment.client_id == models.Client.client_id).where(models.Shipment.client_id == client_id)
    
    return execute_with_sql(db, stmt, True)