import streamlit as st
import altair as alt
import requests
import os
from dotenv import load_dotenv

number_fmt = "{:,.4f}"

load_dotenv()

API_HOST = os.environ["API_HOST"]
API_PORT = os.environ["API_PORT"]
base_url = f"http://{API_HOST}:{API_PORT}"

response = requests.get(
    url=base_url + "/binance/get_favorite",
    params={"user_id": 1}
)

symbols = response.json()["data"]

price_charts = {}

for symbol in symbols:
    response = requests.get(
        url=base_url + "/binance/get_price_chart",
        params={"symbol": symbol, "timeframe": "1d"}
    )
    price_charts[symbol] = response.json()["data"]

st.line_chart(price_charts)
