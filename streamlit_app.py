import streamlit as st

st.set_page_config(
    page_title="Shipment Tracker",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Shipment Tracker — SQL Explorer")
st.markdown("---")

st.markdown("""
Welcome to the **SQL Explorer** — a tool for browsing shipment and client data.

Select a section from the left sidebar:
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("📦 **Shipments** — browse and filter shipments"):
        st.switch_page("pages/shipments.py")


with col1:
    if st.button("👥 **Clients** — browse client data"):
        st.switch_page("pages/clients.py")

    

st.markdown("---")
st.caption("Every operation displays the raw SQL query — to show what happens under the hood.")