# 📦 Shipment Tracker API

A RESTful API for tracking shipments — built with FastAPI, SQLAlchemy, and SQLite.

Inspired by real-world e-commerce integration experience (DHL eConnect REST API, OAuth 2.0).

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

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/shipments/` | Create a new shipment |
| GET | `/shipments/` | Get all shipments |
| GET | `/shipments/{tracking_number}` | Get shipment by tracking number |
| PATCH | `/shipments/{tracking_number}/status` | Update shipment status |
| DELETE | `/shipments/{tracking_number}` | Delete shipment |

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

**Create a shipment:**
```bash
curl -X POST http://127.0.0.1:8000/shipments/ \
  -H "Content-Type: application/json" \
  -d '{"tracking_number": "DHL-001", "origin": "Warsaw", "destination": "Berlin"}'
```

**Response:**
```json
{
  "id": 1,
  "tracking_number": "DHL-001",
  "status": "created",
  "origin": "Warsaw",
  "destination": "Berlin",
  "created_at": "2026-04-07T12:00:00",
  "updated_at": "2026-04-07T12:00:00"
}
```

---

## 🗺️ Roadmap

- [ ] PostgreSQL support
- [ ] Docker containerization
- [ ] Authentication (JWT / OAuth 2.0)
- [ ] External API integration
- [ ] Dashboard UI (Streamlit)
- [ ] AI anomaly detection layer

---
