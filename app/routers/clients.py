from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import models
from app.models import Client
from app.database import get_db, execute_with_sql
from sqlalchemy import select

from app.schemas import ClientCreate, ClientUpdate

from datetime import datetime
router = APIRouter(tags=["clients"])


@router.post("/clients/", status_code=201)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    client_stmt = select(models.Client).where(models.Client.client_id == client.client_id)
    client_result = db.execute(client_stmt).scalars().first()

    if client_result:
        raise HTTPException(status_code=400, detail="This client ID already exists")
      
    db_clients = models.Client(**client.model_dump())
    db.add(db_clients)
    db.commit()
    db.refresh(db_clients)
    return db_clients

@router.get("/clients/")
def get_all_client(db: Session = Depends(get_db)):
    client_stmt = select(models.Client)

    return execute_with_sql(db, client_stmt, False)


@router.patch("/clients/status/{client_id}")
def change_client_status(client_id: str, update: ClientUpdate, db: Session = Depends(get_db)):
    stmt = select(models.Client).where(models.Client.client_id == client_id)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(status_code=404, detail="Shipment not found")

    result.active = update.active
    result.updated_at = datetime.utcnow()
    if not update.active:
        result.closed_at = datetime.utcnow()

    db.commit()
    db.refresh(result)
    return execute_with_sql(db, stmt, False, True)

    