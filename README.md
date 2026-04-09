# 📦 Shipment Tracker API

A RESTful API for tracking shipments — built with FastAPI, SQLAlchemy, and SQLite.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy ORM) |
| Validation | Pydantic |
| Server | Uvicorn |
| Language | Python 3.14 |

---

## 📋 Endpoints

### Shipments
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/shipments/` | Create a new shipment |
| GET | `/shipments/` | Get all shipments |
| GET | `/shipments/{tracking_number}` | Get shipment by tracking number |
| PATCH | `/shipments/{tracking_number}/status` | Update shipment status |
| DELETE | `/shipments/{tracking_number}` | Delete shipment |

### Clients
| Method | Endpoint | Description |
|---|---|---|
| GET | `/clients/` | Get all clients |
| POST | `/clients/` | Create a new client |
---

## ⚙️ Setup & Run
```bash
# Clone the repo
git clone https://github.com/MaciejSantkiewicz/shipment-tracker-api.git
cd shipment-tracker-api

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
python -m pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

API will be available at: `http://127.0.0.1:8000`

Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

---

## 📬 Example Request

**Createa a client:**
```bash
curl -X POST http://127.0.0.1:8000/client/ \
  -H "Content-Type: application/json" \
  -d '{"client_id": "DE-001", "name": "new client", "address": "new client address 1","telephone": "111-111-11-11","email": "new_client_email@emil.com}'
```

**Response:**
```json
{
  "address": "new client address 1",
  "client_id": "DE-001",
  "active": true,
  "email": "new_client_email@emil.com",
  "updated_at": "2026-04-09T10:39:55.766695",
  "id": 2,
  "name": "new client",
  "telephone": "111-111-11-11",
  "created_at": "2026-04-09T10:39:55.766690",
  "closed_at": null
}
```


**Create a shipment:**
```bash
curl -X POST http://127.0.0.1:8000/shipments/ \
  -H "Content-Type: application/json" \
  -d '{"client_id": "DE-001", tracking_number": "DE-PL-0001", "origin": "Germany", "destination": "Poland"}'
```

**Response:**
```json
{
  "id": 1,
  "client_id": "DE-001",
  "tracking_number": "DDE-PL-0001",
  "status": "created",
  "origin": "Germany",
  "destination": "Poland",
  "created_at": "2026-04-07T12:00:00",
  "updated_at": "2026-04-07T12:00:00"
}
```

---

## 🗺️ Roadmap

- [ ] PostgreSQL support
- [x] Client model with foreign key relationship
- [ ] Docker containerization
- [ ] Authentication (JWT / OAuth 2.0)
- [ ] External API integration
- [ ] JOIN queries with SQL visibility
- [ ] Dashboard UI (Streamlit)
- [ ] AI anomaly detection layer

---
