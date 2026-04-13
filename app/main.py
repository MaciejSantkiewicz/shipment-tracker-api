from fastapi import FastAPI
from app.database import engine, Base
from app.routers import clients, shipments, auth



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shipment Tracker API", version="1.0.0")
app.include_router(clients.router)
app.include_router(shipments.router)
app.include_router(auth.router)

# --- Endpoints ---

@app.get("/")
def root():
    return {"message": "Shipment Tracker API is running"}
