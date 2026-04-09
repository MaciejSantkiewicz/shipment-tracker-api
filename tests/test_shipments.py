from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import pytest

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

testing = TestClient(app)


#---------------DB setup & cleanup------------------------
def setup_function():
    # new table for testing
    Base.metadata.create_all(bind=engine)


def teardown_function():
    # clears all tables after tests
    Base.metadata.drop_all(bind=engine)


#-------------fixtures---------------------
@pytest.fixture
def create_new_client():
    testing.post(
        "/clients/",
        json = {
            "client_id": "TEST-PL-001",
            "name": "New Client",
            "address": "Client address 1",
            "telephone": "111-111-111",
            "email": "new_client_email@email.com"
        }
    )



#-----------CLIENT enpoints tests----------------------------
def test_create_client():
    response = testing.post(
        "/clients/",
        json = {
            "client_id": "TEST-PL-001",
            "name": "New Client",
            "address": "Client address 1",
            "telephone": "111-111-111",
            "email": "new_client_email@email.com"
        }
    )
    assert response.status_code == 201


def test_create_duplicated_id_client(create_new_client):
    response = testing.post(
        "/clients/",
        json = {
            "client_id": "TEST-PL-001",
            "name": "New Client 2 ",
            "address": "Client address 2",
            "telephone": "211-211-211",
            "email": "new_client_email2@email.com"
        }
    )
    
    assert response.status_code == 400
    print(response.json())

#-----------SHIPMENT enpoints tests---------------------------
def test_create_shipment(create_new_client):
    response = testing.post(
        "/shipments/",
        json={
            "client_id": "TEST-PL-001",
            "tracking_number": "TEST-001",
            "origin": "Warsaw",
            "destination": "Berlin"
        }
    )

    assert response.status_code == 201
    
    
def test_create_shipment_invalid_client_id(create_new_client):
    response = testing.post(
        "/shipments/",
        json={
            "client_id": "TEST-PL-999",
            "tracking_number": "TEST-001",
            "origin": "Warsaw",
            "destination": "Berlin"
        }
    )

    assert response.status_code == 400
    print(response.json())

def test_get_shipment_not_found():
    response = testing.get(
        "/shipments/TEST-XYZ"
    )
    assert response.status_code == 404
    print(response.json())

def test_get_shipment(create_new_client):
    create_shipment = testing.post(
        "/shipments/",
        json={
            "client_id": "TEST-PL-001",
            "tracking_number": "TEST-123",
            "origin": "Warsaw",
            "destination": "Berlin"
        }
    )

    get_response = testing.get(
        "/shipments/TEST-123"
    )


    assert get_response.status_code == 200
    

