from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import models
from app.models import Client
from app.database import get_db

from app.schemas import ClientCreate


router = APIRouter()


@router.post("/clients/", status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Client).filter(models.Client.client_id == client.client_id).first()
                        
    if existing:
        raise HTTPException(status_code=400, detail="This client ID already exists")

    db_clients = models.Client(**client.model_dump())
    db.add(db_clients)
    db.commit()
    db.refresh(db_clients)
    return db_clients

@router.get("/clients/")
def get_all_client(db: Session = Depends(get_db)):
    query = db.query(models.Client)
    return query.all()