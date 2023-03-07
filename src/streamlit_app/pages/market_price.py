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

symbol = st.text_input("Symbol", "")
timeframe = st.selectbox(
    "Timeframe",
    ["5m", "30m", "1h", "2h", "1d", "3d", "1w", "1M"]
)

if symbol == "":
    symbol = "BTC/USDT"
    
response = requests.get(
    url=base_url + "/binance/get_price_chart",
    params={"symbol": symbol.upper(), "timeframe": timeframe}
)

if st.button("Add to favorite"):
    resp = requests.post(
        url=base_url + "/binance/add_favorite",
        params={"user_id":1, "symbol": symbol.upper()}
    )
    if resp.status_code == 200:
        st.write("Added to favorite")

if response.status_code == 404:
    st.error("Symbol not found")
if response.status_code == 200:
    prices = response.json()["data"]
    current_price = number_fmt.format(response.json()["current_price"])
    compare_last_hour = response.json()["compare_last_hour"]
    compare_last_hour_per = number_fmt.format(response.json()["compare_last_hour_per"])
    compare_last_date = response.json()["compare_last_date"]
    compare_last_date_per = number_fmt.format(response.json()["compare_last_date_per"])
    
    last_hour_sign = "+" if float(compare_last_hour) >= 0 else ""
    last_date_sign = "+" if float(compare_last_date) >= 0 else ""

    st.title(current_price)
    st.markdown("**{0}{1} ({0}{2}%)** Today".format(last_hour_sign, number_fmt.format(compare_last_hour), compare_last_hour_per))
    st.markdown("**{0}{1} ({0}{2}%)** After Hours".format(last_date_sign, number_fmt.format(compare_last_date), compare_last_date_per))
    st.line_chart(prices)

    