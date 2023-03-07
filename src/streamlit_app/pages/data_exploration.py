import streamlit as st
import requests
import pandas as pd
import json
import altair as alt
from dotenv import load_dotenv
import os

load_dotenv()

API_HOST = os.environ["API_HOST"]
API_PORT = os.environ["API_PORT"]
base_url = f"http://{API_HOST}:{API_PORT}"



st.set_page_config(
    page_title="Streamlit app",
    layout="wide"
)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    content = uploaded_file.read()
    if st.button("Process Data"):
        tab1, tab2 = st.tabs(["Stats", "Visual"])
        response = requests.post(
            url=base_url + "/processor/process_data",
            files={"csv_file": content},
            params={"column_name": "Item_Outlet_Sales"}
        )
        with tab1:
            st.write(response.json())
        
        with tab2:
            outlets = requests.get(
                url=base_url + "/outlets"
            )
            outlets = outlets.json()
            outlet_id = st.selectbox(
                "Select Outlet",
                outlets["outlets"]
            )

            total_items = requests.get(
                url=base_url + f"/outlets/{outlet_id}/total_items"
            )

            total_sales = requests.get(
                url=base_url + f"/outlets/{outlet_id}/total_sales"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Total Items")        
                st.title(total_items.json()["total_items"])

                count_by_types = requests.get(
                    url=base_url + f"/outlets/{outlet_id}/items/count_by_type"
                )

                count_by_types_df = pd.DataFrame(json.loads(count_by_types.json()[0]))
                count_by_types_c = alt.Chart(count_by_types_df).mark_bar().encode(
                    x="Item_Type",
                    y="Item_Identifier"
                )
                st.altair_chart(count_by_types_c)

                count_by_fat_content = requests.get(
                    url=base_url + f"/outlets/{outlet_id}/items/count_by_fat_content"
                )

                count_by_fat_content_df = pd.DataFrame(json.loads(count_by_fat_content.json()[0]))
                count_by_fat_content_c = alt.Chart(count_by_fat_content_df).mark_bar().encode(
                    y="Item_Fat_Content",
                    x="Item_Identifier"
                )
                st.altair_chart(count_by_fat_content_c)

            with col2:        
                st.markdown("Total Sales")        
                st.title(total_sales.json()["total_sales"])

                sales_by_types = requests.get(
                    url=base_url + f"/outlets/{outlet_id}/items/sales_by_type"
                )

                sales_by_types_df = pd.DataFrame(json.loads(sales_by_types.json()[0]))
                sales_by_types_c = alt.Chart(sales_by_types_df).mark_bar().encode(
                    x="Item_Type",
                    y="Item_Outlet_Sales"
                )
                st.altair_chart(sales_by_types_c)

                sales_by_fat_content = requests.get(
                    url=base_url + f"/outlets/{outlet_id}/items/sales_by_fat_content"
                )

                sales_by_fat_content_df = pd.DataFrame(json.loads(sales_by_fat_content.json()[0]))
                sales_by_fat_content_c = alt.Chart(sales_by_fat_content_df).mark_bar().encode(
                    y="Item_Fat_Content",
                    x="Item_Outlet_Sales"
                )
                st.altair_chart(sales_by_fat_content_c)