import streamlit as st
import requests
import pandas as pd
import json
import altair as alt
import os

base_url = st.session_state["BASE_URL"]

st.set_page_config(
    page_title="Streamlit app",
    layout="wide"
)



uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    content = uploaded_file.read()
    if st.button("Process data"):
        tab1, tab2, tab3 = st.tabs(["Data Stats", "By Outlet", "By Product"])
        response = requests.post(
            url=base_url + "/process_data",
            files={"csv_file": content}
        )
        resp = response.json()
        
        # with tab2:
        outlets = requests.get(
            url=base_url + "/outlets"
        )
        outlets = outlets.json()
        outlet_id = st.selectbox(
            "Select Outlet",
            outlets["outlets"]
        )

        unique_items = requests.get(
            url=base_url + f"/outlets/{outlet_id}/items"
        )
        st.write(unique_items.json())
            # "Total Outlets"
            # st.title(data["Outlet_Identifier"].nunique())
            # col1, col2 = st.columns(2)
        
            # with col1:
            #     outlet_by_item_type = data.loc[:, ["Item_Identifier", "Outlet_Identifier", "Item_Type"]].drop_duplicates() \
            #         .groupby(["Outlet_Identifier", "Item_Type"]) \
            #         .nunique() \
            #         .reset_index()
            #     outlet_by_item_type_chart = alt.Chart(outlet_by_item_type).mark_bar().encode(
            #         x="Outlet_Identifier",
            #         y="Item_Identifier",
            #         color="Item_Type"
            #     )
            #     st.altair_chart(outlet_by_item_type_chart, use_container_width=True)

            # with col2:
            #     outlet_by_year = data.loc[:, ["Outlet_Type", "Outlet_Identifier"]].drop_duplicates() \
            #         .groupby("Outlet_Type") \
            #         .nunique() \
            #         .reset_index()                
            #     outlet_by_year_chart = alt.Chart(outlet_by_year).mark_bar().encode(
            #         x="Outlet_Type",
            #         y="Outlet_Identifier"
            #     )
            #     st.altair_chart(outlet_by_year_chart, use_container_width=True)