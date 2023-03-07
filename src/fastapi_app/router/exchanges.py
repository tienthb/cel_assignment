from fastapi import APIRouter, HTTPException
import ccxt
import pandas as pd
from typing import List

router = APIRouter(
    prefix="/binance",
    tags=["market"]
)

binance = ccxt.binance()
markets = binance.load_markets()
favorite_file_path = f"./favorite.json"


@router.get("/get_price_chart")
def get_price_chart(symbol: str, timeframe: str):
    if symbol not in markets:
        raise HTTPException(status_code=404, detail="Symbol not found")
    
    ohlcv = binance.fetch_ohlcv(symbol, timeframe)
    # get closing price only
    prices = [x[4] for x in ohlcv]
    current_price = prices[-1]
    last_hour_price = binance.fetch_ohlcv(symbol, "1h")
    last_hour_price = last_hour_price[-2][4]

    last_date_price = binance.fetch_ohlcv(symbol, "1d")
    last_date_price = last_date_price[-2][4]
    return {
        "data": prices,
        "current_price": current_price,
        "compare_last_hour":  current_price - last_hour_price,
        "compare_last_hour_per": (current_price - last_hour_price) / last_hour_price,
        "compare_last_date": (current_price - last_date_price),
        "compare_last_date_per": (current_price - last_date_price) / last_date_price
    }

@router.post("/add_favorite")
def update_fav_symbol(user_id: int, symbol: str):
    
    try:
        df = pd.read_json(favorite_file_path)
    except FileNotFoundError:
        df = pd.DataFrame({"user_id": [], "symbol": []})
    df = df.explode("symbol").reset_index(drop=True)
    with open("./test.txt", "w") as f:
        f.write(f"{user_id},{symbol}")
    if len(df[(df["user_id"] == user_id) & (df["symbol"] == symbol)]) > 0:
        raise HTTPException(status_code=404, detail="Symbol existed")
    else:
        df = df.append({"user_id": user_id, "symbol": symbol}, ignore_index=True)
        df.to_json(favorite_file_path)
    return {
        "status": "success"
    }

@router.get("/get_favorite")
def get_favorite_symbol(user_id: int):
    try:
        df = pd.read_json(favorite_file_path)
        df = df.explode("symbol").reset_index(drop=True)
        df = df.loc[df["user_id"] == user_id, "symbol"]
        return {
            "data": df.to_list()
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No symbol in favorite list")
    

@router.get("/get_price_charts")
def get_price_charts(symbols, timeframe: str):
    price_charts = {}
    for symbol in symbols:
        if symbol not in markets:
            raise HTTPException(status_code=404, detail="Symbol not found")
        
        ohlcv = binance.fetch_ohlcv(symbol, timeframe)
        # get closing price only
        price_charts[symbol] = [x[4] for x in ohlcv]
    
    return price_charts