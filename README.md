# 📦 Shipment Tracker API

A RESTful API for tracking shipments — built with FastAPI, SQLAlchemy, and SQLite.
GUI made with Streamlit.

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy ORM) |
| Validation | Pydantic |
| Server | Uvicorn |
| Language | Python 3.14 |
| GUI | Streamlit |

---

## 👥 User Roles

The API supports three user roles, each with different access levels:

| Role | Access |
|---|---|
| `admin` | Full access to all endpoints and all clients |
| `employee` | Access to one or more assigned clients |
| `client_user` | Access to exactly one assigned client (limit enforced by API) |

User-client assignments are managed through the `user_clients` table. Role-based access is enforced on all protected endpoints via JWT authentication.

---

## 📋 Endpoints

### Authentication & Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/users` | Get all users |
| POST | `/auth/users/clients` | Assign a client to a user |
| POST | `/auth/users/connection` | View all user-client connections |
| POST | `/auth/users/client/connection` | View connections for a specific user-client pair |

#### Rules for `/auth/users/clients`

- Returns `404` if user or client does not exist
- Returns `409` if the user-client connection already exists
- Returns `409` if a `client_user` already has a client assigned (limit: 1)

---

### Clients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/clients/` | Create a new client |
| GET | `/clients/` | Get all clients |
| PATCH | `/clients/status/{client_id}` | Update client status (active/inactive) |
| PATCH | `/clients/details/{client_id}` | Update client details |

---

### Shipments

| Method | Endpoint | Description |
|---|---|---|
| POST | `/shipments/` | Create a new shipment |
| GET | `/shipments/` | Get all shipments |
| GET | `/shipments/stats` | Count all shipments grouped by status |
| GET | `/shipments/stats/filtered` | Show shipments grouped by status with minimum count filter |
| GET | `/shipments/with-clients` | Show all shipments with joined client data |
| GET | `/shipments/{tracking_number}` | Get shipment by tracking number |
| GET | `/shipments/clients/{client_id}` | Get all shipments for a specific client |
| PATCH | `/shipments/{tracking_number}/status` | Update shipment status |
| DELETE | `/shipments/{tracking_number}` | Delete shipment |

Shipment statuses: `created`, `in_transit`, `delivered`, `failed`

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

# Run Streamlit
python -m streamlit run streamlit_app.py
```

API will be available at: `http://127.0.0.1:8000`

Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`

Streamlit GUI will be available at: `http://localhost:8501/`

---

## 📬 Example Requests

**Create a client:**
```bash
curl -X POST http://127.0.0.1:8000/clients/ \
  -H "Content-Type: application/json" \
  -d '{"client_id": "DE-001", "name": "new client", "address": "new client address 1", "telephone": "111-111-11-11", "email": "new_client_email@email.com"}'
```

**Response:**
```json
{
  "address": "new client address 1",
  "client_id": "DE-111",
  "active": true,
  "email": "new_client_email@email.com",
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
  -d '{"client_id": "DE-001", "tracking_number": "DE-PL-0001", "origin": "Germany", "destination": "Poland"}'
```

**Response:**
```json
{
  "id": 1,
  "client_id": "DE-001",
  "tracking_number": "DE-PL-0001",
  "status": "created",
  "origin": "DE",
  "destination": "PL",
  "created_at": "2026-04-07T12:00:00",
  "updated_at": "2026-04-07T12:00:00"
}
```

**Assign a client to a user:**
```bash
curl -X POST http://127.0.0.1:8000/auth/users/clients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"username": "john_doe", "client_id": "DE-001"}'
```

---

## 🗺️ Roadmap

- [ ] PostgreSQL support
- [x] Client model with foreign key relationship
- [x] User roles (admin, employee, client_user)
- [x] User-client assignments with role-based limits
- [x] Role-based access control on endpoints
- [ ] Docker containerization
- [ ] Authentication (JWT / OAuth 2.0)
- [ ] External API integration
- [x] JOIN queries with SQL visibility
- [x] Dashboard UI (Streamlit)
- [ ] AI anomaly detection layer