from fastapi import APIRouter, UploadFile, File
import pandas as pd
import numpy as np
import io

router = APIRouter(
    prefix="/processor",
    tags=["processor"]
)

@router.post("/process_data")
async def process_data(csv_file: UploadFile = File(...), column_name: str = None):
    resp = {}
    contents = await csv_file.read()

    data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    
    # Replace LF, reg with Low Fat, Regular
    data["Item_Fat_Content"] = data["Item_Fat_Content"].apply(lambda x: "Regular" if x == "reg" else "Low Fat" if x == "LF" else x)
    # Replace null in Item_Weight
    item_weight = data.loc[~data["Item_Weight"].isna(), ["Item_Identifier", "Item_Weight"]].drop_duplicates()
    data = data.merge(item_weight, how="left", on="Item_Identifier").drop("Item_Weight_x", axis=1).rename(columns={"Item_Weight_y":"Item_Weight"})

    q1 = np.percentile(data[column_name], 25)
    q3 = np.percentile(data[column_name], 75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    filtered_data = data[(data[column_name] > lower_bound) & (data[column_name] < upper_bound)]

    resp["original_data_size"] = len(data)
    resp["processed_data_size"] = len(filtered_data)
    filtered_data.to_csv("./processed_data.csv", index=False)
    return resp

