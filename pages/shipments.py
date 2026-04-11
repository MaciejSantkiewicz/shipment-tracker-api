import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"


# response = requests.get(f"{BASE_URL}/shipments/")
# data = response.json()

st.title("📦 Shipments")



st.sidebar.title("Filters")

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
        ["created", "in_transit", "delivered", "failed"]
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