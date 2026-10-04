import streamlit as st

st.set_page_config(
    page_title="College Academic Assistant",
    page_icon="🎓",
    layout="wide"
)

# Load the actual application only after Streamlit has started correctly.
from src.app import *