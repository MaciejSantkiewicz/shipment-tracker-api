from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from app.database import SessionLocal, engine, Base
from app import models
from app.models import ShipmentStatus


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shipment Tracker API", version="1.0.0")


# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Pydantic data validation ---
class ShipmentCreate(BaseModel):
    tracking_number: str
    origin: str
    destination: str

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus


# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Shipment Tracker API is running"}


@app.post("/shipments/", status_code=201)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Shipment).filter(
        models.Shipment.tracking_number == shipment.tracking_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tracking number already exists")

    db_shipment = models.Shipment(**shipment.model_dump())
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


@app.get("/shipments/")
def get_all_shipments(db: Session = Depends(get_db)):
    return db.query(models.Shipment).all()


@app.get("/shipments/{tracking_number}")
def get_shipment(tracking_number: str, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.tracking_number == tracking_number
    ).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@app.patch("/shipments/{tracking_number}/status")
def update_status(tracking_number: str, update: ShipmentUpdate, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment.status = update.status
    shipment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(shipment)
    return shipment

@app.delete("/shipments/{tracking_number}", status_code=204)
def delete_shipment(tracking_number: str, db: Session = Depends(get_db)):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    

    db.delete(shipment)
    db.commit()
    