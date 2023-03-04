from fastapi import APIRouter
import pandas as pd

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