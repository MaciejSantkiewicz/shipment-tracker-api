import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"


st.title("👥 Clients")

st.sidebar.title("Filters")

with st.expander("Add client"):
    with st.form("new_client"):
        client_id = st.text_input("Client ID", max_chars=6, placeholder="CC-001")
        name = st.text_input("Name")
        address = st.text_input("Address")
        telephone = st.text_input("Telephone")
        email = st.text_input("Email")

        submitted = st.form_submit_button("Create Client")

        if submitted:
            response = requests.post(
                f"{BASE_URL}/clients/",
                json={
                    "client_id": client_id,
                    "name": name,
                    "address": address,
                    "telephone": telephone,
                    "email": email
                }
            )
            if response.status_code == 201:
                st.success("Client created successfully!")
            else:
                st.error(f"Error: {response.json()['detail']}")

with st.expander("Update client status"):
    with st.form("Update_client_status"):
        client_id = st.text_input("Client ID", max_chars=6)
        status = st.selectbox("Active", (True, False))

        submitted = st.form_submit_button("Update Client Status")

        if submitted:
            response = requests.patch(
                f"{BASE_URL}/clients/status/{client_id}",
                json={"active": status}
            )
            if response.status_code == 200:
                st.success("Client status successfully changed!")
            else:
                st.error(f"Error: {response.json()['detail']}")



endpoint = st.sidebar.selectbox(
    "Select query type",
    ["All clients"]
)

if endpoint == "All clients":
    response = requests.get(f"{BASE_URL}/clients/")
    data = response.json()




st.subheader("SQL Query")
st.code(data["sql"], language="sql")
st.subheader("Results")

st.dataframe(data["data"])