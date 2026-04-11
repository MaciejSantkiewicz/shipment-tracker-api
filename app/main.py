from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.database import engine, Base, get_db, execute_with_sql
from app import models
from app.routers import clients

from app.schemas import ShipmentCreate, ShipmentUpdate
from app.models import ShipmentStatus


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shipment Tracker API", version="1.0.0")
app.include_router(clients.router)

# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Shipment Tracker API is running"}


@app.post("/shipments/", status_code=201)
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



@app.get("/shipments/")
def get_all_shipments(status: Optional[ShipmentStatus] = None, db: Session = Depends(get_db)):
    stmt = select(models.Shipment)
    if status:
            stmt = stmt.where(models.Shipment.status == status)
    
    return execute_with_sql(db, stmt, False)


@app.get("/shipments/with-clients")
def get_shipments_with_clients(db: Session = Depends(get_db)):
    stmt = select(models.Shipment.tracking_number, models.Shipment.status,models.Client.name, models.Client.email, models.Client.client_id).join(
        models.Client, models.Client.client_id == models.Shipment.client_id
    )
    return execute_with_sql(db, stmt, True)
 


@app.get("/shipments/{tracking_number}")
def get_shipment(tracking_number: str, db: Session = Depends(get_db)):
    stmt = select(models.Shipment).where(models.Shipment.tracking_number == tracking_number)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return execute_with_sql(db, stmt, False, True)


@app.patch("/shipments/{tracking_number}/status")
def update_status(tracking_number: str, update: ShipmentStatus, db: Session = Depends(get_db)):
    stmt = select(models.Shipment).where(models.Shipment.tracking_number == tracking_number)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")

    result.status = update
    result.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(result)
    return result



@app.delete("/shipments/{tracking_number}", status_code=204)
def delete_shipment(tracking_number: str, db: Session = Depends(get_db)):
    stmt = select(models.Shipment).where(models.Shipment.tracking_number == tracking_number)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")
    
    db.delete(result)
    db.commit()
    