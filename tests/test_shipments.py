from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# temporary test db
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# swaping db's
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function():
    # new table for testing
    Base.metadata.create_all(bind=engine)


def teardown_function():
    # clears all tables after tests
    Base.metadata.drop_all(bind=engine)


def test_create_shipment():
    response = client.post(
        "/shipments/",
        json={
            "tracking_number": "TEST-001",
            "origin": "Warsaw",
            "destination": "Berlin"
        }
    )
    assert response.status_code == 201
    assert response.json()["tracking_number"] == "TEST-001"
    


def test_get_shipment_not_found():
    response = client.get(
        "/shipments/TEST-XYZ"
    )
    assert response.status_code == 404

def test_get_shipment():
    create_shipment = client.post(
        "/shipments/",
        json={
            "tracking_number": "TEST-123",
            "origin": "Warsaw",
            "destination": "Berlin"
        }
    )

    get_response = client.get(
        "/shipments/TEST-123"
    )


    assert get_response.status_code == 200
    