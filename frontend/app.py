import streamlit as st
import os

st.set_page_config(
    page_title="XAI Football Analytics Suite",
    layout="wide"
)

# Load CSS correctly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "style.css")

with open(CSS_PATH) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚽ XAI-Powered Football Analytics Dashboard")
st.write("Use the sidebar to navigate between models.")
