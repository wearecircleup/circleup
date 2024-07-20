import streamlit as st
from menu import menu
import pandas as pd
from utils.body import medium_parragraph,psudo_title,html_banner

st.set_page_config(
    page_title="Circle Up",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Redirect to app.py if not logged in, otherwise show the navigation menu
menu()

# Verify the user's role
if st.session_state.role not in ["Sentinel"]:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title(f"{psudo_title}")
st.subheader(f"You are currently logged with the role of {st.session_state.role}.")
st.markdown(f"<p style='text-align: justify;'>{medium_parragraph}</p>", unsafe_allow_html=True)

with st.container(height=100):
    df = pd.DataFrame([st.session_state.user_auth])
    st.dataframe(df)

st.markdown(f"<p style='text-align: justify;'>{medium_parragraph}</p>", unsafe_allow_html=True)
st.write(st.session_state.user_auth)