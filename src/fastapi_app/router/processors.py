from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter(
    prefix="/processor",
    tags=["processor"]
)

@router.post("/process_data")
async def process_data(csv_file: UploadFile = File(...)):
    resp = {}
    contents = await csv_file.read()

    data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    # Replace LF, reg with Low Fat, Regular
    data["Item_Fat_Content"] = data["Item_Fat_Content"].apply(lambda x: "Regular" if x == "reg" else "Low Fat" if x == "LF" else x)
    # Replace null in Item_Weight
    item_weight = data.loc[~data["Item_Weight"].isna(), ["Item_Identifier", "Item_Weight"]].drop_duplicates()
    data = data.merge(item_weight, how="left", on="Item_Identifier").drop("Item_Weight_x", axis=1).rename(columns={"Item_Weight_y":"Item_Weight"})

    # resp["data"] = data.to_json()
    data.to_csv("./cleaned_data.csv", index=False)
    return {"status": "success"}
