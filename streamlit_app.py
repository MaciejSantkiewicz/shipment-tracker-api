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
    st.info("📦 **Shipments** — browse and filter shipments")

with col2:
    st.info("👥 **Clients** — browse client data")

st.markdown("---")
st.caption("Every operation displays the raw SQL query — to show what happens under the hood.")