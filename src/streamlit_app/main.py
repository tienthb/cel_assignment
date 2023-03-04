import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

API_HOST = os.environ["API_HOST"]
API_PORT = os.environ["API_PORT"]
BASE_URL = f"http://{API_HOST}:{API_PORT}"

if "BASE_URL" not in st.session_state:
    st.session_state["BASE_URL"] = BASE_URL

st.set_page_config(
    page_title="Streamlit app",
    layout="wide"
)

