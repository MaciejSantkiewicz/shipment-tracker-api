import streamlit as st
import requests

from app.models import ShipmentStatus

BASE_URL = "http://127.0.0.1:8000"


st.title("📦 Shipments")



st.sidebar.title("Filters")

with st.expander("Add shipment"):
    with st.form("new_shipment", clear_on_submit = True):
        client_id = st.text_input("Client ID")
        tracking_number = st.text_input("Tracking number")
        origin = st.text_input("Origin")
        destination = st.text_input("Destination")

        submitted = st.form_submit_button("Create Shipment")

        if submitted:
            response = requests.post(
                f"{BASE_URL}/shipments/",
                json={
                    "client_id": client_id,
                    "tracking_number": tracking_number,
                    "origin": origin,
                    "destination": destination,
                }
            )
            if response.status_code == 201:
                st.success("Shipemnt created successfully!")
            else:
                st.error(f"Error: {response.json()['detail']}")

with st.expander("Delete shipment"):
    with st.form("delete_shipment", clear_on_submit = True):
        tracking_number = st.text_input("Tracking number")

        submitted = st.form_submit_button("Delete shipment")

        if submitted:
            response = requests.delete(
                f"{BASE_URL}/shipments/{tracking_number}"
            )
            if response.status_code == 204:
                st.success("Shipemnt deleted successfully!")
            else:
                st.error(f"Error: {response.json()['detail']}")


with st.expander("Update status"):
    with st.form("update_status"):
        tracking_number = st.text_input("Tracking number")
        status = st.selectbox(
            "Select status",
            ShipmentStatus
        )

        submitted = st.form_submit_button("Update status")
        
        if submitted:
            response = requests.patch(
                f"{BASE_URL}/shipments/{tracking_number}/status",
                json={"status": status}
            )
            if response.status_code == 200:
                st.success("Shipemnt status successfully!")
            else:
                st.error(f"Error: {response.json()['detail']}")



endpoint = st.sidebar.selectbox(
    "Select query type",
    ["All Shipments", "Filter by Status", "With Clients", "Stats", "Stats with HAVING"]
)

if endpoint == "All Shipments":
    response = requests.get(f"{BASE_URL}/shipments/")
    data = response.json()

elif endpoint == "Filter by Status":
    status = st.sidebar.selectbox(
        "Select status",
        ShipmentStatus
    )

    response = requests.get(f"{BASE_URL}/shipments/", params={"status": status})
    data = response.json()

elif endpoint == "With Clients":
    response = requests.get(f"{BASE_URL}/shipments/with-clients")
    data = response.json()

elif endpoint == "Stats":
    response = requests.get(f"{BASE_URL}/shipments/stats")
    data = response.json()

elif endpoint == "Stats with HAVING":
    min_count = st.sidebar.number_input("Minimum shipment count",
                                        min_value= 1,
                                        value= 1)

    response = requests.get(f"{BASE_URL}/shipments/stats/filtered", params={"min_count": min_count})
    data = response.json()


st.subheader("SQL Query")
st.code(data["sql"], language="sql")
st.subheader("Results")

st.dataframe(data["data"])