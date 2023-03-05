from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter(
    prefix="/outlets",
    tags=["outlets"]
)


@router.get("/")
def get_outlets():
    df = pd.read_csv("./cleaned_data.csv")
    return {
        "outlets": df["Outlet_Identifier"].drop_duplicates().to_list()
    }


@router.get("/{outlet_id}/items")
def get_items(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Identifier"]].drop_duplicates()
    return {
        df.to_json()
    }


@router.get("/{outlet_id}/items/count_by_type")
def count_items_by_type(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Identifier", "Item_Type"]].drop_duplicates() \
            .groupby("Item_Type").count().reset_index()
    return {
        df.to_json()
    }


@router.get("/{outlet_id}/items/count_by_fat_content")
def count_items_by_fat_content(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Identifier", "Item_Fat_Content"]].drop_duplicates() \
            .groupby("Item_Fat_Content").count().reset_index()
    return {
        df.to_json()
    }


@router.get("/{outlet_id}/items/sales_by_type")
def sales_items_by_type(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Outlet_Sales", "Item_Type"]].drop_duplicates() \
            .groupby("Item_Type").sum().reset_index()
    return {
        df.to_json()
    }


@router.get("/{outlet_id}/items/sales_by_fat_content")
def sales_items_by_fat_content(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Outlet_Sales", "Item_Fat_Content"]].drop_duplicates() \
            .groupby("Item_Fat_Content").sum().reset_index()
    return {
        df.to_json()
    }


@router.get("/{outlet_id}/total_items")
def get_total_items(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Identifier"]].drop_duplicates()
    return {
        "total_items": len(df)
    }


@router.get("/{outlet_id}/total_sales")
def get_total_sales(outlet_id: str):
    df = pd.read_csv("./cleaned_data.csv")
    df = df.loc[df["Outlet_Identifier"] == outlet_id, ["Item_Outlet_Sales"]].drop_duplicates()
    return {
        "total_sales": df["Item_Outlet_Sales"].sum()
    }